import os
import json
from ast import literal_eval

import pandas as pd

from databricks import sql
from databricks_cli.dbfs.api import DbfsApi
from databricks_cli.dbfs.dbfs_path import DbfsPath
from databricks_cli.sdk.api_client import ApiClient

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render
from django.urls import reverse
from pyspark.sql import SparkSession

from .models import DataAsset
from .graphql import get_mtm_response

# KMP_DUPLICATE_LIB_OK = True
DATABRICKS_HOST =  os.environ['DATABRICKS_HOST']
DATABRICKS_TOKEN =  os.environ['DATABRICKS_TOKEN']
DATABRICKS_HTTP_PATH = os.environ['DATABRICKS_HTTP_PATH']

# Connect to Postgres Database
USER = os.environ.get('DB_USER')
PASS = os.environ.get('DB_PASSWORD')
HOST = os.environ.get('DB_HOST')
DATABASE = os.environ.get('DB_NAME')
PORT = os.environ.get('DB_PORT')
DB_OPTIONS = literal_eval(os.environ.get('DB_OPTIONS')).get('sslmode')

# Create your views here.
def login_view(request):
    if request.method == 'POST':

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('data_assets_list'))
        else:
            return render(request, 'data_assets/login.html', {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, 'data_assets/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@login_required(login_url='login')
def data_asset_names(request):
    search_query = request.GET.get('q')
    data_assets = DataAsset.objects.filter(name__icontains=search_query)[:5] if search_query else []
    results = [data_asset.name for data_asset in data_assets]
    return JsonResponse(results, safe=False)


@login_required(login_url='login')
def data_asset_search(request):
    search_query = request.GET.get('q')
    if search_query:
        data_assets = DataAsset.objects.filter(name__icontains=search_query)
    else:
        data_assets = DataAsset.objects.all()

    results = [{'id': data_asset.id, 'name': data_asset.name} for data_asset in data_assets]
    return JsonResponse({'tables': results})


@login_required(login_url='login')
def data_assets_list(request):
    # click.get_current_context = lambda: click.Context(command=DummyCommand(), auto_envvar_prefix=None)

    # Create Databricks API client
    api_client = ApiClient(token=DATABRICKS_TOKEN, host=DATABRICKS_HOST)

    # Create DBFS API object using the API client
    dbfs_api = DbfsApi(api_client)
    
    # Get list of files in the directory
    dbfs_path_str = "dbfs:/user/hive/warehouse/mtm_stage.db"
    dbfs_path = DbfsPath(dbfs_path_str)
    dbfs_files = dbfs_api.list_files(dbfs_path)
    
    # Process files as needed
    data_assets = []
    search_query = request.GET.get('q', '')
    
    if search_query:
        data_assets = DataAsset.objects.filter(name__icontains=search_query)
    else:
        for file in dbfs_files:
            if file.is_dir:
                data_asset_name = str(file.dbfs_path).split('/')[-1].replace('\x1b[0m', '')
                data_asset = DataAsset.objects.get_or_create(name=data_asset_name)[0]
                data_assets.append(data_asset)
    
    return render(request, 'data_assets/list.html', {'data_assets': data_assets,
        'search_query': search_query})


@login_required(login_url='login')
def data_asset_detail(request, pk):
    data_asset = DataAsset.objects.get(pk=pk)

    # Query data from Databricks Delta table
    connection = sql.connect(
        server_hostname=DATABRICKS_HOST.replace('https://', ''),
        http_path=DATABRICKS_HTTP_PATH,
        access_token=DATABRICKS_TOKEN,
        _tls_no_verify=True
    )
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM delta.`dbfs:/user/hive/warehouse/mtm_stage.db/{data_asset.name}`")
        data = cursor.fetchall()

    # Convert data to a DataFrame
    columns = [key for key in data[0].asDict()]
    df = pd.DataFrame(data, columns=columns)
    html_top_5 = df.head().to_html(index=False)
    print(html_top_5)

    # Process the data
    sample_statistics = "TODO"

    # Update the DataAsset object with the processed data
    data_asset.sample_statistics = sample_statistics
    data_asset.save()

    # Return the HTML output
    return render(request, 'data_assets/detail.html', {
        'data_asset': data_asset, 'html_top_5': html_top_5})


@login_required(login_url='login')
def query_data(request, table_name):
    question = request.GET.get('question', '')

    # Create a SparkSession using Databricks Connect
    spark = (
        SparkSession.builder
        .appName("ManagedTableQuery")
        .config("spark.databricks.service.server.enabled", "true")
        .getOrCreate()
    )

    # Set the current database in the SparkSession
    spark.catalog.setCurrentDatabase('mtm_stage')

    # Query the specified table
    df = spark.sql(f"SELECT * FROM {table_name}")

    # Convert the DataFrame to a pandas DataFrame
    dff = df.toPandas()

    # Generate the pandas code using the Sketch package and capture the HTML output
    html_output = dff.sketch.howto(question, call_display=False)

    # Execute the HTML output using eval()
    eval_output = eval(html_output)

    # Convert the result to JSON format
    result = eval_output.to_json()

    # Stop the SparkSession
    spark.stop()
    context = {'result': result}
    return render(request, 'data_assets/query_data_search.html', context)


@login_required(login_url='login')
def query_data_search(request):
    table_name = request.GET.get('table_name')
    if table_name:
        url = reverse('query_data', args=[table_name])
    else:
        table_name = ''
        url = reverse('query_data_search')

    context = {
        'table_name': table_name,
        'url': url,
    }

    return render(request, 'data_assets/query_data_search.html', context)


@login_required(login_url='login')
def neural_search(request):
    if request.method == 'GET':
        brands = request.user.brands.all()
        regions = request.user.regions.all()
        return render(request, 'data_assets/neural_search.html', {
            'brands': brands,
            'regions': regions
        })
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        question = data['question']

        return StreamingHttpResponse(
            streaming_content=get_mtm_response(question, request.user)
        )

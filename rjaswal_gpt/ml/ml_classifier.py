# import json
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.svm import SVC
# from sklearn.model_selection import train_test_split

# # Load the labeled dataset from a JSON file
# with open('labeled_queries.json') as file:
#     labeled_queries = json.load(file)

# # # Prepare the data
# # queries = [query for query, _ in labeled_queries]
# # labels = [label for _, label in enumerate(labeled_queries)]

# # Prepare the data
# queries = []
# labels = []
# for item in labeled_queries:
#     queries.append(item['query'])
#     labels.append(item['table'])

# print(labels)

# # Create a TF-IDF vectorizer
# vectorizer = TfidfVectorizer()

# # Convert the queries into feature vectors
# X = vectorizer.fit_transform(queries)

# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

# # Train an SVM classifier
# classifier = SVC()
# classifier.fit(X_train, y_train)

# # Example usage
# user_query = "What is the number of retained consumers for Clinique in North America?"
# user_query_vector = vectorizer.transform([user_query])
# predicted_table = classifier.predict(user_query_vector)[0]
# print("Predicted table:", predicted_table)


import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import joblib

# Load the labeled dataset from a JSON file
with open('labeled_queries.json') as file:
    labeled_queries = json.load(file)

# Prepare the data
queries = []
labels = []
for item in labeled_queries:
    queries.append(item['query'])
    labels.append(item['table'])

# Create a TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Convert the queries into feature vectors
X = vectorizer.fit_transform(queries)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

# Train an SVM classifier
classifier = SVC()
classifier.fit(X_train, y_train)

# Save the trained model and vectorizer
joblib.dump(classifier, 'classifier.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
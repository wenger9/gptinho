document.addEventListener('DOMContentLoaded', () => {
    // Identify input box
    const inputBox = document.querySelector('#id_q_dropdown');
    
    // Set up event listener for search box
    inputBox.addEventListener('keyup', () => {
        const searchQuery = inputBox.value;
        console.log(`Searching: ${searchQuery}`);
        getTables(searchQuery);
    });

    // Set up event listener for search clear
    const clearButton = document.querySelector('#clear-button');
    clearButton.addEventListener('click', () => {
        inputBox.value = '';
        getTables(inputBox.value);
    });
});


async function getTables(query) {
    // Collect data from API
    const response = await fetch(`search?q=${query}`);
    const data = await response.json();
    outputTable = document.querySelector('tbody');
    outputTable.innerHTML='';
    for (table of data['tables']) {
        const table_row = document.createElement('tr');
        table_row.innerHTML = `<td><a href="/data_assets/${table['id']}/">${table['name']}</a></td>`
        outputTable.append(table_row);
    }    
}
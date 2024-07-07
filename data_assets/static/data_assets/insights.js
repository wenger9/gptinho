document.addEventListener('DOMContentLoaded', () => {
    // Identify input box
    const inputBox = document.querySelector('#search-box');
    const queryForm = document.querySelector('#insights-search');
    const intermediateToggle = document.querySelector('#intermediateToggle');

    // Set up event listener for search box
    queryForm.onsubmit = () => {
        const searchQuery = inputBox.value;
        console.log(`Searching: ${searchQuery}`);
        updateText('insightOutput', JSON.stringify({"type": "start",
            "text": `Running new query: ${searchQuery}`}))
        // Clear out text in search bar
        inputBox.value = ''
        // Start spinner
        showLoadingSpinner(document.querySelector('.btn'));
        getInisghts(searchQuery);
        return false;
    };

    // Add event listener to intermediate output toggle
    intermediateToggle.addEventListener('change', () => {
        const intOutputs = document.querySelectorAll('.intermediate');
        for (output of intOutputs) {
            output.classList.toggle('hidden');
        }
    })

});

async function getInisghts(query) {   
    // Get csrf token
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    // Send query via AJAX request for processing
    const response = await fetch('', {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin', // Do not send CSRF token to another domain.
        body: JSON.stringify({
            question: query
        })
    });
    // Capture streaming response
    const reader = response.body.getReader();
    // Output streaming response via infinite loop
    while (true) {
        const {value, done} = await reader.read();
        if (done) {
            hideLoadingSpinner(document.querySelector('.btn'));
            break;
        }
        // Streaming response is in byte arrays; need to turn into text.
        let decodedStr = new TextDecoder().decode(value); 
        // Send to function for display on page
        updateText('insightOutput', decodedStr);
    }
}

function updateText(htmlId, text, bold=false) {
    // Convert text to JSON object
    text = JSON.parse(text);
    const outputElement = document.querySelector(`#${htmlId}`);
    // Split text into array of separate lines
    const arrayText = text['text'].split('\n');
    // Wrap each line of text in a <p> element and add to output <div>
    for (const line of arrayText) {
        const newText = document.createElement('p');
        newText.classList.add('code-output');
        // Allow intermediate text to be toggled by adding a specific class
        if (text['type'] === 'intermediate') {
            newText.classList.add('intermediate');
            newText.classList.add('hidden');
        }
        if (intermediateToggle.checked) {
            newText.classList.remove('hidden');
        }
        newText.innerText = line;
        outputElement.append(newText);
    }
    // Include line break when output is final
    if (text['type'] === 'final') {
        outputElement.append(document.createElement('hr'));
    }
}

function showLoadingSpinner(button) {
    button.innerHTML = `
    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    <span class="sr-only">Fetching...</span>
    `;
    button.setAttribute('disabled', true);
}

function hideLoadingSpinner(button) {
    button.innerHTML = 'Search';
    button.removeAttribute('disabled');
}

async function typeWriter(text, textElement) {
    words = text.split(' ');
    let i = 0;
    while (i < words.length) {
        await typeWriterDelay(100);
        textElement.innerText.concat(' ', words[i]);
        i++;
        console.log(i, textElement.innerText)
    }
    return;
}


function typeWriterDelay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
  }
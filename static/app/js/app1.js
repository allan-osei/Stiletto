function post_note() {
    note_element = document.getElementById("note-text");
    rating_element = document.getElementById("note-rating");
    oid = document.getElementById("note-webhook-id");
    wid = document.getElementById("note-webhook-wid");
    fetch(
        "localhost:8000/journal_note_api" + wid, {
            "method": "POST",
            "body": JSON.stringify({
                "note": note_element.textContent.trim(),
                "rating": rating_element.textContent.trim(),
                "pk": oid
            })
        }
    )
}

function get_notes(wid, w) {
    fetch(
        `http://localhost:8000/journal_note_api?w=${w}&wid=${wid}`,{"method":"GET"}
    ).then((res) => res.json()
    ).then((data) => {
        if (!data.message) {
            showToast("There's no data to export");
            return;
        }
        const decodedData = atob(data.message);
        const linkSource = `data:text/plain;charset=utf-8,${encodeURIComponent(decodedData)}`;
        const downloadLink = document.createElement("a");
        const fileName = "Compiled Notes.txt";
        downloadLink.href = linkSource;
        downloadLink.download = fileName;
        downloadLink.click();
    })
}

function get_note(wid, w) {
    fetch(
        `localhost:8000/journal_note_api?w=${w}&wid=${wid}`,{"method":"GET"}
    ).then((res) => res.json()
    ).then((data) => {
        message = data.message;
        note_element = document.getElementById("note-text");
        rating_element = document.getElementById("note-rating");
        note_element.innerText = message.note;
        rating_element.innerText = message.rating;
    })
}


function copy(event) {
    navigator.clipboard.writeText(document.getElementById('link').innerText).then(function() {
    // Create and show toast notification
    showToast("Copied to clipboard!");
}, function(err) {
    console.error('Could not copy text: ', err);
    showToast("Failed to copy text.");
});
}
   
function add_data(wid, w, name, n, messagePrefix, messageSuffix, chat_ids, parse, messageFormat) {
    document.getElementById("editmodalwid").value = wid;
    document.getElementById("editmodalw").value = w;
    if (w == "discord") {
        document.getElementById("cid").innerText = "Chat Webhook Url";
    }
    document.getElementById("editmodalw").setAttribute('data', n);
    if (w == "discord" || w == "tg") {
        chat_ids.forEach(function(chat_id) {
            var chatIdInput = document.createElement("input");
            chatIdInput.type = "text";
            chatIdInput.className = "form-control mb-1 to-be-deleted chatid";
            chatIdInput.name = "chat_id";
            chatIdInput.required = true;
            chatIdInput.value = chat_id;
            chatIdInput.setAttribute('data', chat_id);
            document.querySelector('#editmodal form').insertBefore(chatIdInput, document.querySelector('#editmodal .float-end'));
        });
        var messagePrefixInput = document.createElement("textarea");
        messagePrefixInput.type = "text";
        messagePrefixInput.className = "form-control mb-1 to-be-deleted input2";
        messagePrefixInput.name = "message-prefix";
        messagePrefixInput.required = true;
        messagePrefixInput.value = messagePrefix;
        var messagePrefixLabel = document.createElement("label");
        messagePrefixLabel.for = "message-prefix";
        messagePrefixLabel.innerText = "Message Prefix";
        var messagePrefixBox = document.createElement("div");
        messagePrefixBox.className = "message-box to-be-deleted";
        messagePrefixBox.appendChild(messagePrefixLabel);
        messagePrefixBox.appendChild(messagePrefixInput);
        document.querySelector('#editmodal form').insertBefore(messagePrefixBox, document.querySelector('#editmodal .float-end'));

        var messageSuffixInput = document.createElement("textarea");
        messageSuffixInput.className = "form-control mb-1 to-be-deleted input2";
        messageSuffixInput.name = "message-suffix";
        messageSuffixInput.required = true;
        messageSuffixInput.value = messageSuffix;
        var messageSuffixLabel = document.createElement("label");
        messageSuffixLabel.for = "message-suffix";
        messageSuffixLabel.innerText = "Message Suffix";
        var messageSuffixBox = document.createElement("div");
        messageSuffixBox.className = "message-box to-be-deleted mt-2";
        messageSuffixBox.appendChild(messageSuffixLabel);
        messageSuffixBox.appendChild(messageSuffixInput);
        document.querySelector('#editmodal form').insertBefore(messageSuffixBox, document.querySelector('#editmodal .float-end'));
        var nameInput = document.createElement("input");
        nameInput.type = "text";
        nameInput.className = "form-control mb-1 to-be-deleted";
        nameInput.name = "name";
        nameInput.required = true;
        nameInput.value = name;
        var nameLabel = document.createElement("label");
        nameLabel.for = "name";
        nameLabel.className = "to-be-deleted mt-2";
        nameLabel.innerText = "Name";
        document.querySelector('#editmodal form').insertBefore(nameLabel, document.querySelector('#editmodal .float-end'));
        document.querySelector('#editmodal form').insertBefore(nameInput, document.querySelector('#editmodal .float-end'));

        var parse = document.createElement("input");
        parse.type = "checkbox";
        parse.className = "form-check-input to-be-deleted mx-1";
        parse.name = "parse";
        parse.required = false;
        parse.checked = true; // Make it checked by default
        parse.setAttribute('onChange', 'is_checked()');
        var parseLabel = document.createElement("label");
        parseLabel.for = "parse";
        parseLabel.className = "to-be-deleted mr-1";
        parseLabel.innerText = "Parse";
        var parseBox = document.createElement("div");
        parseBox.className = "to-be-deleted mt-3";
        parseBox.appendChild(parseLabel);
        parseBox.appendChild(parse);
        document.querySelector('#editmodal form').insertBefore(parseBox, document.querySelector('#editmodal .float-end'));
        
        
        var messageFormatInput = document.createElement("textarea");
        messageFormatInput.type = "text";
        messageFormatInput.className = "form-control mb-1 to-be-deleted input2";
        messageFormatInput.name = "message-format";
        messageFormatInput.required = true;
        messageFormatInput.value = messageFormat;
        var messageFormatLabel = document.createElement("label");
        messageFormatLabel.for = "message-format";
        messageFormatLabel.className = "to-be-deleted";
        messageFormatLabel.innerText = "Message Format";
        var messageFormatBox = document.createElement("div");
        messageFormatBox.className = "message-box to-be-deleted mt-2";
        messageFormatBox.appendChild(messageFormatLabel);
        messageFormatBox.appendChild(messageFormatInput);
        document.querySelector('#editmodal form').insertBefore(messageFormatBox, document.querySelector('#editmodal .float-end'));
        
        if (parse.checked == "False") {
            messageFormatBox.style.display = "none";
        }



    } else if (w == "mt5") {
        var nameInput = document.createElement("input");
        nameInput.type = "text";
        nameInput.className = "form-control mb-1 to-be-deleted";
        nameInput.name = "name";
        nameInput.required = true;
        nameInput.value = name;
        var nameLabel = document.createElement("label");
        nameLabel.for = "name";
        nameLabel.className = "to-be-deleted";
        nameLabel.innerText = "Name";
        document.querySelector('#editmodal form').insertBefore(nameLabel, document.querySelector('#editmodal .float-end'));
        document.querySelector('#editmodal form').insertBefore(nameInput, document.querySelector('#editmodal .float-end'));
    }
}
function removeElements() {
    var elements = document.getElementsByClassName('to-be-deleted');
    while(elements.length > 0){
        elements[0].parentNode.removeChild(elements[0]);
    }
}

function is_checked() {
    var checkbox = document.querySelector('#editmodal input[name="parse"]');
    if (checkbox.checked) {
        var messageFormatTextarea = document.querySelector('#editmodal textarea[name="message-format"]').parentElement;
        messageFormatTextarea.style.display = "block";
    } else {
        // Checkbox is not checked
        var messageFormatTextarea = document.querySelector('#editmodal textarea[name="message-format"]').parentElement;
        messageFormatTextarea.style.display = "none";
        }
    }

document.querySelector('.tt-2').parentElement.style.display = "none";
function show_tg_parse(element) {
        var checkbox = element;
        if (checkbox.checked) {
            var messageFormatTextarea = document.querySelector('.tt-2');
            messageFormatTextarea.parentElement.style.display = "block";
            messageFormatTextarea.style.display = "block";
            
        } else {
            // Checkbox is not checked
            var messageFormatTextarea = document.querySelector('.tt-2');
            messageFormatTextarea.parentElement.style.display = "none";
            messageFormatTextarea.style.display = "none";
            }
        }



function add_chat_id() {
    var b = document.getElementById("editmodalw");
    var maxChats = b.getAttribute("data"); // Change this to the maximum number of chats allowed
    var numChats = document.querySelectorAll('#editmodal input[name="chat_id"]').length;
    if (numChats >= maxChats) {
        showToast("Exceeded max number of chats, upgrade to add more");
        return;
    }
    console.log(maxChats, numChats)
    var newInput = document.createElement('input');
    newInput.type = 'text';
    newInput.className = 'form-control mb-1';
    newInput.name = 'chat_id';
    newInput.setAttribute('data', "new");
    newInput.required = true;
    var chatInputs = document.querySelectorAll('#editmodal form input[name="chat_id"]');
    var lastChatInput = chatInputs.length > 0 ? chatInputs[chatInputs.length - 1] : null;
    lastChatInput.parentNode.insertBefore(newInput, lastChatInput.nextSibling);
}
 
function appendText() {
    var chatInputs = document.querySelectorAll('#editmodal input[name="chat_id"]');
    chatInputs.forEach(function(input) {
        var data = input.getAttribute('data');
        input.value = data + ':' + input.value;
    });
}

function displayError(message) {
    const errorContainer = document.createElement('div');
    errorContainer.classList.add('error-container', 'position-fixed', 'top-0', 'end-0', 'p-3');

    const errorHTML = `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
            <strong>Error!</strong> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;

    errorContainer.innerHTML = errorHTML;
    document.body.appendChild(errorContainer);

    // Automatically remove the error message after 5 seconds
    setTimeout(() => {
        document.body.removeChild(errorContainer);
    }, 10000);
}

function toggleCarouselDisplay() {
    const carousel1 = document.getElementById('carouselExampleAutoplaying1');
    const carousel2 = document.getElementById('carouselExampleAutoplaying2');
    const screenWidth = window.innerWidth;

    if (screenWidth < 768) { // Assuming 768px as the breakpoint for smaller screens
        if (carousel1 && carousel2) {
            carousel1.style.display = 'none';
            carousel2.style.display = 'block';
        }
    } else {
        if (carousel1 && carousel2) {
            carousel1.style.display = 'block';
            carousel2.style.display = 'none';
        }
    }
}

// Add event listener to window resize to handle dynamic changes in screen size
window.addEventListener('resize', toggleCarouselDisplay);

// Initial call to set the correct display on load
toggleCarouselDisplay();


function toggleStar(element) {
    const stars = element.parentElement.querySelectorAll('.bi-star, .bi-star-fill');
    let isChecked = false;

    stars.forEach(star => {
        if (isChecked) {
            star.classList.remove('bi-star-fill');
            star.classList.add('bi-star');
        } else {
            star.classList.remove('bi-star');
            star.classList.add('bi-star-fill');
        }

        if (star === element) {
            isChecked = true;
        }
    });
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function submitNote(element, link, pk) {
    const textareaValue = element.parentElement.parentElement.parentElement.querySelector('textarea').value.trim();
    const stars = element.parentElement.parentElement.querySelectorAll('.bi-star, .bi-star-fill');
    let filledStars = 0;

    stars.forEach(star => {
        if (star.classList.contains('bi-star-fill')) {
            filledStars++;
        }
    });

    const requestBody = { 'note-rating': filledStars, 'pk': pk };

    if (textareaValue !== '' && textareaValue !== null) {
        requestBody['note-text'] = textareaValue;
    }

    fetch(link, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Function to get the CSRF token from the cookie
        },
        body: JSON.stringify(requestBody),
    })
    .then(response => {
        if (response.ok) {
           showToast('Note submitted successfully');
        } else {
            displayError('Failed to submit note');
        }
    })
    .catch(error => {
        console.error('Error submitting note:', error);
        displayError('Error submitting note');
    });
}




function showToast(message) {
    const toastContainer = document.createElement('div');
    toastContainer.classList.add('toast-container', 'position-fixed', 'bottom-0', 'end-0', 'p-3');

    const toastHTML = `
        <div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <strong class="me-auto">Notification</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">${message}</div>
        </div>
    `;

    toastContainer.innerHTML = toastHTML;
    document.body.appendChild(toastContainer);

    const toastElement = toastContainer.querySelector('.toast');
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 10000
    });

    toast.show();

    // Remove the toast from DOM after it's hidden
    toastElement.addEventListener('hidden.bs.toast', () => {
        document.body.removeChild(toastContainer);
    });
}
function toggle_note(pk, wid) {
    console.log("kk")
    id = document.getElementById("note-webhook-id");
    wid = document.getElementById("note-webhook-wid");
    id.setAttribute('value', pk);
    wid.setAttribute('value', wid);
    get_note(wid, pk)
    // var myModal = new Modal(document.getElementById('note-create'), options);
    // myModal.show();

}


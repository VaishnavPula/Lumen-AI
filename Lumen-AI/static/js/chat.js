// =========================
// CHAT PAGE JAVASCRIPT
// =========================


// Maximum message length

let MAX_LENGTH = 2000;


// =========================
// GET HTML ELEMENTS
// =========================

let messages = document.getElementById("messages");

let welcome = document.getElementById("welcome");

let form = document.getElementById("chat-form");

let input = document.getElementById("message-input");

let sendButton = document.getElementById("send-btn");

let charCount = document.getElementById("char-count");

let historyList = document.getElementById("history-list");

let historyEmpty = document.getElementById("history-empty");

let newChatButton = document.getElementById("new-chat-btn");

let deleteButton = document.getElementById("delete-chat-btn");

let title = document.getElementById("chat-title");

let sidebar = document.getElementById("sidebar");

let overlay = document.getElementById("overlay");

let sidebarButton = document.getElementById("sidebar-toggle");


// =========================
// CURRENT CHAT
// =========================

let conversationId = null;

let sending = false;


// =========================
// API FUNCTION
// =========================

async function api(url, options) {

    try {

        let response = await fetch(url, options);

        let data = {};


        try {

            data = await response.json();

        }
        catch (error) {

            data = {};

        }


        // If user is not logged in

        if (response.status == 401) {

            window.location.href = "/login";

        }


        return {

            ok: response.ok,

            status: response.status,

            data: data

        };

    }
    catch (error) {

        return {

            ok: false,

            status: 0,

            data: {

                error:
                    "Could not reach the server. Check your connection and try again."

            }

        };

    }

}


// =========================
// TIME FUNCTIONS
// =========================

function formatTime(time) {

    let date;


    if (time) {

        date = new Date(time);

    }
    else {

        date = new Date();

    }


    return date.toLocaleTimeString([], {

        hour: "2-digit",

        minute: "2-digit"

    });

}


function dayLabel(time) {

    let date = new Date(time);

    let today = new Date();

    let yesterday = new Date();


    yesterday.setDate(today.getDate() - 1);


    if (date.toDateString() == today.toDateString()) {

        return "Today";

    }


    if (date.toDateString() == yesterday.toDateString()) {

        return "Yesterday";

    }


    return date.toLocaleDateString([], {

        month: "short",

        day: "numeric"

    });

}


// =========================
// SCROLL TO BOTTOM
// =========================

function scrollToBottom() {

    messages.scrollTop = messages.scrollHeight;

}


// =========================
// FORMAT MESSAGE
// =========================

function buildContent(text) {

    let fragment =
        document.createDocumentFragment();


    let parts = text.split("```");


    parts.forEach(function(part, index) {


        // Code block

        if (index % 2 == 1) {

            let lines = part.split("\n");

            let firstLine = lines[0].trim();

            let language =
                /^[\w+#-]*$/.test(firstLine);

            let body;


            if (language) {

                body = lines.slice(1);

            }
            else {

                body = lines;

            }


            let pre =
                document.createElement("pre");

            let code =
                document.createElement("code");


            code.textContent =
                body.join("\n").replace(/\n$/, "");


            pre.appendChild(code);

            fragment.appendChild(pre);

        }


        // Normal text

        else if (part.trim()) {

            let div =
                document.createElement("div");

            div.className = "text";

            div.textContent = part.trim();

            fragment.appendChild(div);

        }

    });


    return fragment;

}


// =========================
// ADD MESSAGE
// =========================

function addMessage(type, text, timestamp) {

    welcome.hidden = true;


    let message =
        document.createElement("div");


    message.className =
        "message " + type;


    let bubble =
        document.createElement("div");


    bubble.className =
        "bubble-body";


    bubble.appendChild(
        buildContent(text)
    );


    message.appendChild(bubble);


    let meta =
        document.createElement("div");


    meta.className = "meta";


    let time =
        document.createElement("span");


    time.textContent =
        formatTime(timestamp);


    meta.appendChild(time);


    // Add Copy button to bot messages

    if (type == "bot") {

        let copyButton =
            document.createElement("button");


        copyButton.type = "button";

        copyButton.className = "copy-btn";

        copyButton.textContent = "Copy";


        copyButton.addEventListener(
            "click",
            function() {

                copyText(
                    text,
                    copyButton
                );

            }
        );


        meta.appendChild(copyButton);

    }


    message.appendChild(meta);

    messages.appendChild(message);


    scrollToBottom();


    return message;

}


// =========================
// COPY MESSAGE
// =========================

async function copyText(text, button) {

    try {

        await navigator.clipboard.writeText(text);

        button.textContent = "Copied!";

    }
    catch (error) {

        button.textContent = "Press Ctrl+C";

    }


    setTimeout(function() {

        button.textContent = "Copy";

    }, 1500);

}


// =========================
// TYPING ANIMATION
// =========================

function showTyping() {

    let message =
        document.createElement("div");


    message.className =
        "message bot";


    message.id =
        "typing-indicator";


    message.innerHTML =
        '<div class="bubble-body">' +

        '<div class="typing">' +

        '<span></span>' +
        '<span></span>' +
        '<span></span>' +

        '</div>' +

        '</div>';


    messages.appendChild(message);


    scrollToBottom();

}


function hideTyping() {

    let typing =
        document.getElementById(
            "typing-indicator"
        );


    if (typing) {

        typing.remove();

    }

}


// =========================
// CLEAR MESSAGES
// =========================

function clearMessages() {

    let messageList =
        messages.querySelectorAll(".message");


    messageList.forEach(function(message) {

        message.remove();

    });


    welcome.hidden = false;

}


// =========================
// LOAD CHAT HISTORY
// =========================

async function loadConversations() {

    let result =
        await api("/api/conversations");


    if (!result.ok) {

        return;

    }


    let conversations =
        result.data.conversations || [];


    historyList.innerHTML = "";


    if (conversations.length > 0) {

        historyEmpty.hidden = true;

    }
    else {

        historyEmpty.hidden = false;

    }


    let lastDay = "";


    conversations.forEach(function(conversation) {


        let day =
            dayLabel(
                conversation.updated_at
            );


        if (day != lastDay) {

            let heading =
                document.createElement("li");


            heading.className =
                "history-group";


            heading.textContent = day;


            historyList.appendChild(
                heading
            );


            lastDay = day;

        }


        let item =
            document.createElement("li");


        let button =
            document.createElement("button");


        button.type = "button";

        button.className =
            "history-item";


        if (conversation.id == conversationId) {

            button.classList.add("active");

        }


        button.textContent =
            conversation.title;


        button.title =
            conversation.title;


        button.addEventListener(
            "click",
            function() {

                openConversation(
                    conversation.id
                );

            }
        );


        item.appendChild(button);

        historyList.appendChild(item);

    });

}


// =========================
// OPEN OLD CHAT
// =========================

async function openConversation(id) {

    let result =
        await api(
            "/api/conversations/" + id
        );


    closeSidebar();


    if (!result.ok) {

        addMessage(
            "bot error",

            result.data.error ||
            "Could not open that chat."
        );

        return;

    }


    conversationId = id;


    clearMessages();


    title.textContent =
        result.data.conversation.title;


    deleteButton.hidden = false;


    result.data.messages.forEach(
        function(message) {

            addMessage(

                message.sender,

                message.message,

                message.timestamp

            );

        }
    );


    loadConversations();


    input.focus();

}


// =========================
// NEW CHAT
// =========================

async function startNewChat() {

    let result =
        await api(
            "/api/conversations/new",
            {
                method: "POST"
            }
        );


    closeSidebar();


    if (!result.ok) {

        addMessage(
            "bot error",

            result.data.error ||
            "Could not start a new chat."
        );

        return;

    }


    conversationId =
        result.data.conversation_id;


    clearMessages();


    title.textContent =
        "New chat";


    deleteButton.hidden = true;


    loadConversations();


    input.focus();

}


// =========================
// DELETE CHAT
// =========================

async function deleteCurrentChat() {

    if (conversationId == null) {

        return;

    }


    let answer =
        confirm(
            "Delete this chat? This cannot be undone."
        );


    if (!answer) {

        return;

    }


    let result =
        await api(

            "/api/conversations/" +
            conversationId,

            {
                method: "DELETE"
            }

        );


    if (!result.ok) {

        addMessage(
            "bot error",

            result.data.error ||
            "Could not delete the chat."
        );

        return;

    }


    conversationId = null;


    clearMessages();


    title.textContent =
        "Lumen";


    deleteButton.hidden = true;


    loadConversations();

}


// =========================
// SENDING STATUS
// =========================

function setSending(status) {

    sending = status;


    sendButton.disabled = status;

    input.disabled = status;


    if (status == false) {

        input.focus();

    }

}


// =========================
// CHARACTER COUNTER
// =========================

function updateCounter() {

    charCount.textContent =
        input.value.length +
        " / " +
        MAX_LENGTH;

}


// =========================
// AUTO RESIZE TEXTAREA
// =========================

function autoResize() {

    input.style.height = "auto";


    input.style.height =
        Math.min(
            input.scrollHeight,
            160
        ) + "px";

}


// =========================
// SEND MESSAGE
// =========================

async function sendMessage(text) {

    text = text.trim();


    if (text == "") {

        return;

    }


    if (sending) {

        return;

    }


    // Show user message

    addMessage(
        "user",
        text
    );


    // Clear input

    input.value = "";


    updateCounter();

    autoResize();


    // Disable input

    setSending(true);


    // Show typing animation

    showTyping();


    // Send message to Flask

    let result =
        await api(

            "/api/chat",

            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"

                },

                body: JSON.stringify({

                    message: text,

                    conversation_id:
                        conversationId

                })

            }

        );


    // Remove typing animation

    hideTyping();


    if (result.ok) {


        conversationId =
            result.data.conversation_id;


        title.textContent =
            result.data.title;


        deleteButton.hidden = false;


        // Show AI response

        addMessage(

            "bot",

            result.data.reply,

            result.data.timestamp

        );


        // Refresh history

        loadConversations();

    }
    else {


        addMessage(

            "bot error",

            result.data.error ||

            "Sorry, something went wrong. Please try again."

        );

    }


    // Enable input

    setSending(false);

}


// =========================
// MOBILE SIDEBAR
// =========================

function openSidebar() {

    sidebar.classList.add("open");

    overlay.hidden = false;

}


function closeSidebar() {

    sidebar.classList.remove("open");

    overlay.hidden = true;

}


// =========================
// FORM SUBMIT
// =========================

form.addEventListener(
    "submit",
    function(event) {

        event.preventDefault();

        sendMessage(input.value);

    }
);


// =========================
// ENTER KEY
// =========================

input.addEventListener(
    "keydown",
    function(event) {


        if (

            event.key == "Enter" &&

            event.shiftKey == false &&

            event.isComposing == false

        ) {

            event.preventDefault();

            sendMessage(input.value);

        }

    }
);


// =========================
// INPUT CHANGES
// =========================

input.addEventListener(
    "input",
    function() {

        updateCounter();

        autoResize();

    }
);


// =========================
// SUGGESTION BUTTONS
// =========================

let suggestions =
    document.querySelectorAll(
        ".suggestion"
    );


suggestions.forEach(
    function(button) {

        button.addEventListener(
            "click",
            function() {

                sendMessage(
                    button.textContent
                );

            }
        );

    }
);


// =========================
// BUTTON EVENTS
// =========================

newChatButton.addEventListener(
    "click",
    startNewChat
);


deleteButton.addEventListener(
    "click",
    deleteCurrentChat
);


sidebarButton.addEventListener(
    "click",
    openSidebar
);


overlay.addEventListener(
    "click",
    closeSidebar
);


// =========================
// START CHAT PAGE
// =========================

loadConversations();

input.focus();

updateCounter();
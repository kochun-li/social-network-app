"use strict"

function loadPosts() {
    let xhr = new XMLHttpRequest()
    // event handler that gets called whenever readyState changes
    xhr.onreadystatechange = function() {
        if (xhr.readyState !== 4) return
        // if request is DONE, call updatePage
        updatePage(xhr)
    }

    xhr.open("GET", getPostURL, true)
    xhr.send()
}

function updatePage(xhr) {
    if (xhr.status === 200) {
        // we do not check if fails to parse as data sent back from server
        // and we know we won't mess up in server side
        // Receive server dat aa sXML(or JSON or HTML or even text)
        // parse the JSON text into JavaScript Object
        let response = JSON.parse(xhr.responseText)
        if (response['posts'].length > 0) {
            updatePost(response['posts'])
        }
        updateComments(response['comments'])
        return
    }

    if (xhr.status === 0) {
        displayError("Cannot connect to server")
        return
    }


    if (!xhr.getResponseHeader('content-type') === 'application/json') {
        displayError(`Received status = ${xhr.status}`)
        return
    }

    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    }

    displayError(response)
}

function displayError(message) {
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}

function updatePost(posts) {
    let globalPosts = document.getElementById("global-posts")

    // Adds each to do post item received from the server to the displayed list
    posts.forEach(post => {
        const postId = `id_post_div_${post.id}`
        if (document.getElementById(postId) === null) {
            if (globalPosts.firstChild !== null) {
                globalPosts.insertBefore(makePostHTML(post), globalPosts.firstChild)
            } else {
                globalPosts.appendChild(makePostHTML(post))
            }
        }
    })
}

function updateComments(comments) {
    comments.forEach(comment => {
        const postId = comment.post_id;
        const commentId = `id_comment_div_${comment.id}`;
        let PostComments = document.getElementById(`comments_for_post_${postId}`);
        // check if comment already exists
        if (document.getElementById(commentId) === null) {
            PostComments.appendChild(makeCommentHTML(comment));
        }
    }) 
}


function makePostHTML(post) {
    let postDiv = document.createElement("div")
    postDiv.id = `id_post_div_${post.id}`
    postDiv.className = "post"
    
    // Create the profile link, text content, and datetime elements
    const profileLink = makeProfileLinkHTML(post, "post");
    const textContent = makeTextHTML(post, "post");
    const dateTime = makeDateTimeHTML(post, "post");

    // Create comment placeholder
    const commentPlaceholder = document.createElement("div");
    commentPlaceholder.id = `comments_for_post_${post.id}`;
    // Create comment input box
    const commentDiv = makeCommentBoxHTML(post);
    
    // Append elements in order
    postDiv.appendChild(document.createTextNode("Post by "));
    postDiv.appendChild(profileLink);
    postDiv.appendChild(document.createTextNode(" - "));
    postDiv.appendChild(textContent);
    postDiv.appendChild(document.createTextNode(" - "));
    postDiv.appendChild(dateTime);

    postDiv.appendChild(commentPlaceholder);

    postDiv.appendChild(commentDiv);

    return postDiv;
}

function makeCommentHTML(comment) {
    let commentDiv = document.createElement("div")
    commentDiv.id = `id_comment_div_${comment.id}`
    commentDiv.className = "comment"
    
    // Create the profile link, text content, and datetime elements
    const profileLink = makeProfileLinkHTML(comment, "comment");
    const textSpan = makeTextHTML(comment, "comment");
    const dateTime = makeDateTimeHTML(comment, "comment");
    
    commentDiv.appendChild(document.createTextNode("Comment by "));
    commentDiv.appendChild(profileLink);
    commentDiv.appendChild(document.createTextNode(" - "));
    commentDiv.appendChild(textSpan);
    commentDiv.appendChild(document.createTextNode(" - "));
    commentDiv.appendChild(dateTime);
    
    return commentDiv;
}

function makeTextHTML(item, type) {
    let textSpan = document.createElement("span")
    if (type === "post") {
        textSpan.id = `id_post_text_${item.id}`
    } else {
        textSpan.id = `id_comment_text_${item.id}`
    }
    textSpan.innerHTML = `${sanitize(item.text)}`
        return textSpan
}

function makeProfileLinkHTML(item, type) {
    let profileLink = document.createElement("a")
   
    if (type === "post") {
        profileLink.id = `id_post_profile_${item.id}`
    } else {
        profileLink.id = `id_comment_profile_${item.id}`
    }
    console.log(item.user_id)
    profileLink.href = getProfileURL(item.user_id)
    profileLink.innerHTML = `${item.first_name} ${item.last_name}`
    return profileLink
}

function makeDateTimeHTML(item, type) {
    let dateTime = new Date(item.creation_time)
    let date = dateTime.toLocaleDateString()
    let hour = dateTime.toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})

    let date_time = document.createElement("span")
    if (type === "post") {
        date_time.id = `id_post_date_time_${item.id}`
    } else {
        date_time.id = `id_comment_date_time_${item.id}`
    }
    date_time.innerHTML = `${date} ${hour}`
    return date_time
}

function makeCommentBoxHTML(post) {
    let commentBox = document.createElement("div");
    commentBox.id = `id_comment_box_for_post_${post.id}`;
    commentBox.className = "input-container";
    
    let label = document.createElement("label");
    label.htmlFor = `id_comment_input_text_${post.id}`;
    label.textContent = "Comment:";
    
    let input = document.createElement("input");
    input.type = "text";
    input.id = `id_comment_input_text_${post.id}`;
    
    let button = document.createElement("button");
    button.id = `id_comment_button_${post.id}`;
    button.textContent = "Submit";
    
    button.addEventListener("click", function() {
        submitComment(post.id);
    });
    
    commentBox.appendChild(label);
    commentBox.appendChild(input);
    commentBox.appendChild(button);
    
    return commentBox;
}

function submitComment(postId) {
    let commentTextElement = document.getElementById(`id_comment_input_text_${postId}`);
    let commentTextValue = commentTextElement.value;

    // Clear input box and old error message (if any)
    commentTextElement.value = "";

    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState !== 4) return
        updatePage(xhr)
    }

    xhr.open("POST", addCommentURL, true)
    // remember about the enctype for regular form-data
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    // now pass the request body (the payload here)
    xhr.send(`comment_text=${commentTextValue}&post_id=${postId}&csrfmiddlewaretoken=${getCSRFToken()}`)
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
}

function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown"
}
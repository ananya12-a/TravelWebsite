"use strict"

var page = "none";

var calendar_events = null;

// Sends a new request to update the post
function loadPage(trip_id) {
    console.log("--------loadingpage")
    //console.log("loadPost")
    let xhr = new XMLHttpRequest()
    console.log(xhr)
    xhr.onreadystatechange = function() {
        if (this.readyState !== 4) return;
        updatePage(xhr,trip_id);
    }
    // generates the response that's the parameter for the updatePost function

    xhr.open("POST", "travelwebsite/get-trips", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    
    // Prepare the data to be sent in the request
    // let data = "trip_id=" + encodeURIComponent(trip_id);
    
    xhr.send(`csrfmiddlewaretoken=${getCSRFToken()}&trip_id=${trip_id}`);
    return calendar_events;
}

function updatePage(xhr,trip_id) {
    console.log("--------updatePage")
    if (xhr.status === 200) {
        let response = JSON.parse(xhr.responseText)
        return updateItinerary(response,trip_id)
    }

    if (xhr.status === 0) {
        displayError("Cannot connect to server")
        return
    }


    if (!xhr.getResponseHeader('content-type') === 'application/json') {
        displayError(`Received status = ${xhr.status}`)
        return
    }

    /* let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    } */

    //displayError(response)
}

function displayError(message) {
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
}

function updateItinerary(items, trip_id) {
    console.log("--------AAAAAAAAAAAAAAAAAA updateItinerary")
    console.log("made it here")
    // it will be just one item i believe
    // items.id - should be from response correct trip id
    // should have all the information from get_trip (location, etc)
    console.log(items)

    let followerContainer = document.getElementById("trip_followers")
    while (followerContainer.hasChildNodes()) {
        followerContainer.firstChild.remove()
    }        
    followerContainer.innerHTML = listFollowers(items[0].people_followers)

    let budgetContainer = document.getElementById("budget")
    while (budgetContainer.hasChildNodes()) {
        budgetContainer.firstChild.remove()
    }        
    budgetContainer.innerHTML = `
    <div style="color: black; padding: 0 30px;">
        <h4 style="font-size: 26px; margin-bottom: 5px;">Budget:</h4>
        <p style="font-size: 18px; margin-top: 0;">$${items[0].cost}</p>
    </div>`

    //location
    let locationContainer = document.getElementById("location")
    while (locationContainer.hasChildNodes()) {
        locationContainer.firstChild.remove()
    }
    locationContainer.innerHTML = `
    <div style="color: black; padding: 0 30px;">
        <h4 style="font-size: 26px; margin-bottom: 5px;">Location:</h4>
        <p style="font-size: 18px; margin-top: 0;">${items[0].location}</p>
    </div>`

    //origin airport
    let originCont = document.getElementById("origin_airport")
    while (originCont.hasChildNodes()) {
        originCont.firstChild.remove()
    }
    originCont.innerHTML = `
    <div style="color: black; padding: 0 30px;">
        <h4 style="font-size: 26px; margin-bottom: 5px;">Origin Airport:</h4>
        <p style="font-size: 18px; margin-top: 0;">${items[0].origin_airport}</p>
    </div>`

    // destination airport
    let destCont = document.getElementById("dest_airport")
    while (destCont.hasChildNodes()) {
        destCont.firstChild.remove()
    }
    destCont.innerHTML = `
    <div style="color: black; padding: 0 30px;">
        <h4 style="font-size: 26px; margin-bottom: 5px;">Destination Airport:</h4>
        <p style="font-size: 18px; margin-top: 0;">${items[0].destination_airport}</p>
    </div>`

    // date stuff
    let startDateContainer = document.getElementById("start_date_cont")
    let endDateContainer = document.getElementById("end_date_cont")
    while (startDateContainer.hasChildNodes()) {
        startDateContainer.firstChild.remove()
    }
    while (endDateContainer.hasChildNodes()) {
        endDateContainer.firstChild.remove()
    }
    startDateContainer.innerHTML = `
    <div style="color: black; padding: 0 30px;">
        <h4 style="font-size: 26px; margin-bottom: 5px;">Start Date:</h4>
        <p style="font-size: 18px; margin-top: 0;">${items[0].start_date}</p>
    </div>`
    endDateContainer.innerHTML = `
    <div style="color: black; padding: 0 30px;">
        <h4 style="font-size: 26px; margin-bottom: 5px;">End Date:</h4>
        <p style="font-size: 18px; margin-top: 0;">${items[0].end_date}</p>
    </div>`

    // flights information
    let flightsContainer = document.getElementById("flights")
    while (flightsContainer.hasChildNodes()) {
        flightsContainer.firstChild.remove()
    }
    flightsContainer.innerHTML = `
    <div style="color: black; padding: 0 30px;">
        <h4 style="font-size: 26px; margin-bottom: 5px;">Flights:</h4>
        <p style="font-size: 18px; margin-top: 0;">${items[0].flights} <a href="${items[0].flights_url}" target="_blank">Check More Flights!</a></p>
    </div>`
    console.log("flight url", items[0])
    // show acttivities
    let itineraryContainer = document.getElementById("itinerary")
    while (itineraryContainer.hasChildNodes()) {
        itineraryContainer.firstChild.remove()
    }
    console.log("intin",items[0].itinerary)
    itineraryContainer.innerHTML = makeItinerary(items[0].itinerary)

    return makeCalendar(items)

    // let calendarContainer = document.getElementById("calendar")
    // let followersContainer = document.getElementById("followers")

    // while (calendarContainer.hasChildNodes()) {
    //     calendarContainer.firstChild.remove()
    // }
    // //calendarContainer.innerHTML = makeCalendar(items)

    // while (followersContainer.hasChildNodes()) {
    //     followersContainer.firstChild.remove()
    // }

    // // add activities
    //     let addActivityContainer = document.getElementById("add_activity")
    //     while (addActivityContainer.hasChildNodes()) {
    //         addActivityContainer.firstChild.remove()
    //     }
    
    // idk how to do this
    // gotta do another function

}

function makeCalendar(items) {
    console.log("--------BBBBBBBBBBBBB makeCalendar")
    var events = []
    events.push({
        title: "Departure Flight",
        start: items[0].start_date,
        backgroundColor: '#3788d8',
        borderColor: '#3788d8'
    })
    items[0].itinerary.forEach(item => {
        var event = {
            title: item.activity_type,
            start: item.date + 'T' + item.start_time, // Format: YYYY-MM-DDTHH:MM:SS
            end: item.date + 'T' + item.end_time, // Format: YYYY-MM-DDTHH:MM:SS
            backgroundColor: '#3788d8',
            borderColor: '#3788d8'
        };
        
        events.push(event)
    });
    events.push({
        title: "Arrival Flight",
        start: items[0].end_date,
        backgroundColor: '#3788d8',
        borderColor: '#3788d8'
    })
    calendar_events = events;
    return events
}

function listFollowers(followers) {
    console.log("--------CCCCCCCCCCCCCCCCCcc listFollowers")
    console.log("followers:", followers)
    let element = `<ol>`
    for (let i = 0; i < followers.length; i++) {
        element += `<li>${followers[i]}
                    </li>`
    }
    element += `</ol>`
    return element
}
function makeItinerary(itinerary) {
    console.log("--------DDDDDDDDDDD makeItinerary")
    console.log("make itin func")
    let element = `<p style="color: black; font-size: 23px;">Activities: </p>
    <ul>`
    // sort by date
    itinerary.sort((a, b) => {
        let dateA = new Date(a.date);
        let dateB = new Date(b.date);
        return dateA - dateB;
    });
    console.log("postsort", itinerary)

    let totcost = 0

    for (let i = 0; i < itinerary.length; i++) {
        element += `<li class="flex items-center justify-between">
                <span class="mr-4">${itinerary[i].date} (${itinerary[i].start_time} - ${itinerary[i].end_time}): ${itinerary[i].activity_type} ($${itinerary[i].cost})</span>
                <form action="delete_activity/${itinerary[i].id}" method="POST" class="inline-block">
                    <button type="submit" class="icon-button trash-icon" title="Delete">
                        <svg class="w-6 h-6 text-gray-800 dark:text-white icon-button trash-icon" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
                            <path fill-rule="evenodd" d="M8.586 2.586A2 2 0 0 1 10 2h4a2 2 0 0 1 2 2v2h3a1 1 0 1 1 0 2v12a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V8a1 1 0 0 1 0-2h3V4a2 2 0 0 1 .586-1.414ZM10 6h4V4h-4v2Zm1 4a1 1 0 1 0-2 0v8a1 1 0 1 0 2 0v-8Zm4 0a1 1 0 1 0-2 0v8a1 1 0 1 0 2 0v-8Z" clip-rule="evenodd"/>
                        </svg>
                    </button>
                    <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                </form>
            </li>`;

        totcost += parseInt(itinerary[i].cost)
    }
    element += `Total Cost Activities: $${totcost}</ul>`
    //updateItinerary(itinerary)
    return element
    //delete trip delete_activity/<int:activity_id

}


function deleteItem(id) {
    console.log("--------EEEEEEEEEEE deleteItem")
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState !== 4) return
        updatePage(xhr)
    }
    
    xhr.open("POST", deleteItemURL(id), true)
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xhr.send(`csrfmiddlewaretoken=${getCSRFToken()}`)
}

function makeElement(item) {
    console.log("--------FFFFFFFFFFFFFFF makeElement")
    // let deleteButton
    // if (item.user === myUserName) {
    //     deleteButton = `<button onclick='deleteItem(${item.id})'>X</button>`
    // } else {
    //     deleteButton = "<button style='visibility: hidden'>X</button> "
    // }

    // let details = `<span class="details">(id=${item.id}, ip_addr=${item.ip_addr}, user=${item.user})</span>`

    // let element = document.createElement("li")
    // element.innerHTML = `${deleteButton} ${sanitize(item.text)} ${details}`

    // return element


    // it will be under item.trip
    let element = document.createElement("div")

    let isoformat = item.creation_time;
    let date = new Date(isoformat);
    let formatdate = date.toLocaleDateString("en-US");
    let formattime = date.toLocaleTimeString("en-US", { hour: 'numeric', minute: 'numeric', hour12: true });

    if (item == None) {
        element.innerHTML = `<div>
            <div> Empty Calendar </div> need button to change all of this?
            <div> Empty Day Calendar </div>
            <div> Dates: None to None </div>
            <div> Followers: None </div>
            <div> Flights: None: </div>
            <div> Add Activity for Form Stuff
                <label>Add Activity:</label>
                <textarea id="activity_${item.id}"></textarea>
                <textarea id="date_${item.id}"></textarea>
                <textarea id="time_${item.id}"></textarea>
                <textarea id="duration_${item.id}"></textarea>
                <textarea id="cost_${item.id}"></textarea>
                <button type="submit" id="activity_button_${item.id}" onclick="makeActivity(${item.id})">Submit</button>
            </div>
        </div>`    
    }
    else {
        element.innerHTML = `<div>
            <div> Calendar Stuff </div>
            <div> Itinerary for chosend ay </div>
            <div> Dates </div>
            <div> Followers </div>
            <div> Flights </div>
            <div> Add Activity for Form Stuff
                <label>Add Activity:</label>
                <textarea id="activity_${item.id}"></textarea>
                <textarea id="date_${item.id}"></textarea>
                <textarea id="time_${item.id}"></textarea>
                <textarea id="duration_${item.id}"></textarea>
                <textarea id="cost_${item.id}"></textarea>
                <button type="submit" id="activity_button_${item.id}" onclick="makeActivity(${item.id})">Submit</button>
            </div>
        </div>`
    }


    // <div id="id_post_div_${item.id}">
    //         <p id="id_poster_${item.id}"> Post by <a id="id_post_profile_${item.id}" href="/dummy_profile/${item.user_id}">${sanitize(item.user_firstname)} ${sanitize(item.user_lastname)}</a>: </p>
    //         <p id="id_post_text_${item.id}"> ${item.text}</p>
    //         <p id="id_post_date_time_${item.id}"> ${formatdate} ${formattime} </p>
    //     </div>
    //     <div id="my-comments-go-here-for-post-${item.id}"> </div>
    //     <div>
    //         <label>Comment:</label>
    //         <textarea id="id_comment_input_text_${item.id}"></textarea>
    //         <button type="submit" id="id_comment_button_${item.id}" onclick="makeActivity(${item.id})">Submit</button>
    //     </div>
    // </div>`

    list.prepend(element)    
    

    
    // let commentContainer = document.getElementById("my-comments-go-here-for-post-" + item.id)
    // // while (commentContainer.hasChildNodes()) {
    // //     commentContainer.firstChild.remove()
    // // }
    // // Adds each to do list item received from the server to the displayed list
    // // items.forEach(item => comments.prepend(addComment(item.comments)))
    // console.log(item)
    // let comments = item.comments
    // // comments.forEach(comment => commentContainer.append(addComment(comment)))

    // comments.forEach(comment => {
    //     // Check if the item is already in the list
    //     if (!document.getElementById(`id_comment_div_${comment.id}`)) {
    //         commentContainer.append(addComment(comment));
    //     }
    // });

}

function makeActivity(id) {
    console.log("--------GGGGGGGGGGGGGGGG makeActivity")
    console.log("makeActivity called")
    // let itemTextElement = document.getElementById("id_comment_input_text_" + id)
    // let itemTextValue = itemTextElement.value

    let itemActivityElement = document.getElementById("activity_" + id)
    let itemActivityValue = itemActivityElement.value
    let itemDateElement = document.getElementById("date_" + id)
    let itemDateValue = itemDateElement.value
    let itemTimeElement = document.getElementById("time_" + id)
    let itemTimeValue = itemTimeElement.value
    let itemDurationElement = document.getElementById("duration_" + id)
    let itemDurationValue = itemDurationElement.value
    let itemCostElement = document.getElementById("cost_" + id)
    let itemCostValue = itemCostElement.value
        
    // Clear input box and old error message (if any)
    itemDateElement.value = ''
    itemTimeElement.value = ''
    itemDurationElement.value = ''
    itemCostElement.value = ''
    displayError('')

    activityObj = get_object_or_404(Activity, id=id)
    activity_type = activityObj.activity_type
    start_time = activityObj.start_time
    end_time = activityObj.end_time
    date = activityObj.date
    location = activityObj.location
    cost = activityObj.cost

    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState !== 4) return
        updatePage(xhr) 
        /* if (start_time > end_time) {
            displayError('Start time is greater than end time')
        } */
    }

    xhr.open("POST", "travelwebsite/add-activity", true)
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    // xhr.send(`comment_text=${itemTextValue}&postid=${id}&csrfmiddlewaretoken=${getCSRFToken()}`)
    // activity id how to get trip id to send
    xhr.send(`activity=${itemActivityValue}&date=${itemDateValue}&time=${itemTimeValue}&duration=${itemDurationValue}&cost=${itemCostValue}&trip_id=${id}&csrfmiddlewaretoken=${getCSRFToken()}`)
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

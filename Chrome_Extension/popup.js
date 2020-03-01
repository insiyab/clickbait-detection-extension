
document.addEventListener("DOMContentLoaded", () => {
	var searchForm = document.getElementById('searchForm');
	searchForm.addEventListener("submit", () => {
		var searchText = document.getElementById("searchText").value;
		chrome.runtime.sendMessage(
			{
				task: "activate-tool",
				queryText: searchText
			});
	}, false);
}, false);

function makeXhrRequest(method, url, token) {
	return new Promise((resolve, reject) => {
		let xhr = new XMLHttpRequest()
		xhr.open(method, url, true)
		xhr.setRequestHeader('Authorization', 'Bearer ' + token)
		xhr.onload = function(){
		if (xhr.status >= 200 && xhr.status < 300){
			return resolve(xhr.response);
		} else {
			reject(Error({
				status: xhr.status,
				statusTextInElse: xhr.statusText
			}));
		}
	}
	xhr.onerror = function(){
		reject(Error({
			status: xhr.status,
			statusText: xhr.statusText
		}))
	}
	xhr.send()
	})
}

function messageListener(request, sender, sendResponse) {
	let outputElement = document.getElementById("output_element");
	switch (request.task) {
		case "msg-to-popup":
			document.getElementById("output_element").innerText = request.msg;
			break;
		default:
			console.log("ERROR REQUEST TASK (FROM CONTENT SCRIPT)");
	}
}
chrome.runtime.onMessage.addListener(messageListener);




document.addEventListener("DOMContentLoaded", () => {
	console.log("Hey from popup");
	var searchForm = document.getElementById('searchForm');
	searchForm.addEventListener("submit", () => {
		var searchText = document.getElementById("searchText").value;
		chrome.runtime.sendMessage(
			{
				task: "initiate-tool",
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
		/*
			//makeXhrRequest("GET","http://127.0.0.1:5000/this",'');
			let req = new XMLHttpRequest();
			let obj = {
				'param1': "first param",
				'param2': "second param"
			}
			//req.open("GET","http://127.0.0.1:5000/this",true);
			req.open("POST","http://127.0.0.1:5000/this",true);
			req.onload = (arg) => {
				console.log(arg);
				console.log("you");
				document.getElementById("output_element");
			}
			//req.send("from popup script!");
			req.send("kelper helper");
			//chrome.runtime.getURL("http://127.0.0.1:5000/this");
			*/
			console.log("hey");

			break;
		default:
			console.log("ERROR REQUEST TASK (FROM CONTENT SCRIPT)");
	}
}
chrome.runtime.onMessage.addListener(messageListener);



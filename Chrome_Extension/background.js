let popupId;

function messageListener(request, sender, sendResponse) {
	switch (request.task) {
		case "open-popup":
			chrome.tabs.create(
				{
					url:"popup.html"
				},
				tab => {
					sendResponse({res: "hey!! !!"});
				});
			//chrome.tabs.remove(sender.tab.id);
			break;
		case "initiate-tool":
			chrome.tabs.query({active: true}, tabs => {
				let activeTab = tabs[0];
				chrome.tabs.sendMessage(
					activeTab.id,
					{
						task: "activate-tool"
					});
			});
			break;
		case "msg-to-popup":
			let req = new XMLHttpRequest();
			req.open("GET","http://127.0.0.1:5000/this",true);
			req.onload = (arg) => {
				console.log(arg);
				//document.getElementById("output_element");
			}
			req.send();
	
			chrome.tabs.sendMessage(
				{
					task: "incoming-msg",
					msg: request.msg
				});
			break;	
		case "send-for-late-reply":
			setTimeout(() => {
				chrome.tabs.query({}, tabs => {
					var lastId = tabs[tabs.length-1].id;
					chrome.tabs.sendMessage(
						lastId,
						{
							task: "another-delay-response"
						},
						response => {
							sendResponse({res: response.n});
						});
				});
			}, 2000);
			//sendResponse({res: "finally!"});
			return true;
			break;
		default:
			console.log("ERROR RECEIVING MESSAGE '"+request.task+"'");
			sendResponse({res: "ERROR WITH MESSAGE (FROM BACKGROUND)"});
			//chrome.runtime.onMessage.removeListener(messageListener);
	}
}
chrome.runtime.onMessage.addListener(messageListener);


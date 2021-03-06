let popupId;

function messageListener(request, sender, sendResponse) {
	switch (request.task) {
		case "open-url":
			chrome.tabs.create(
				{
					url: request.url,
					active: false
				},
				tab => {
					function updateListener(tabId, info) {
						 if (info.status == "complete") {
							 chrome.tabs.onUpdated.removeListener(updateListener);
							 let key = selectedArr[0][0];
								chrome.tabs.sendMessage(
									tab.id,
									{
										task: "get-video-metrics"
									},
									response => {
										sendResponse({videoTite: response.videoTitle});
			
									});
						 }
					 }
					 chrome.tabs.onUpdated.addListener(updateListener);
					return true;
				});
			//chrome.tabs.remove(sender.tab.id);
			return true;
			break;
		case "activate-tool":
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


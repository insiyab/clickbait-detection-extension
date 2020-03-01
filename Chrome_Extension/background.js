function messageListener(request, sender, sendResponse) {
	switch (request.task) {
		case "open-popup":
			break;
		case "remove-element":
			selectedElementsArr.splice(request.index,1);
			break;
		case "clear-selected-elements":
			selectedElementsArr = [];
			break;
		case "close-this-tab":
			chrome.tabs.remove(sender.tab.id);
			break;
		case "activate-tool":
			if (!toolWindow)
				chrome.windows.create(
					{
						url: "http://www.minemime.com",
						focused: false
					},
					window => {
						console.log(toolWindow = window);
						toolWindow.active = true;
					});
			break;
		case "deactivate-tool":
			if (toolWindow) {
				chrome.windows.remove(toolWindow.id);
				toolWindow = undefined;
			}
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
		case "create-tab--set-dom-state--click-element--search-for-text":
			chrome.tabs.create(
				{
					url: sender.tab.url, 
					active: false, 
					openerTabId: sender.tab.id
				},
				tab => {
					function updateListener(tabId, info) {
						if (info.status == "complete") {
							chrome.tabs.onUpdated.removeListener(updateListener);
							var key = request.localStorageKey;
							var queryText = request.textToSearch;
							chrome.tabs.sendMessage(
								tab.id,
								{
									task: "set-new-dom-state",
									localStorageKey: key
								},
								domSetResponse => {
									domSetResponseFunc(request, sendResponse, 
										domSetResponse, tab.id, key);
								});
						}
					}
					chrome.tabs.onUpdated.addListener(updateListener);
				});
			return true;
			break;
		case "initiate-query-text-search":
			chrome.tabs.query({active: true}, tabs => {
				// tabs should contain only the active tab when {active: true}
				var activeTab = tabs[0];
				clickAll(activeTab, request.queryText, selectedElementsArr);
				/*
				chrome.tabs.sendMessage(
					activeTab.id,
					{
						task: "click-selected-elements-then-search-for-query-text",
						textToSearchFor: request.queryText
					});
				*/
			});
			
			console.log("queryText: "+request.queryText);
			break;
		case "get-all-tabs-in-window":
			chrome.tabs.getAllInWindow(tabs => {
				for (var i=0; i<tabs.length; i++)
					console.log("id: "+tabs[i].id+" title: "+tabs[i].title);
				sendResponse({tabs: tabs});
			});
			//chrome.runtime.onMessage.removeListener(messageListener);
			return true;
			break;
		default:
			console.log("ERROR RECEIVING MESSAGE '"+request.task+"'");
			//chrome.runtime.onMessage.removeListener(messageListener);
	}
}
chrome.runtime.onMessage.addListener(messageListener);


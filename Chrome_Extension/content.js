// used for recording DOM mutations
let nextBirthmark = 0;
let targetElement = {style: {background: ''}};

function highlightElement(e) {
	var evt = e || window.event;

	if (evt.shiftKey) {
		E = e.target;

		// highlight (hold down shift)
		if (!evt.ctrlKey)
			if (E != targetElement) {
				targetElement.style.background = '';
				targetElement = E;
				E.style.background = "#FDFF47";
			} 

		// unhighlight (hold down shift + control)
		if (evt.ctrlKey)
			E.style.background = "";
	}
}

function clearHighlighted(selectedElements) {

	var arr = selectedElements;
	for (var i=0; i<arr.length; i++) {
		arr[i][0].style.background = "";
	}
	chrome.runtime.sendMessage(
		{
			task: "clear-selected-elements"
		});
	return [];
}

function mark(unmarkedNodes) {
	var unmarkedNodes = document.querySelectorAll(":not([birthmark])");
	for (var i=0; i<unmarkedNodes.length; i++)
		unmarkedNodes[i].setAttribute("birthmark",(nextBirthmark += 1).toString(16));
}

function viewMutations(mutationList, observer) {
	// if there exists any elements that do not have a 'birthmark' attribute
	if ((unmarked = document.querySelectorAll(":not([birthmark])")).length > 0)
		mark(unmarked);
}

function messageListener(request, sender, sendResponse) {
	/*
	switch (request.task) {
	}
	*/
}
chrome.runtime.onMessage.addListener(messageListener);

function clickYouTubeElement(element) {

	chrome.runtime.sendMessage(
		{
			task: "click"
			//nodeToClick: nodeBirthmark
		},
		response => {
			/*
			localStorage.removeItem(nodeBirthmark);
			if (response.contains)
				console.log("\""+queryText+"\" exists in tab "+response.tabId);
			else
				console.log("\""+queryText+"\" dne in tab "+response.tabId);
			*/
		});
}

document.addEventListener(
	"keydown", 
	e => {
	
		var evt = e || window.event;
	
		// press shift + 's' keys to activate selection tool
		if (evt.shiftKey && evt.which === 83 && !evt.altKey)
			document.addEventListener("mousemove", highlightElement, false);
	
		// press shiftKey + altKey + 's' keys to disable selection tool
		if (evt.shiftKey && evt.altKey && evt.which === 83)
			document.removeEventListener("mousemove", highlightElement, false);
	
		// press shift + ctrl + enter to click all the selected elements
		if (evt.shiftKey && evt.ctrlKey && evt.which === 13) 
			for (var i=0; i<1000; i++)
				chrome.runtime.sendMessage(
					{
						task: "open-popup"
					},
					response => {console.log(response.res);});
	
		// press ctrl + 'r' keys to activate/execute video check tool
		if (evt.ctrlKey && evt.which == 82)
			clickYouTubeElement(targetElement);
	
	}, false);

window.addEventListener("DOMContentLoaded", e => {

	var targetNode = document.getElementsByTagName("HTML")[0];
	var observerOptions = {
		childList: true,
		attributes: true,
		subtree: true
	}

	var observer = new MutationObserver(viewMutations);
	observer.observe(targetNode, observerOptions);
}, false);

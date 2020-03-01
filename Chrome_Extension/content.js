// used for recording DOM mutations
let nextBirthmark = 0;
let targetElement = {style: {background: ''}};
let n = 0;

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
				sendMsg("msg-to-popup",E.tagName);
				console.log(E);
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

function sendMsg(task, msg) {

	chrome.runtime.sendMessage(
		{
			task: task,
			msg: msg
			//nodeToClick: nodeBirthmark
		});
}

function messageListener(request, sender, sendResponse) {
	switch (request.task) {
		case "activate-tool":
			document.addEventListener("mousemove", highlightElement, false);
			break;
		case "deactivate-tool":
			document.removeEventListener("mousemove", highlightElement, false);
			break;
		default:
			console.log("ERROR REQUEST TASK (FROM CONTENT SCRIPT)");
	}
}
chrome.runtime.onMessage.addListener(messageListener);



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

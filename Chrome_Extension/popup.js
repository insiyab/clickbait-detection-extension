document.addEventListener("DOMContentLoaded", () => {
	var searchForm = document.getElementById('searchForm');
	searchForm.addEventListener("submit", () => {
		var searchText = document.getElementById("searchText").value;
		chrome.runtime.sendMessage(
			{
				task: "initiate-query-text-search",
				queryText: searchText
			});
	}, false);
}, false);



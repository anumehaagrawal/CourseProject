
  function getCurrentTabUrl() {
    var queryInfo = {
      active: true,
      currentWindow: true,
    }
  
    chrome.tabs.query(queryInfo, function(tabs) {
        alert("Hello");
    })
  }
  
  document.querySelector('#checkPage').addEventListener('click', getCurrentTabUrl)
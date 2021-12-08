document.addEventListener('DOMContentLoaded', function() {
  var taburl = "";
  chrome.tabs.query({
    active: true,
    currentWindow: true
  }, function(tabs) {
    var tab = tabs[0];
    taburl = tab.url;
  });
  document.querySelector('#checkPage').addEventListener('click', function() {
    chrome.runtime.sendMessage('get-topStocks', (response) => {
      document.querySelector('#topStocks').innerHTML = response;
    });
    chrome.runtime.sendMessage('get-stockNews', (response) => {
      document.querySelector('#stockNews').innerHTML = response;
    });
    chrome.runtime.sendMessage('get-visualize', (response) => {
      document.querySelector('#visualize').innerHTML = response;
      document.getElementById('graph').style.display='block';

    });
    chrome.runtime.sendMessage('get-visualize1', (response) => {
      document.querySelector('#visualize1').innerHTML = response;
      document.getElementById('graph1').style.display='block';
    });
    chrome.runtime.sendMessage(taburl, (response) => {
      document.querySelector('#specificStock').innerHTML = response;
    });

  }, false);
}, false);

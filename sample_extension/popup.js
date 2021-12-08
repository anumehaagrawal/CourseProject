
// function getCurrentTabUrl() {
//   // var queryInfo = {
//   //   active: true,
//   //   currentWindow: true,
//   // }

//   // chrome.tabs.query(queryInfo, function(tabs) {
//   //     alert("Hello");
//   // })
//   chrome.runtime.sendMessage(
//     function (response) {
//       result = response.topStocks;
//       alert(result.summary);
//     })
// }

// document.querySelector('#checkPage').addEventListener('click', getCurrentTabUrl)


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
      // 3. Got an asynchronous response with the data from the background
      document.querySelector('#topStocks').innerHTML = response;
    });
    chrome.runtime.sendMessage('get-stockNews', (response) => {
      // 3. Got an asynchronous response with the data from the background
      document.querySelector('#stockNews').innerHTML = response;
    });
    chrome.runtime.sendMessage('get-visualize', (response) => {
      // 3. Got an asynchronous response with the data from the background
      document.querySelector('#visualize').innerHTML = response;
      document.getElementById('graph').style.display='block';
      // document.getElementById('graph').style.display='block';

    });
    chrome.runtime.sendMessage('get-visualize1', (response) => {
      // 3. Got an asynchronous response with the data from the background
      document.querySelector('#visualize1').innerHTML = response;
      document.getElementById('graph1').style.display='block';
      // document.getElementById('graph1').style.display='block';
    });
    chrome.runtime.sendMessage(taburl, (response) => {
      // 3. Got an asynchronous response with the data from the background
      document.querySelector('#specificStock').innerHTML = response;
    });
    // chrome.runtime.sendMessage(taburl_sentiment, (response) => {
    //   // 3. Got an asynchronous response with the data from the background
    //   document.querySelector('#sentiment').innerHTML = response;
    // });
  }, false);
}, false);

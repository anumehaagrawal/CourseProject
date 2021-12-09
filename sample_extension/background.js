
var serverhost = 'http://127.0.0.1:5000';

chrome.runtime.onMessage.addListener(
    function (obj, sender, sendResponse) {
        if(obj == "get-topStocks") {
            var url = serverhost + '/_top_stocks/';
            console.log(url);
            fetch(url)
                .then(response => response.text())
                .then(response => sendResponse(response))
                .catch()
        }
        else if(obj == "get-stockNews") {
            var url = serverhost + '/_top_stocks_news/';
            console.log(url);
            fetch(url)
                .then(response => response.text())
                .then(response => sendResponse(response))
                .catch()
        }
        else if(obj == "get-visualize") {
            var url = serverhost + '/visualize/';
            console.log(url);
            fetch(url)
                .then(response => response.text())
                .then(response => sendResponse(response))
                .catch()
        }
        else if(obj == "get-visualize1") {
            var url = serverhost + '/visualize1/';
            console.log(url);
            fetch(url)
                .then(response => response.text())
                .then(response => sendResponse(response))
                .catch()
        }
        else{
            var tabUrl = obj;
            var url = serverhost + '/stock?url=' + tabUrl;
            fetch(url)
                .then(response => response.text())
                .then(response => sendResponse(response))
                .catch()
        }
        return true;
});

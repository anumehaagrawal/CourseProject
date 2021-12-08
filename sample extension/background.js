
var serverhost = 'http://127.0.0.1:5000';

// .then(response => sendResponse({topStocks: response}))

chrome.runtime.onMessage.addListener(

    function (obj, sender, sendResponse) {
        if(obj == "get-topStocks") {
            var url = serverhost + '/_top_stocks/';

            console.log(url);

            //var url = "http://127.0.0.1:8000/wiki/get_wiki_summary/?topic=%22COVID19%22"
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

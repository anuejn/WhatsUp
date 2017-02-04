/**
 * Created by jaro on 13.11.16.
 */
var host = document.location.host.indexOf(":") != -1 ? "http://localhost" : "";

function mongo_query(map, reduce, callback, query) {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            callback(JSON.parse(this.responseText));
        }
    };

    var requestUrl = host + "/api";
    requestUrl += "?map=" + encodeURIComponent(map.toString());
    requestUrl += "&reduce=" + encodeURIComponent(reduce.toString());
    if(query && (typeof query === 'string' || query instanceof String)) {
        requestUrl += "&query=" + encodeURIComponent(query.toString());
    } else if(typeof(query) === "boolean"){
        requestUrl += "&query";
    }

    request.open("GET", requestUrl, true);
    request.send();
}

function example_map() {
    emit("count", 1);
}

function example_reduce(key, values) {
    return values.reduce((previousValue, currentValue) => currentValue + previousValue);
} 
var count = example_reduce;

/**
 * Created by jaro on 13.11.16.
 */

function mongo_query(map, reduce, callback) {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            callback(JSON.parse(this.responseText));
        }
    };

    var requestUrl = "/api";
    requestUrl += "?map=" + encodeURIComponent(map.toString());
    requestUrl += "&reduce=" + encodeURIComponent(reduce.toString());

    request.open("GET", requestUrl, true);
    request.send();
}

function example_map() {
    emit("count", 1)
}

function example_reduce(key, values) {
    var total = 0;
    for (var i = 0; i < values.length; i++) {
        total += values[i];
    }
    return total;
}
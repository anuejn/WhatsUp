/**
 * Created by jaro on 13.11.16.
 */

class Request {
    constructor(baseUrl, mapFunction, reduceFunction) {
        this.requestUrl = baseUrl + "?map=" + encodeURIComponent(mapFunction) + "&reduce" + encodeURIComponent(reduceFunction);
        console.log(this.requestUrl);
    }

    getResult(callbackFunction) {
        data = [];
        callbackFunction(data);
    }
}
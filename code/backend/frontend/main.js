$(() => {
    //initialize the connection
    $.couch.urlPrefix = "http://admin:cOuChDb!1!@neindev.tk:5984";
    $.couch.login({
        name: "admin",
        password: "cOuChDb!1!",
        success: function(data) {
            console.log(data);
            console.log($.couch.session())
        },
        error: function(status) {
            console.log(status);
        }
    });

    var db = $.couch.db("news");

    //do a test query
    var mapFunction = function (doc) {
        emit();
    };

    db.query(mapFunction, "_count", "javascript", {
        success: function (data) {
            console.log(data);
        },
        error: function (status) {
            console.log(status);
        },
        reduce: false
    });
});

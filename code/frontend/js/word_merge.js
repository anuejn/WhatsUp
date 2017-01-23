/**
 * Created by jaro on 22.12.16.
 */

function word_merge(list) {
    modList = list.slice();
    modList.forEach((nowItem, nowCount, nowObject) => {
        var regex = new RegExp("^" + nowItem["_id"] + '.{0,2}','g');
        nowObject.forEach((item, index, object) => {
            if(nowItem["_id"] == item["_id"]) return;
            if(nowItem["_id"].length < 4) return;
            checkWord = item["_id"];
            if(checkWord.match(regex)) {
                nowObject[nowCount]["value"] += item["value"];
                object.splice(index, 1);
            }
        });
    });
    return modList
}

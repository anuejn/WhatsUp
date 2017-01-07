/**
 * Created by jaro on 22.12.16.
 */

function word_merge(list) {
    modList = list.slice();
    modList.forEach((nowItem, nowCount, nowObject) => {
        var regex = new RegExp("^" + nowItem["_id"].toLowerCase() + '.{0,2}','g');
        nowObject.forEach((item, index, object) => {
            if(nowItem["_id"].toLowerCase() == item["_id"].toLowerCase()) return;
            checkWord = item["_id"].toLowerCase();
            if(checkWord.match(regex)) {
                nowObject[nowCount]["value"] += item["value"];
                object.splice(index, 1);
            }
        });
    });
    return modList
}
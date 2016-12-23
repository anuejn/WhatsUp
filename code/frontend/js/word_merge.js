/**
 * Created by jaro on 22.12.16.
 */

function word_merge(list) {
    list.forEach((nowItem, nowCount, nowObject) => {
        nowWord = nowItem["_id"].toLowerCase();
        nowObject.forEach((item, index, object) => {
            checkWord = item["_id"].toLowerCase();
            var regex = new RegExp(nowWord + '.{0,2}','g');
            if(checkWord.match(regex)) {
                nowObject[nowCount]["value"] += item["value"];
                object.splice(index, 1);
            }
        });
    });
}
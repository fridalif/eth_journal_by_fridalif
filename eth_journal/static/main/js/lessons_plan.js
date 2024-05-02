function get_lessons_from_date(date){
    let xhr = new XMLHttpRequest();
    xhr.open("GET","/api/lessons/?date="+date);
    xhr.responseType = 'json';
    xhr.send();
    xhr.onload = function(){
        result = xhr.response;
        alert(result);
        return;
    }
    return;
}

function get_previous_day_lesson(day,month,year){
    current_date = new Date(year,month-1,day);
    alert(current_date.toString());
}

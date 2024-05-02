function get_lessons_from_date(date){
    let xhr = new XMLHttpRequest();
    xhr.open("GET","/api/lessons/?date="+date.getFullYear()+'-'+(date.getMonth()+1)+'-'+date.getDate());
    xhr.responseType = 'json';
    xhr.send();
    xhr.onload = function(){
        result = xhr.response;
        side_bar_block = document.getElementById('marks_side_bar_content_block')
        side_bar_block.innerHTML = ''
        for (let i = 0; i < result.length; i++) {
             result_info = result[i]['subject_name']
             side_bar_block.innerHTML += '<div class="marks_side_bar_lesson_block"><div class="marks_side_bar_font">'+result_info+'</div></div>';
        }
        return;
    }
    return;
}

function get_previous_day_lesson(date){
    var day = date.getDate() - 1;
    date.setDate(day);
    get_lessons_from_date(date);
    date_representation_block = document.getElementById('date_representation_block');
    date_representation_block.innerHTML = date.getDate()+'.'+(date.getMonth()+1)+'.'+date.getFullYear();
}

function get_next_day_lesson(date){
    var day = date.getDate() + 1;
    date.setDate(day);
    get_lessons_from_date(date);
    date_representation_block = document.getElementById('date_representation_block');
    date_representation_block.innerHTML = date.getDate()+'.'+(date.getMonth()+1)+'.'+date.getFullYear();
}

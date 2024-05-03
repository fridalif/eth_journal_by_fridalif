function get_lessons_from_date(date){
    prev_chosen_id =0;
    let xhr = new XMLHttpRequest();
    xhr.open("GET","/api/lessons/?date="+date.getFullYear()+'-'+(date.getMonth()+1)+'-'+date.getDate());
    xhr.responseType = 'json';
    xhr.send();
    xhr.onload = function(){
        result = xhr.response;
        side_bar_block = document.getElementById('marks_side_bar_content_block')
        side_bar_block.innerHTML = ''
        for (let i = 0; i < result.length; i++) {
             result_info = result[i]['subject_name'];
             result_info += '(Кабинет: ' + result[i]['room']+', Тип: '+result[i]['type'];//+ 'Преподаватель:';
             result_info +=', Начало: '+result[i]['start_time']+', Окончание: '+result[i]['end_time']+'';
             teacher_info = ', Преподаватель: ';
             if (result[i]['abstract_teacher_name']!=null){
                teacher_info += result[i]['abstract_teacher_surname']+' '+result[i]['abstract_teacher_name']+' '+result[i]['abstract_teacher_father_name'];
             }
            else{
                teacher_info += result[i]['teacher_surname']+' '+result[i]['teacher_name']+' '+result[i]['teacher_father_name'];
            }
            group_info = ', Группа: '+result[i]['group_year_of_study']+result[i]['group_letter'];
            result_info+=teacher_info+group_info+')';
            side_bar_block.innerHTML += '<div id="marks_side_bar_lesson_block_'+String(result[i]['id'])+'" class="marks_side_bar_lesson_block" onclick="get_lesson_marks_from_id('+result[i]['id']+');">'+'<div class="marks_side_bar_font">'+result_info+'</div></div>';
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

function get_lesson_marks_from_id(lesson_id){
    if (prev_chosen_id > 0){
        prev_chosen_div = document.getElementById('marks_side_bar_lesson_block_'+String(prev_chosen_id));
        prev_chosen_div.className = 'marks_side_bar_lesson_block';
    }
    lesson_div = document.getElementById('marks_side_bar_lesson_block_'+String(lesson_id));
    lesson_div.className = 'marks_side_bar_lesson_block_choosen';
    prev_chosen_id = lesson_id;

    let xhr = new XMLHttpRequest();
    xhr.open("GET","/api/lessons/?date="+date.getFullYear()+'-'+(date.getMonth()+1)+'-'+date.getDate());
    xhr.responseType = 'json';
    xhr.send();
    xhr.onload = function(){
        result = xhr.response;
    }
}
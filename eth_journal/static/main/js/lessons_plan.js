function get_lessons_from_date(date){
    prev_chosen_id =0;
    let xhr = new XMLHttpRequest();
    xhr.open("GET","/api/lessons/?date="+date.getFullYear()+'-'+(date.getMonth()+1)+'-'+date.getDate());
    xhr.responseType = 'json';
    xhr.send();
    xhr.onload = function(){
        result = xhr.response;
        side_bar_block = document.getElementById('marks_side_bar_content_block');
        side_bar_block.innerHTML = '';
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
    return;
}

function get_next_day_lesson(date){
    var day = date.getDate() + 1;
    date.setDate(day);
    get_lessons_from_date(date);
    date_representation_block = document.getElementById('date_representation_block');
    date_representation_block.innerHTML = date.getDate()+'.'+(date.getMonth()+1)+'.'+date.getFullYear();
    return;
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
    xhr.open("GET","/api/lesson_student_info/"+String(lesson_id)+"/");
    xhr.responseType = 'json';
    xhr.send();
    marks_array = ['','2','3','4','5','Н','УП'];
    xhr.onload = function(){
        result = xhr.response;
        table_block = document.getElementById('marks_content_block');
        table_block.innerHTML = '';
        table_block.innerHTML = '<div class="marks_table_header_block"><div class="marks_table_header_font">Введите оценки:</div></div><div class="marks_table_row_header"><div class="marks_table_header_name_cell"><div class="marks_table_name_font">ФИО</div></div><div class="marks_table_header_mark_cell"><div class="marks_table_marks_font">Оценка</div></div><div class="marks_table_header_pluses_cell"><div class="marks_table_pluses_font">Особые заслуги</div></div><div class="marks_table_header_minuses_cell"><div class="marks_table_minuses_font">Замечание</div></div></div>';
        row_data = '<div class="marks_table_block" id="marks_table_block">'

        for (let i=0; i<result.length;i++){
            row_data += '<div class="marks_table_row" id="'+result[i]['id']+'">';
            if (result[i]['student_name']!=null){
                row_data += '<div class="marks_table_name_cell">'+result[i]['student_surname']+' '+result[i]['student_name']+' '+result[i]['student_father_name']+'</div>';
            }
            else{
                row_data += '<div class="marks_table_name_cell">'+result[i]['abstract_student_surname']+' '+result[i]['abstract_student_name']+' '+result[i]['abstract_student_father_name']+'</div>';
            }
            row_data += '<div class="marks_table_mark_cell">'
            if (!is_teacher){
                row_data += "<div class='white_table_font'>"+result[i]['mark']+'</div></div>';
            }
            else{
                row_data +="<select id='choose_mark' name='mark' class='choose_mark'>";
                for (let j=0; j<marks_array.length; j++){
                    row_data+='<option value="'+marks_array[j]+'"';
                    if (result[i]['mark'] == marks_array[j]){
                        row_data+='selected';
                    }
                    row_data+='>'+marks_array[j]+'</option>';
                }
                row_data += "</select></div>";
            }
            if (!is_teacher){
                row_data+='<div class="marks_table_pluses_cell"><div class="white_table_font">'+result[i]['commendation']+'</div></div>'
                row_data += '<div class="marks_table_minuses_cell"><div class="white_table_font">'+result[i]['chastisement']+'</div></div>'
            }
            else{
                row_data += '<div class="marks_table_pluses_cell"><input type="text" class="pluses_input" name="pluses_input" id="pluses_input" value="'+result[i]['commendation']+'"></div>'
                row_data += '<div class="marks_table_minuses_cell"><input type="text" class="minuses_input" name="minuses_input" id="minuses_input" value="'+result[i]['chastisement']+'"></div>'
            }

            row_data += '</div>';
        }
        submit_button = '';
        if (is_teacher){
            submit_button = '<input placeholder="Домашнее задание..." type="textarea" name="homework" id="homework_block"';
            if (result.length!=0){
                if (result[0]['homework']!=''){
                    submit_button += ' value="'+result[0]['homework']+'"';
                }
                submit_button += '><div class="submit_button_table" onclick="send_changes('+lesson_id+');">Подтвердить изменения</div>';
            }
        }
        else{
            submit_button = '<input placeholder="Домашнее задание..." type="textarea" name="homework" id="homework_block"';
            if (result.length!=0){
                if (result[0]['homework']!=''){
                    submit_button += ' value="'+result[0]['homework']+'"';
                }
                submit_button += ' readonly>';
            }
        }
        table_block.innerHTML +=row_data+'</div>'+submit_button;
        return;
    }
    return;
}


function send_changes(lesson_id){
    table_rows = document.getElementsByClassName('marks_table_row');
    for (let row_iter=0;row_iter<table_rows.length;row_iter++){
        lesson_info_id = table_rows[row_iter].id;
        mark = table_rows[row_iter].getElementsByClassName('choose_mark')[0].value;
        commendation = table_rows[row_iter].getElementsByClassName('pluses_input')[0].value;
        chastisement = table_rows[row_iter].getElementsByClassName('minuses_input')[0].value;
        let xhr = new XMLHttpRequest();
        let request_data = JSON.stringify({"id": lesson_info_id,"mark":mark,"commendation":commendation,"chastisement":chastisement });
        xhr.open("PUT","/api/lesson_student_info/"+String(lesson_id)+"/");
        xhr.setRequestHeader('X-CSRFToken',document.getElementsByName("csrfmiddlewaretoken")[0].value);
        xhr.setRequestHeader('Content-Type','application/json');
        xhr.responseType = 'json';
        xhr.send(request_data);
        console.log(row_iter);
        xhr.onload = function(){
            result = xhr.response;
            if (result['error']){
                alert(result['error']);
            }
            return;
        }
    }
    homework = document.getElementById('homework_block').value;
    let xhr = new XMLHttpRequest();
    let request_data = JSON.stringify({"homework": homework });
    xhr.open("PUT","/api/lessons/"+String(lesson_id)+"/");
    xhr.setRequestHeader('X-CSRFToken',document.getElementsByName("csrfmiddlewaretoken")[0].value);
    xhr.setRequestHeader('Content-Type','application/json');
    xhr.responseType = 'json';
    xhr.send(request_data);
    xhr.onload = function(){
        result = xhr.response;
        if (result['error']){
            alert(result['error']);
        }
        return;
    }
    alert('Успешно!');
    return;
}
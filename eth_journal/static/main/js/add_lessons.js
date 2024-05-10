function create_new_subject(){
    subject_name = document.getElementById('subject_name').value;
    let xhr = new XMLHttpRequest();
    let request_data = JSON.stringify({"subject_name":subject_name});
    xhr.open("POST","/api/subjects/");
    xhr.setRequestHeader('X-CSRFToken',document.getElementsByName("csrfmiddlewaretoken")[0].value);
    xhr.setRequestHeader('Content-Type','application/json');
    xhr.responseType = 'json';
    xhr.send(request_data);

    xhr.onload = function(){
        result = xhr.response;
        if(result["error"]){
            alert(result["error"]);
            return;
        }
        table = document.getElementById('add_subject_table_block');
        table.innerHTML = '<div class="add_subject_row">'+result['subject_name']+'</div>'+table.innerHTML;
        subjects[subjects_counter] = {"subject_id":String(result["id"]),"subject_name":result['subject_name']};
        subjects_counter++;
    }
}

function add_subject_init(){
    side_bar_subject = document.getElementById('subject_creating');
    side_bar_lesson = document.getElementById('lesson_creating');
    side_bar_subject.className='marks_side_bar_lesson_block_choosen';
    side_bar_lesson.className = 'marks_side_bar_lesson_block';
    main_block = document.getElementById('main_add');
    main_block.innerHTML = '';
    main_block.innerHTML = '<div class="add_subject_subject_label">Название предмета:</div><input id="subject_name" name="subject_name" type="text" class="add_subject_subject_input"><div class="add_subject_subject_submit" onclick="create_new_subject();"><div class="add_subject_subject_submit_font">Добавить</div></div><div class="add_subject_table_block_header">Существующие предметы:</div>';
    subject_table = '<div class="add_subject_table_block" id="add_subject_table_block">';
    for(let i=0;i<subjects.length;i++){
        row = '<div class="add_subject_row">'+subjects[i]['subject_name']+"</div>";
        subject_table+=row;
    }
    subject_table+='</div>';
    main_block.innerHTML+=subject_table;
}

function add_lesson_init(){
    side_bar_subject = document.getElementById('subject_creating');
    side_bar_lesson = document.getElementById('lesson_creating');
    side_bar_subject.className='marks_side_bar_lesson_block';
    side_bar_lesson.className = 'marks_side_bar_lesson_block_choosen';
    main_block = document.getElementById('main_add');
    main_block.innerHTML = '';
    main_block.innerHTML = '<div class="add_subject_table_block_header">Существующие уроки:</div>';
    select_subject = '<select id="subject_input" class="add_lesson_subject_select">';
    select_subject += '<option value="-1" selected>Предмет</option>';
    for(let i=0;i<subjects.length;i++){
        select_subject += '<option value="'+subjects[i]['subject_id']+'">'+subjects[i]['subject_name']+"</option>";
    }
    select_subject +='</select>';
    main_block.innerHTML+=select_subject;
    select_group ='<select id="group_input" class="add_lesson_group_select">';
    select_group += '<option value="-1" selected>Группа</option>';
    for(let i=0;i<groups.length;i++){
        select_group += '<option value="'+groups[i]['group_id']+'">'+groups[i]['group_name']+'</option>';
    }
    select_group+='</select>';
    main_block.innerHTML+=select_group;
    input_date = '<input type="date" id="date_input" class="add_lesson_date_input">';
    main_block.innerHTML+=input_date;
    select_time_area = '<select id="time_input" class="add_lesson_time_select">';
    select_time_area += '<option value="-1" selected>Временной промежуток</option>';
    for(let i=0; i<time_areas.length;i++){
        select_time_area += '<option value="'+String(i)+'">'+time_areas[i][0]+'-'+time_areas[i][1]+'</option>';
    }
    select_time_area += '</select>';
    main_block.innerHTML+=select_time_area;
    main_block.innerHTML+='<input type="text" id="room_input" class="add_lesson_room_input" placeholder="Кабинет">';
    main_block.innerHTML+='<input type="text" id="type_input" class="add_lesson_type_input" placeholder="Тип занятия">';
    main_block.innerHTML+='<div class="add_lesson_submit" onclick="create_new_lesson();">Добавить</div>';


    add_lesson_table = '<div class="add_subject_table_block" id="add_lesson_table_block">';
    add_lesson_table += '<div class="add_subject_header_row">';
    add_lesson_table += '<div class="add_lesson_subject_cell">Предмет</div>';
    add_lesson_table += '<div class="add_lesson_group_cell">Группа</div>';
    add_lesson_table += '<div class="add_lesson_date_cell">Дата</div>';
    add_lesson_table += '<div class="add_lesson_start_time_cell">Начало</div>';
    add_lesson_table += '<div class="add_lesson_end_time_cell">Оконочание</div>';
    add_lesson_table += '<div class="add_lesson_room_cell">Кабинет</div>';
    add_lesson_table += '<div class="add_lesson_type_cell">Тип занятия</div>';
    add_lesson_table += '</div>'
    for (let i=0;i<my_lessons.length;i++){
        row = '<div class="add_subject_row">';
        row += '<div class="add_lesson_subject_cell">'+my_lessons[i]['subject_name']+'</div>';
        row += '<div class="add_lesson_group_cell">'+my_lessons[i]['group_name']+'</div>';
        let date = new Date(my_lessons[i]['date'])
        row += '<div class="add_lesson_date_cell">'+String(date.getDate())+'.'+String(date.getMonth()+1)+'.'+String(date.getFullYear())+'</div>';
        let start_time = my_lessons[i]['start_time']
        let day_period = start_time.split(' ')[1]
        let time = start_time.split(' ')[0]

        let hours = parseInt(time.split(':')[0])
        if(day_period=='p.m.'){
            hours+=12;
        }
        if(hours == null){
            hours = '00';
        }
        let minutes = time.split(':')[1]
        if(minutes == null){
            minutes = '00';
        }
        row += '<div class="add_lesson_start_time_cell">'+hours+':'+minutes+'</div>';
        let end_end_time = my_lessons[i]['end_time']
        let end_day_period = end_end_time.split(' ')[1]
        let end_time = end_end_time.split(' ')[0]
        let end_hours = parseInt(end_time.split(':')[0])
        if(end_day_period=='p.m.'){
            end_hours+=12;
        }
        if(end_hours == null){
            end_hours = '00';
        }
        let end_minutes = end_time.split(':')[1]
        if(end_minutes == null){
            end_minutes = '00';
        }
        row += '<div class="add_lesson_end_time_cell">'+end_hours+':'+end_minutes+'</div>';
        row += '<div class="add_lesson_room_cell">'+my_lessons[i]['room']+'</div>';
        row += '<div class="add_lesson_type_cell">'+my_lessons[i]['type']+'</div>';
        row+='</div>';
        add_lesson_table+=row;
    }
    add_lesson_table +='</div>';
    main_block.innerHTML+=add_lesson_table;
    return;
}


function create_new_lesson(){
    subject = document.getElementById('subject_input').value;
    group = document.getElementById('group_input').value;
    date = document.getElementById('date_input').value;
    time = document.getElementById('time_input').value;
    room = document.getElementById('room_input').value;
    type = document.getElementById('type_input').value;
    if(subject == '-1'||group == '-1'||date==''||time=='-1'||room==''||type==''){
        alert('Заполните все поля!');
    }
    let xhr = new XMLHttpRequest();
    let request_data = JSON.stringify({"subject":subject,"group":group,"date":date,"start_time":time_areas[time][0],
                                       "end_time":time_areas[time][1],'room':room,'type':type});
    xhr.open("POST","/api/lessons/");
    xhr.setRequestHeader('X-CSRFToken',document.getElementsByName("csrfmiddlewaretoken")[0].value);
    xhr.setRequestHeader('Content-Type','application/json');
    xhr.responseType = 'json';
    xhr.send(request_data);

    xhr.onload = function(){
        result = xhr.response;
        if(result["error"]){
            alert(result["error"]);
            return;
        }
        console.log(result);
    }

}
function get_all_votes_stat(){
    marks_all_button = document.getElementsByClassName('table_header_change_pass_button')[0];
    marks_group_button = document.getElementsByClassName('table_header_group_stat_button');
    if(marks_group_button.length!=0){
        marks_group_button = marks_group_button[0];
    }
    else{
        marks_group_button = null;
    }
    votes_all_button = document.getElementsByClassName('table_header_register_button')[0];
    votes_all_button.id = 'table_header_register_chosen_button';
    if(marks_group_button!=null){
        marks_group_button.id = 'table_header_group_stat_button';
    }
    marks_all_button.id = 'table_header_change_pass_button';
    table = document.getElementById('admin_table_block');
    table.innerHTML = '';
    header_row  = '<div class="admin_table_row_header">';
    header_row += '<div class="stat_table_number">№</div>';
    header_row += '<div class="stat_table_register_username_cell">Логин</div>';
    header_row += '<div class="stat_table_register_name_cell">ФИО</div>';
    header_row += '<div class="stat_table_register_role_cell">Ссылка на профиль</div>';
    header_row += '<div class="stat_table_choose_role">Голосов</div>';
    header_row += '<div class="stat_table_choose_group">% положительных голосов</div>';
    header_row += '</div>';

    table.innerHTML = header_row;

    for (let i=0;i<profiles_raiting.length;i++){
        row  = '<div class="admin_table_row">';
        row += '<div class="stat_table_number">'+String(i+1)+'</div>';
        row += '<div class="stat_table_register_username_cell">'+profiles_raiting[i]['username']+'</div>';
        row += '<div class="stat_table_register_name_cell">'+profiles_raiting[i]['full_name']+'</div>';
        row += '<div class="stat_table_register_role_cell"><a class="profile_link_stat" href="'+profiles_raiting[i]['profile_link']+'">'+profiles_raiting[i]['profile_link']+'</a></div>'
        row += '<div class="stat_table_choose_role">'+String(profiles_raiting[i]['votes'])+'</div>';
        row += '<div class="stat_table_choose_group">'+String(profiles_raiting[i]['percent'])+'%'+'</div>';
        row += '</div>';
        table.innerHTML += row;
    }

}
function get_all_marks_stat(){
    marks_all_button = document.getElementsByClassName('table_header_change_pass_button')[0];
    marks_group_button = document.getElementsByClassName('table_header_group_stat_button');
    if(marks_group_button.length!=0){
        marks_group_button = marks_group_button[0];
    }
    else{
        marks_group_button = null;
    }
    votes_all_button = document.getElementsByClassName('table_header_register_button')[0];
    votes_all_button.id = 'table_header_register_button';
    if(marks_group_button!=null){
        marks_group_button.id = 'table_header_group_stat_button';
    }
    marks_all_button.id = 'table_header_change_pass_chosen_button';
    table = document.getElementById('admin_table_block');
    table.innerHTML = '';

    header_row  = '<div class="admin_table_row_header">';
    header_row += '<div class="stat_table_number">№</div>';
    header_row += '<div class="stat_table_register_username_cell">Логин</div>';
    header_row += '<div class="stat_table_register_name_cell">ФИО</div>';
    header_row += '<div class="stat_table_avg_mark_cell">Средняя оценка</div>'
    header_row += '</div>';

    table.innerHTML = header_row;

    for (let i=0;i<all_marks_raiting.length;i++){
        row  = '<div class="admin_table_row">';
        row += '<div class="stat_table_number">'+String(i+1)+'</div>';
        row += '<div class="stat_table_register_username_cell">'+all_marks_raiting[i]['username']+'</div>';
        row += '<div class="stat_table_register_name_cell">'+all_marks_raiting[i]['full_name']+'</div>';
        row += '<div class="stat_table_avg_mark_cell">'+String(all_marks_raiting[i]['avg_mark'])+'</div>';
        row += '</div>';
        table.innerHTML += row;
    }
}
function get_group_marks_stat(group_id){
    marks_all_button = document.getElementsByClassName('table_header_change_pass_button')[0];
    marks_group_button = document.getElementsByClassName('table_header_group_stat_button');
    if(marks_group_button.length!=0){
        marks_group_button = marks_group_button[0];
    }
    else{
        marks_group_button = null;
    }
    if(marks_group_button == null){return;}
    votes_all_button = document.getElementsByClassName('table_header_register_button')[0];
    votes_all_button.id = 'table_header_register_button';
    if(marks_group_button!=null){
        marks_group_button.id = 'table_header_group_stat_chosen_button';
    }
    marks_all_button.id = 'table_header_change_pass_button';
    table = document.getElementById('admin_table_block');
    table.innerHTML = '';

    header_row  = '<div class="admin_table_row_header">';
    header_row += '<div class="stat_table_number">№</div>';
    header_row += '<div class="stat_table_register_username_cell">Логин</div>';
    header_row += '<div class="stat_table_register_name_cell">ФИО</div>';
    header_row += '<div class="stat_table_avg_mark_cell">Средняя оценка</div>'
    header_row += '</div>';

    table.innerHTML = header_row;
    let group_marks_counter = 0;
    for (let i=0;i<all_marks_raiting.length;i++){
        if(all_marks_raiting[i]['group_id']!=group_id){
            continue;
        }
        row  = '<div class="admin_table_row">';
        row += '<div class="stat_table_number">'+String(group_marks_counter+1)+'</div>';
        row += '<div class="stat_table_register_username_cell">'+all_marks_raiting[i]['username']+'</div>';
        row += '<div class="stat_table_register_name_cell">'+all_marks_raiting[i]['full_name']+'</div>';
        row += '<div class="stat_table_avg_mark_cell">'+String(all_marks_raiting[i]['avg_mark'])+'</div>';
        row += '</div>';
        table.innerHTML += row;
        group_marks_counter++;
    }
}
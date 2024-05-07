function get_register_requests(){
    let xhr = new XMLHttpRequest();
    table = document.getElementById('admin_table_block')
    xhr.open("GET","/api/register_requests/");
    xhr.responseType = 'json';
    xhr.send();

    xhr.onload = function(){
        result = xhr.response;
        for(let row=0; row<result.length;row++){
            row_div = '<div class="admin_table_row" id="row_'+row+'">';
            row_div += '<div class="admin_table_register_username_cell">'+result[row]['login']+'</div>';
            row_div += '<div class="admin_table_register_name_cell">'+result[row]['surname']+' '+result[row]['name']+' '+String(result[row]['father_name'])+'</div>';
            row_div += '<div class="admin_table_register_role_cell">'+result[row]['role']+'</div>';
            row_div +='<div class="admin_table_choose_role">';
            row_div += '<select id="choose_role_admin" name="choose_role_admin">';
            row_div += "<option value='Student' selected>Студент</option>";
            row_div += "<option value='Teacher'>Учитель</option>";
            row_div += '</select>';
            row_div+='</div>';
            row_div +='<div class="admin_table_choose_group">';
            row_div += '<select id="choose_group_admin" name="choose_group_admin">';
            row_div += "<option value='-1' selected>Нет группы</option>";
            for (let group_iter = 0; group_iter<groups.length; group_iter++){
                row_div+='<option value="'+groups[group_iter]['id']+'">'+groups[group_iter]['year_of_study']+groups[group_iter]['group_letter']+'</option>';
            }
            row_div += '</select>'
            row_div +='</div>';
            row_div += '<div class="admin_table_choose_abstract">';
            row_div += "<select id='choose_abstract_admin' name='choose_abstract_admin'>";
            for (let abstract_teacher_iter = 0; abstract_teacher_iter<abstract_teachers.length;abstract_teacher_iter++){
                row_div += "<option value='Teacher_"+abstract_teachers[abstract_teacher_iter]['id']+"'>"
                row_div += abstract_teachers[abstract_teacher_iter]['surname']+' ';
                row_div += abstract_teachers[abstract_teacher_iter]['name']+' ';
                row_div += String(abstract_teachers[abstract_teacher_iter]['father_name']);
                row_div +='</option>';
            }
            for (let abstract_student_iter = 0; abstract_student_iter<abstract_kids.length;abstract_student_iter++){
                row_div += "<option value='Student_"+abstract_kids[abstract_student_iter]['id']+"'>"
                row_div += abstract_kids[abstract_student_iter]['surname']+' ';
                row_div += abstract_kids[abstract_student_iter]['name']+' ';
                row_div += String(abstract_kids[abstract_student_iter]['father_name']);
                row_div +='</option>';
            }
            row_div+='</select>';
            row_div +='</div>';
            row_div +='<div class="admin_table_choose_accept" id="'+result[row]['id']+'" onclick="accept_register('+"'row_"+String(row)+"'"+');">✓'+'</div>';
            row_div +='<div class="admin_table_choose_deny" id="'+result[row]['id']+'" onclick="deny_register('+"'row_"+String(row)+"'"+');">X'+'</div>';
            table.innerHTML+=row_div;
        }
        return;
    }

}

function accept_register(row){
    row_div = document.getElementById(String(row));
    console.log(row_div);
}
function deny_register(row){
    row_div = document.getElementById(String(row));
    console.log(row_div);
}

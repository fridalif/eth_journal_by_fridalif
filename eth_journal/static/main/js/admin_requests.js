function get_register_requests(){
    let xhr = new XMLHttpRequest();
    table = document.getElementById('admin_table_block')
    xhr.open("GET","/api/register_requests/");
    xhr.responseType = 'json';
    xhr.send();
    xhr.onload = function(){
        result = xhr.response;
        for(let row=0; row<result.length;row++){
            row_div = '<div class="admin_table_row">';
            row_div += '<div class="admin_table_register_username_cell">'+result[row]['login']+'</div>';
            row_div += '<div class="admin_table_register_name_cell">'+result[row]['surname']+' '+result[row]['name']+' '+String(result[row]['father_name'])+'</div>';
            row_div += '<div class="admin_table_register_role_cell">'+result[row]['role']+'</div>';
            row_div +='<div class="admin_table_choose_role">'+'</div>';
            row_div +='<div class="admin_table_choose_group">'+'</div>';
            row_div += '<div class="admin_table_choose_abstract">'+'</div>';
            row_div +='<div class="admin_table_choose_accept" id="'+result[row]['id']+'">'+'</div>';
            row_div +='<div class="admin_table_choose_deny" id="'+result[row]['id']+'">'+'</div>';
            table.innerHTML+=row_div;
        }
        return;
    }
    return;
}


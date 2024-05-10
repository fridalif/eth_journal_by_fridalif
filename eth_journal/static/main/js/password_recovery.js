function send_password_recovery_request(){
    password = document.getElementById('register_input_password_block').value;
    retype_password = document.getElementById('register_input_retype_password_block').value;
    username = document.getElementById('register_input_login_block').value;
    other_info = document.getElementById('register_input_surname_block').value;
    if(password=='' || retype_password==''||username==''){
        alert('Заполните все поля!');
        return;
    }
    if(password!=retype_password){
        alert('Повтор пароля и пароль не совпадают!');
        return;
    }
    let xhr = new XMLHttpRequest();
    let request_data = JSON.stringify({"username": username,"new_password":password,"other_data":other_info});
    xhr.open("POST","/api/change_password/");
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
        alert(result["result"]);
        return;
    }
    return;
}
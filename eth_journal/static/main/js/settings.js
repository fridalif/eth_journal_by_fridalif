function change_username(){
        let xhr = new XMLHttpRequest();
        new_username = document.getElementById('change_username').value;
        let request_data = JSON.stringify({'new_username':new_username});
        xhr.open("POST","/api/change_username/");
        xhr.setRequestHeader('X-CSRFToken',document.getElementsByName("csrfmiddlewaretoken")[0].value);
        xhr.setRequestHeader('Content-Type','application/json');
        xhr.responseType = 'json';
        xhr.send(request_data);
        xhr.onload = function(){
            result = xhr.response;
            if (result['error']){
                alert(result['error']);
                return;
            }
            alert(result['result']);
            document.getElementById('profile_header').innerHTML = new_username+'↓';
            return
        }
        return
}

function change_password(user_id){
    prev_password = document.getElementById('prev_password_input').value;
    new_password = document.getElementById('new_password_input').value;
    new_retype_password = document.getElementById('new_retype_password_input').value;
    if (new_password!=new_retype_password){
        alert('Новый пароль и его повтор не совпадают');
        return;
    }
    let xhr = new XMLHttpRequest();
    let request_data = JSON.stringify({'new_password':new_password,'prev_password':prev_password,'user':user_id});
    xhr.open("POST","/api/change_password/");
    xhr.setRequestHeader('X-CSRFToken',document.getElementsByName("csrfmiddlewaretoken")[0].value);
    xhr.setRequestHeader('Content-Type','application/json');
    xhr.responseType = 'json';
    xhr.send(request_data);
    xhr.onload = function(){
        result = xhr.response;
        if (result['error']){
            alert(result['error']);
            return;
        }
        alert(result['result']);
        return;
    }
    return;
}
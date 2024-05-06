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
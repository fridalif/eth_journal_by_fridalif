function send_vote(profile_slug,send_type){
    let xhr = new XMLHttpRequest();
    let request_data = JSON.stringify({"send_type": send_type });
    xhr.open("POST","/api/profile_raiting/"+profile_slug+'/');
    xhr.setRequestHeader('X-CSRFToken',document.getElementsByName("csrfmiddlewaretoken")[0].value);
    xhr.setRequestHeader('Content-Type','application/json');
    xhr.responseType = 'json';
    xhr.send(request_data);
    xhr.onload = function(){
        result = xhr.response;
        if (result['response']){
            carma_count = result['carma_count'];
            carma_percentage = result['carma_percentage'];
            document.getElementById('carma_counter').innerHTML = 'Голосов: '+carma_count;
            document.getElementById('green_raiting_scale').style = 'width:'+carma_percentage+';background-color:green;height:100%;'
        }
        return;
    }
    return;
}

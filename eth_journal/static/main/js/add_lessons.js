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
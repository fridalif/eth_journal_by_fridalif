function send_register_request(){
	reg_form = document.getElementById('register_form');
	retype_password = document.getElementById('register_input_retype_password_block').value;
	password = document.getElementById('register_input_password_block').value;
	if(retype_password!=password){
		alert('Повтор пароля и пароль не совпадают!');
		return;
	}
	role = document.getElementById('register_input_role_block').value;
	login = document.getElementById('register_input_login_block').value;
	surname = document.getElementById('register_input_surname_block').value;
	name = document.getElementById('register_input_name_block').value;
	if (name == '' || surname == ''||login=='' || role==''||password==''){
		alert('Заполните все поля!');
		return;
	}
	reg_form.submit();
	return;
}
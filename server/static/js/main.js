jQuery(document).ready(function($) {
	$('#reg_submit').click(function(){
		username = $("#username").val()
		password = $("#password").val()
		re_password = $("#re_password").val()
		invalid = false
		if(username == ''){
			$("#username").next('.error').html('用户名不能为空')
			invalid = true
		}
		else{
			$("#username").next('.error').html('')
			invalid = false
		}
		if(password == ''){
			$("#password").next('.error').html('密码不能为空')
			invalid = true
		}
		else{
			$("#password").next('.error').html('')
			invalid = false
		}
		if(re_password == ''){
			$("#re_password").next('.error').html('确认密码不能为空')
			invalid = true
		}
		else{
			$("#re_password").next('.error').html('')
			invalid = false
		}
		if (invalid){
			return false;
		}
		if (!check_username(username)){
			$("#username").next('.error').html('仅允许字母与数字')
			invalid = true
		}else{
			$("#username").next('.error').html('')
			invalid = false
		}
		if (password != re_password){
			$("#re_password").next('.error').html('密码不匹配')
			invalid = true
		}else{
			$("#re_password").next('.error').html('')
			invalid = false
		}
		if (invalid){
			return false;
		}else{
			$('#reg_form').submit();
		}
	});
	
	$('#login_submit').click(function(){
		username = $("#username").val()
		password = $("#password").val()
		invalid = false
		if(username == ''){
			$("#username").next('.error').html('用户名不能为空')
			invalid = true
		}
		else{
			$("#username").next('.error').html('')
			invalid = false
		}
		if(password == ''){
			$("#password").next('.error').html('密码不能为空')
			invalid = true
		}
		else{
			$("#password").next('.error').html('')
			invalid = false
		}
		if (invalid){
			return false;
		}else{
			$('#login_form').submit();
		}
	});
});


	


function check_username(str){
	var result=str.match(/^[a-zA-Z0-9]+$/); 
	if(result==null) return false; 
	return true; 
}
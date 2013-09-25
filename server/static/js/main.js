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
			$("#username").next('.error').html('4-16字节，仅允许中英文数字')
			invalid = true
		}else{
			$("#username").next('.error').html('')
			invalid = false
		}
    if (invalid){
			return false;
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
	
	$('#fav').click(function(){
		$('#fav_form').submit();
	});
	
	
  $("#header_rec_link span").hover(
	function(){$(this).css( 'cursor', 'pointer' );showHover(this);},
    function(){hideHover(this);}
  );
	
  $("#header_rec ul").hover(
	function(){showHover(this);},
    function(){hideHover(this);}
  );

  $("#no_last_c").click(
    function(){
        alert('已经是第一章啦...');
   });

  $("#no_next_c").click(
    function(){
        alert('没有下一章啦...');
  });

  
  //禁止右键, 禁止选中
  //$("#content_p").bind("contextmenu",function(){return false;});  
  //$("#content_p").bind("selectstart",function(){return false;});  

  $(document).on("click", ".delete-book-btn", function () {
       var bid = $(this).data('bid');
       $("#book-id").val(bid);
  });
  
  $('#edit-book').on('hidden.bs.modal', function () {
      $(this).removeData('bs.modal');
  })

});

function showHover(el)
{
    clearTimeout( $(el).parents('ul').find("ul").data('timeout') );
    $(el).parents('ul').find("ul").slideDown(100);
}
function hideHover(el)
{
    clearTimeout( $(el).parents('ul').find("ul").data('timeout') );
    
    $(el).parents('ul').find("ul")
        .data('timeout', setTimeout(function(){
           $(el).parents('ul').find("ul").slideUp(100);
        },100));
    
}
	


function check_username(str){
  if (4 > getByteLen(str) || getByteLen(str) > 16){
    return false;
  }
	var result=str.match(/^[\w\u4e00-\u9fa5]{2,16}$/); 
	if(result==null) return false; 
	return true; 
}

 function getByteLen(val) {
    var len = 0;
    for (var i = 0; i < val.length; i++) {
        if (val[i].match(/[^\x00-\xff]/ig) != null) //全角
            len += 2;
        else
            len += 1;
    }
    return len;
}

$("#page_btn").click(function(){
    var page = $("#page_btn").val()
    $.ajax({
        url : 'user/mypage/orders',
        data : {'page':page},
        success : function(data){
            
        }
    })

})
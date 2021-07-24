$(function(){
    $("img[name=paginator]").click(function(){
        event.preventDefault()
        $.ajax({
            url: PAGINATION_URL + $(this).attr('id'),
            data:{
                // 'searchValue': searchValue, 
                // 'searchValue_2': searchValue_2,
            },
            success:function(data){
                $(PAGINATION_SECTION).html(data)
            }
        })
    });
});
$(function(){
    $("img[name=paginator]").click(function(event){
        event.preventDefault()
        $.ajax({
            url: PAGINATION_URL + $(this).attr('id') + SEARCH_VAL,
            data:{
                // 'start-date': startdate, 
                // 'end-date': enddate, 
            },
            success:function(data){
                $(PAGINATION_SECTION).html(data)
            }
        })
    });

    $("img[name=paginator2]").click(function(event){
        event.preventDefault()

        $.ajax({
            url: PAGINATION_URL2 + $(this).attr('id') + SEARCH_VAL,
            data:{
                // 'searchValue': searchValue, 
                // 'searchValue_2': searchValue_2,
            },
            success:function(data){
                $(PAGINATION_SECTION2).html(data)
            }
        })
    });
})
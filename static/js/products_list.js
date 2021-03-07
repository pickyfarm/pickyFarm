
$(document).ready(function(){
    let cat_name = document.getElementById('big_category').getAttribute('name')
    console.log(cat_name)

    if(cat_name == 'all'){
        $('img[id=all]').attr('src', "/static/images/products_list/cat_all_sel.svg");

        $('img[id=fruit]').mouseover(function () {
            $(this).attr('src', "/static/images/products_list/cat_fruit_sel.svg");
        }).mouseout(function () {
            $(this).attr('src', "/static/images/products_list/cat_fruit.svg");
        });

        $('img[id=vege]').mouseover(function(){
            $(this).attr('src', "/static/images/products_list/cat_vege_sel.svg");
        }).mouseout(function(){
            $(this).attr('src', "/static/images/products_list/cat_vege.svg");
        });

        $('img[id=etc]').mouseover(function(){
            $(this).attr('src', "/static/images/products_list/cat_etc_sel.svg");
        }).mouseout(function(){
            $(this).attr('src', "/static/images/products_list/cat_etc.svg");
        });
        
    }
    else if(cat_name == 'fruit'){
        $('img[id=fruit]').attr('src', "/static/images/products_list/cat_fruit_sel.svg");
        
        $('img[id=all]').mouseover(function(){
            $(this).attr('src', "/static/images/products_list/cat_all_sel.svg");
        }).mouseout(function(){
            $(this).attr('src', "/static/images/products_list/cat_all.svg");
        });

        $('img[id=vege]').mouseover(function(){
            $(this).attr('src', "/static/images/products_list/cat_vege_sel.svg");
        }).mouseout(function(){
            $(this).attr('src', "/static/images/products_list/cat_vege.svg");
        });

        $('img[id=etc]').mouseover(function(){
            $(this).attr('src', "/static/images/products_list/cat_etc_sel.svg");
        }).mouseout(function(){
            $(this).attr('src', "/static/images/products_list/cat_etc.svg");
        });

    }
    else if(cat_name == 'vege'){
        $('img[id=vege]').attr('src', "/static/images/products_list/cat_vege_sel.svg");


        $('img[id=fruit]').mouseover(function () {
            $(this).attr('src', "/static/images/products_list/cat_fruit_sel.svg");
        }).mouseout(function () {
            $(this).attr('src', "/static/images/products_list/cat_fruit.svg");
        });

        $('img[id=all]').mouseover(function(){
            $(this).attr('src', "/static/images/products_list/cat_all_sel.svg");
        }).mouseout(function(){
            $(this).attr('src', "/static/images/products_list/cat_all.svg");
        });

        $('img[id=etc]').mouseover(function(){
            $(this).attr('src', "/static/images/products_list/cat_etc_sel.svg");
        }).mouseout(function(){
            $(this).attr('src', "/static/images/products_list/cat_etc.svg");
        });

    }
    else if(cat_name == 'etc'){
        $('img[id=etc]').attr('src', "/static/images/products_list/cat_etc_sel.svg");

        $('img[id=fruit]').mouseover(function () {
            $(this).attr('src', "/static/images/products_list/cat_fruit_sel.svg");
        }).mouseout(function () {
            $(this).attr('src', "/static/images/products_list/cat_fruit.svg");
        });

        $('img[id=all]').mouseover(function(){
            $(this).attr('src', "/static/images/products_list/cat_all_sel.svg");
        }).mouseout(function(){
            $(this).attr('src', "/static/images/products_list/cat_all.svg");
        });

        $('img[id=vege]').mouseover(function(){
            $(this).attr('src', "/static/images/products_list/cat_vege_sel.svg");
        }).mouseout(function(){
            $(this).attr('src', "/static/images/products_list/cat_vege.svg");
        });

    }

    
    
    

    

    
});
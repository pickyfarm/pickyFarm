$(document).ready(function(){
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
});
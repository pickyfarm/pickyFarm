$(function () {
    // farmer search
    $("img[name=search_button_1]").click(function () {
        var search_key = $('#search_key').val();
        event.preventDefault()
        $.ajax({
            url: 'farmer_search/',
            data: {
                'search_key': search_key,
            },
            success: function (data) {
                $('.search_block_1').html(data)
            }
        })
    });

    // farmer's story search ajax
    $("img[name=search_button_2]").click(function () {
        var select_val = $("#story-search-select option:selected").val()
        var search_key_2 = $('#search_key_2').val();
        event.preventDefault()
        $.ajax({
            url: 'farmer_story_search/',
            data: {
                'select_val': select_val,
                'search_key_2': search_key_2,
            },
            success: function (data) {
                $('.search_block_2').html(data)
            }
        })
    });

    // tag search ajax
    $("td").click(function () {
        var search_cat = $(this).attr("id")
        event.preventDefault()
        $.ajax({
            url: 'farm_cat_search/',
            data: {
                'search_cat': search_cat,
            },
            success: function (data) {
                $('.search_block_1').html(data);
                $(this).css('background-color', 'black');
            }
        })
    });
});


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

    // category search ajax
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
            }
        })
    });

    // hashtag search ajax
    var farm_tags = document.querySelectorAll('#farm_tag');
    farm_tags.forEach(tag => {
        tag.addEventListener('click', function () {
            var search_tag = tag.getAttribute('name')
            console.log(search_tag)
            event.preventDefault()
            $.ajax({
                url: 'farm_tag_search/',
                data: {
                    'search_tag': search_tag,
                },
                success: function (data) {
                    $('.search_block_1').html(data)
                }
            })
        })
    });
})

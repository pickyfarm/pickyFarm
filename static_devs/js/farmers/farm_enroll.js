// 프로필 사진
function readInputFile_1(input) {
    if ($("#id_farmer_profile")) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var path = e.target.result;
            path = "url(" + path + ")";
            $('.default_img_1').css(
                {
                    'background': path,
                    'background-size': 'cover',
                    'background-position': 'center'
                }
            );
        }
        reader.readAsDataURL(input.files[0]);
    }
}
$("#id_farmer_profile").on('change', function () {
    readInputFile_1(this);
});


// 농장 사진
function readInputFile_2(input) {
    if ($("#id_farm_profile")) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var path = e.target.result;
            path = "url(" + path + ")";
            $('.default_img_2').css(
                {
                    'background': path,
                    'background-size': 'cover',
                    'background-position': 'center',
                }
            );
        }
        reader.readAsDataURL(input.files[0]);
    }
}
$("#id_farm_profile").on('change', function () {
    readInputFile_2(this);
});


// 해시 태그

// 해시태그 생성


function deleteHashtag(id) {
    var targetTag = id.parentNode;
    targetTag.remove();
    tagNum--;
}

// function createHashtag() {
//     if (event.keyCode === 13) {
//         var div = document.createElement("div");
//         
//         parent.appendChild(div);
//     }
// }


// 선택한 카테고리 해시태그 색상 변경
var checked = document.querySelector('input[name="farm_cat"]:checked')
checked.parentNode.setAttribute('class', 'sel_bk_color')
$("#id_farm_cat label").on("click", function () {
    if ($(this).find('input[type="radio"]').is(':checked')) {
        $(this).addClass('sel_bk_color');
    }
    else {
        $('#id_farm_cat label').removeClass('sel_bk_color');
    }
});


// farmer's page sample
$('#id_farm_name').keyup(function () {
    $('#sample_farm_name').text($(this).val());
});

$('#id_profile_title').keyup(function () {
    $('#sample_profile_title').text($(this).val());
});

$('#id_profile_desc').keyup(function () {
    $('#sample_profile_desc').text("&#34;" + $(this).val() + "&#34;");
});

$('#id_farm_news').keyup(function () {
    $('#sample_farm_news').text($(this).val());
});


// step2 page form valid check
$('#step2_submit').click(function () {
    // let cats = Array.from(document.querySelectorAll('#id_farm_cat input'))
    // console.log($('#id_farm_cat').val())
    // cats.forEach(cat => {
    //     console.log(cat)
    //     // console.log(cat.is(":checked"))
    // });
    var categories = document.getElementsByName("farm_cat").length;

    for (var i = 0; i < categories; i++) {
        if (document.getElementsByName("farm_cat")[i].checked == true) {
            let farm_cat = document.getElementsByName("farm_cat")[i].value;
            // console.log(farm_cat)
        }
    }

    if ($('#id_farm_name').val() == "") {
        alert("농장 이름을 입력해주세요.");
        return;
    }
    if ($('#id_farmer_profile').val() == "") {
        alert("프로필 사진을 업로드해주세요.");
        return;
    }
    if ($('#id_farm_profile').val() == "") {
        alert("농장 사진을 업로드해주세요.");
        return;
    }
    if ($('#id_profile_title').val() == "") {
        alert("농장 한 줄 소개를 입력해주세요.");
        return;
    }
    if ($('#id_profile_desc').val() == "") {
        alert("농장 상세 소개를 입력해주세요.");
        return;
    }
    if ($('#id_farm_thanks_msg').val() == "") {
        alert("결제 시 보여질 구매 감사 메세지를 작성해주세요.");
        event.preventDefault();
        return;
    }
    if ($('#id_farm_news').val() == "") {
        alert("농소비자에게 전달 할 농가뉴스를 작성해주세요.");
        event.preventDefault();
        return;
    }
    if ($('#id_farm_cat input').is(":checked") == false) {
        alert("카테고리를 선택해주세요.");
        event.preventDefault();
        return;
    }
})

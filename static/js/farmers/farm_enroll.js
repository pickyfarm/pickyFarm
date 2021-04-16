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


// hash tag create
function onKeyDown() {
    if (event.keyCode === 13) {
        var input = document.createElement("input");
        input.setAttribute('type', 'text');
        input.setAttribute('onKeyDown', 'onKeyDown()')
        input.setAttribute('id', 'new_tag')
        var parent = document.getElementById('hashtag_wrap');
        parent.appendChild(input);
    }
}

function resizeInput() {
    this.style.width = this.value.length + "ch";
}
var hashtag_input = document.getElementById('new_tag'); // get the input element
hashtag_input.addEventListener('input', resizeInput); // bind the "resizeInput" callback on "input" event
resizeInput.call(hashtag_input); // immediately call the function


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
            console.log(farm_cat)
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
    if ($('#id_farm_cat input').is(":checked") == false) {
        alert("카테고리를 선택해주세요.");
        event.preventDefault();
        return;
    }
})
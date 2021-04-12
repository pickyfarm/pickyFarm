// 프로필 사진
function readInputFile_1(input) {
    if($("#id_farmer_profile")) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var path = e.target.result;
            path = "url(" + path + ")";
            $('.default_img_1').css(
                {
                    'background':path, 
                    'background-size':'cover', 
                    'background-position':'center'
                }
            );
        }
        reader.readAsDataURL(input.files[0]);
    }
}
$("#id_farmer_profile").on('change', function(){
    readInputFile_1(this);
});


// 농장 사진
function readInputFile_2(input) {
    if($("#id_farm_profile")) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var path = e.target.result;
            path = "url(" + path + ")";
            $('.default_img_2').css(    
                {
                    'background':path, 
                    'background-size':'cover', 
                    'background-position':'center'
                }
            );
        }
        reader.readAsDataURL(input.files[0]);
    }
}
$("#id_farm_profile").on('change', function(){
    readInputFile_2(this);
});


// hash tag create
function onKeyDown() {
    if(event.keyCode === 13) {
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
$('#id_farm_name').keyup(function() {
    $('#sample_farm_name').text($(this).val());
});

$('#id_profile_title').keyup(function() {
    $('#sample_profile_title').text($(this).val());
});

$('#id_profile_desc').keyup(function() {
    $('#sample_profile_desc').text("&#34;"+ $(this).val() + "&#34;");
});


// form valid check

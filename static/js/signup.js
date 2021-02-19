

$("input:radio[name=gender]").on('change', function () {
    if (this.value == "male") {
        $("input:radio[value=male]").parent().addClass("checked");
        $("input:radio[value=female]").parent().removeClass("checked");
    }

    if (this.value == "female") {
        $("input:radio[value=female]").parent().addClass("checked");
        $("input:radio[value=male]").parent().removeClass("checked");
    }
});

$('#nickname-check').click(function () {
    let target = $('#id_nickname').val();
    $.ajax({
        url: 'nickname_validation/',
        data: { 'target': target },
        success: function (data) {
            if (data['isValid'] == false) {
                alert("사용 가능한 닉네임입니다.");
                $('#nicknameValidCheck').attr("valid", "true");
            } else {
                alert("이미 사용중인 닉네임입니다.");
                $('#nicknameValidCheck').attr("valid", "false");
            }
        }
    });
});

$('#id-check').click(function () {
    let target = $('#id_username').val();
    $.ajax({
        url: 'id_validation/',
        data: { 'target': target },
        success: function (data) {
            if (data['isValid'] == false) {
                alert("사용 가능한 ID입니다.");
                $('#idValidCheck').attr("valid", "true");
            } else {
                alert("이미 사용중인 ID입니다.");
                $('#idValidCheck').attr("valid", "false");
            }
        }
    });
});

$('#email-check').click(function () {
    let target = $('#id_email').val();
    $.ajax({
        url: 'email_validation/',
        data: { 'target': target },
        success: function (data) {
            if (data['isValid'] == false) {
                alert("사용 가능한 이메일입니다.");
                $('#emailValidCheck').attr("valid", "true");
            } else {
                alert("이미 사용중인 이메일입니다.");
                $('#emailValidCheck').attr("valid", "false");
            }
        }
    });
});

$('#id_username').change(function () {
    $('#idValidCheck').attr("valid", "false");
})

$('#id_email').change(function () {
    $('#emailValidCheck').attr("valid", "false");
})

$('#id_nickname').change(function () {
    $('#nicknameValidCheck').attr("valid", "false");
})

$('.submit').click(function () {
    if ($('#idValidCheck').attr("valid") == "false") {
        alert("ID 중복확인을 해주시기 바랍니다");
        $('id_username').focus();
        event.preventDefault();
        return;
    }

    if ($('#nicknameValidCheck').attr("valid") == "false") {
        alert("닉네임 중복확인을 해주시기 바랍니다");
        $('id_nickname').focus();
        event.preventDefault();
        return;
    }

    if ($('#emailValidCheck').attr("valid") == "false") {
        alert("이메일 중복확인을 해주시기 바랍니다");
        event.preventDefault();
        $('id_email').focus();
    }

    if ($('#terms_of_services').is(":checked") == false) {
        alert("이용약관에 동의해주시기 바랍니다..");
        event.preventDefault();
        return;
    }

    if ($('#personal_info').is(":checked") == false) {
        alert("개인정보처리방침에 동의해주시기 바랍니다.");
        event.preventDefault();
        return;
    }

    if ($('#over14').is(":checked") == false) {
        alert("만 14세 이상에 체크해주시기 바랍니다.");
        event.preventDefault();
        return;
    }    

    console.log($('#terms_of_services').checked);

})

$('#agree-all').change(function () {
    if (this.checked) {
        $('input[type=checkbox]').prop("checked", true);
    }

    else {
        $('input[type=checkbox]').prop("checked", false);
    }
})



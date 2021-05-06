

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

$('#nickname-check').click(function (e) {
    let target = $('#id_nickname').val();
    let url = $(this).attr('name')
    const messageContainer = document.querySelector('#nickname-valid');

    if (target=="") {
        messageContainer.innerHTML = "✕ 닉네임을 입력해주세요."
        messageContainer.classList.toggle("invalid-form", !messageContainer.classList.contains('invallid-form'))

        return;
    }

    $.ajax({
        url: url,
        data: { 'target': target },
        success: function (data) {
            if (data['isValid'] == false) {
                messageContainer.innerHTML = "✓ 사용 가능한 닉네임입니다."
                messageContainer.classList.toggle("invalid-form", messageContainer.classList.contains('invallid-form'))
                $('#nicknameValidCheck').attr("valid", "true");
            } else {
                messageContainer.innerHTML = '✕ 이미 사용중인 닉네임입니다.'
                messageContainer.classList.toggle("invalid-form", !messageContainer.classList.contains('invallid-form'))
                $('#nicknameValidCheck').attr("valid", "false");
            }
            
        }
    });
});

$('#id-check').click(function () {
    let target = $('#id_username').val();
    let url = $(this).attr('name')
    const messageContainer = document.querySelector('#id-valid');

    if (target=="") {
        messageContainer.innerHTML = "✕ ID를 입력해주세요."
        messageContainer.classList.toggle("invalid-form", !messageContainer.classList.contains('invallid-form'))
        return;
    }

    $.ajax({
        url: url,
        data: { 'target': target },
        success: function (data) {
            if (data['isValid'] == false) {
                messageContainer.innerHTML = "✓ 사용 가능한 ID입니다."
                messageContainer.classList.toggle("invalid-form", messageContainer.classList.contains('invallid-form'))
                $('#idValidCheck').attr("valid", "true");
            } else {
                messageContainer.innerHTML = '✕ 이미 사용중인 ID입니다.'
                messageContainer.classList.toggle("invalid-form", !messageContainer.classList.contains('invallid-form'))
                $('#idValidCheck').attr("valid", "false");
            }
        }
    });
});

$('#email-check').click(function () {
    let target = $('#id_email').val();
    let url = $(this).attr('name')
    const messageContainer = document.querySelector('#email-valid');

    if (target=="") {
        messageContainer.innerHTML = "✕ 이메일을 입력해주세요."
        messageContainer.classList.toggle("invalid-form", !messageContainer.classList.contains('invallid-form'))
        return;
    }

    $.ajax({
        url: url,
        data: { 'target': target },
        success: function (data) {
            if (data['isValid'] == false) {
                messageContainer.innerHTML = "✓ 사용 가능한 이메일입니다."
                messageContainer.classList.toggle("invalid-form", messageContainer.classList.contains('invallid-form'))
                $('#emailValidCheck').attr("valid", "true");
            } else {
                messageContainer.innerHTML = '✕ 이미 사용중인 이메일입니다.'
                messageContainer.classList.toggle("invalid-form", !messageContainer.classList.contains('invallid-form'))
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

document.querySelector('#id_password_re').addEventListener('change', e => {
    const targetValue = document.querySelector('#id_password').value;
    const messageContainer = document.querySelector('#password-valid');

    if (targetValue === e.target.value) {
        messageContainer.innerHTML = '✓ 비밀번호가 일치합니다'
        messageContainer.classList.toggle("invalid-form", messageContainer.classList.contains('invallid-form'))
    }

    else {
        messageContainer.innerHTML = '✕ 비밀번호가 일치하지 않습니다'
        messageContainer.classList.toggle("invalid-form", !messageContainer.classList.contains('invallid-form'))
    }
})



$('#nickname-check').click(function (e) {
    let target = $('#id_nickname').val();
    let url = $(this).attr('name');
    const messageContainer = document.querySelector('#nickname-valid');

    if (target == '') {
        messageContainer.innerHTML = '✕ 닉네임을 입력해주세요.';
        messageContainer.classList.toggle(
            'invalid-form',
            !messageContainer.classList.contains('invallid-form')
        );

        return;
    }

    $.ajax({
        url: url,
        data: { target: target },
        success: function (data) {
            if (data['isValid'] == false) {
                messageContainer.innerHTML = '✓ 사용 가능한 닉네임입니다.';
                messageContainer.classList.toggle(
                    'invalid-form',
                    messageContainer.classList.contains('invallid-form')
                );
                $('#nicknameValidCheck').attr('valid', 'true');
            } else {
                messageContainer.innerHTML = '✕ 이미 사용중인 닉네임입니다.';
                messageContainer.classList.toggle(
                    'invalid-form',
                    !messageContainer.classList.contains('invallid-form')
                );
                $('#nicknameValidCheck').attr('valid', 'false');
            }
        },
    });
});

$('#id-check').click(function () {
    let target = $('#id_username').val();
    let url = $(this).attr('name');
    const messageContainer = document.querySelector('#id-valid');

    if (target == '') {
        messageContainer.innerHTML = '✕ ID를 입력해주세요.';
        messageContainer.classList.toggle(
            'invalid-form',
            !messageContainer.classList.contains('invalid-form')
        );
        return;
    }

    $.ajax({
        url: url,
        data: { target: target },
        success: function (data) {
            if (data['isValid'] == false) {
                messageContainer.innerHTML = '✓ 사용 가능한 ID입니다.';
                messageContainer.classList.toggle(
                    'invalid-form',
                    messageContainer.classList.contains('invalid-form')
                );
                $('#idValidCheck').attr('valid', 'true');
            } else {
                messageContainer.innerHTML = '✕ 이미 사용중인 ID입니다.';
                messageContainer.classList.toggle(
                    'invalid-form',
                    !messageContainer.classList.contains('invalid-form')
                );
                $('#idValidCheck').attr('valid', 'false');
            }
        },
    });
});

$('#email-check').click(function () {
    let target = $('#id_email').val();
    console.log(target);
    let url = $(this).attr('name');
    const messageContainer = document.querySelector('#email-valid');

    if (target == '') {
        messageContainer.innerHTML = '✕ 이메일을 입력해주세요.';
        messageContainer.classList.toggle(
            'invalid-form',
            !messageContainer.classList.contains('invalid-form')
        );
        return;
    }

    $.ajax({
        url: url,
        data: { target: target },
        success: function (data) {
            if (data['isValid'] == false) {
                messageContainer.innerHTML = '✓ 사용 가능한 이메일입니다.';
                messageContainer.classList.toggle(
                    'invalid-form',
                    messageContainer.classList.contains('invallid-form')
                );
                $('#emailValidCheck').attr('valid', 'true');
            } else {
                messageContainer.innerHTML = '✕ 이미 사용중인 이메일입니다.';
                messageContainer.classList.toggle(
                    'invalid-form',
                    !messageContainer.classList.contains('invallid-form')
                );
                $('#emailValidCheck').attr('valid', 'false');
            }
        },
    });
});

// 전화번호 확인

function paddedFormat(num) {
    return num < 10 ? '0' + num : num;
}

function startCountDown(duration, element) {
    let secondsRemaining = duration;
    let min = 0;
    let sec = 0;

    let countInterval = setInterval(function () {
        min = parseInt(secondsRemaining / 60);
        sec = parseInt(secondsRemaining % 60);

        element.placeholder = `${paddedFormat(min)}:${paddedFormat(sec)}`;

        secondsRemaining = secondsRemaining - 1;
        if (secondsRemaining < 0) {
            clearInterval(countInterval);
        }
    }, 1000);
}

$('#phone-number-check').click(function () {
    let target = $('#id_phone_number').val();
    let url = $(this).attr('name');
    const messageContainer = document.querySelector('#phone-number-valid');

    if (target == '') {
        messageContainer.innerHTML = '✕ 전화번호를 입력해주세요.';
        messageContainer.classList.toggle(
            'invalid-form',
            !messageContainer.classList.contains('invalid-form')
        );
        return;
    }

    let time_minutes = 3; // Value in minutes
    let time_seconds = 0; // Value in seconds

    let duration = time_minutes * 60 + time_seconds;

    element = document.querySelector('#id_auth_number');
    element.placeholder = `${paddedFormat(time_minutes)}:${paddedFormat(
        time_seconds
    )}`;

    startCountDown(--duration, element);
    $('#phonenumValidCheck').attr('valid', 'false');

    $.ajax({
        url: url,
        data: { target: target },
        success: function (data) {
            if (data['isValid'] == false) {
                document.querySelector('#id_auth_number').style.display =
                    'block';
                document.querySelector('#auth-number-check').style.display =
                    'block';
                messageContainer.innerHTML = '인증번호를 입력해주세요.';
                messageContainer.classList.toggle(
                    'invalid-form',
                    messageContainer.classList.contains('invallid-form')
                );
                $('#phonenumValidCheck').attr('valid', 'true');
            } else {
                messageContainer.innerHTML = '✕ 이미 등록된 전화번호입니다.';
                messageContainer.classList.toggle(
                    'invalid-form',
                    !messageContainer.classList.contains('invallid-form')
                );
                $('#phonenumValidCheck').attr('valid', 'false');
            }
        },
    });
});

// 인증번호 확인
$('#auth-number-check').click(function () {
    let auth_num = $('#id_auth_number').val();
    let phone_num = $('#id_phone_number').val();
    let url = $(this).attr('name');

    if (auth_num == '') {
        alert('인증번호를 입력하세요.');
        return;
    }

    $.ajax({
        url: url,
        data: { auth_num: auth_num, phone_num: phone_num },
        success: function (data) {
            const messageContainer = document.querySelector(
                '#phone-number-valid'
            );

            console.log(data['isValid']);
            if (data['isValid'] == false) {
                alert('인증번호가 틀렸습니다.');
                return;
            } else if (data['isValid'] == true && data['timeOver'] == true) {
                alert('인증 시간이 만료되었습니다. 인증번호를 재발급하세요.');
            } else {
                console.log(data['timeOver']);
                alert('인증이 완료되었습니다.');
                document.querySelector('#id_auth_number').style.display =
                    'none';
                document.querySelector('#auth-number-check').style.display =
                    'none';
                messageContainer.innerHTML = '';
            }
        },
    });
});

$('#id_username').change(function () {
    $('#idValidCheck').attr('valid', 'false');
});

$('#id_email').change(function () {
    $('#emailValidCheck').attr('valid', 'false');
});

$('#id_nickname').change(function () {
    $('#nicknameValidCheck').attr('valid', 'false');
});

$('.submit').click(function () {
    let auth_num = $('#id_auth_number').val();

    if ($('#idValidCheck').attr('valid') == 'false') {
        alert('ID 중복확인을 해주시기 바랍니다');
        $('#id_username').focus();
        event.preventDefault();
        return;
    }

    if ($('#nicknameValidCheck').attr('valid') == 'false') {
        alert('닉네임 중복확인을 해주시기 바랍니다');
        $('#id_nickname').focus();
        event.preventDefault();
        return;
    }

    if ($('#password-valid-check').attr('valid') === 'false') {
        alert('비밀번호를 확인하여 주시기 바랍니다.');
        $('#id_password').focus();
        event.preventDefault();
        return;
    }

    if ($('#password-re-valid-check').attr('valid') === 'false') {
        alert('입력된 비밀번호가 서로 다릅니다.');
        $('#id_password_re').focus();
        event.preventDefault();
        return;
    }

    if ($('#emailValidCheck').attr('valid') == 'false') {
        alert('이메일 중복확인을 해주시기 바랍니다');
        event.preventDefault();
        $('#id_email').focus();
    }


    if ($('#terms_of_services').is(':checked') == false) {
        alert('이용약관에 동의해주시기 바랍니다.');
        event.preventDefault();
        return;
    }

    if (auth_num == '') {
        alert('인증번호를 입력하세요.');
        $('#id_phone_number').focus();
        event.preventDefault();
        return;
    }

    if ($('#personal_info').is(':checked') == false) {
        alert('개인정보처리방침에 동의해주시기 바랍니다.');
        event.preventDefault();
        return;
    }

    if ($('#over14').is(':checked') == false) {
        alert('만 14세 이상에 체크해주시기 바랍니다.');
        event.preventDefault();
        return;
    }
});

const selectAllButton = document.querySelector('#agree-all');
const checkedTerms = document.querySelectorAll('.signup-terms');

selectAllButton.addEventListener('click', () => {
    checkedTerms.forEach((checkBox) => {
        checkBox.checked = selectAllButton.checked;
    });
});

checkedTerms.forEach((item) => {
    item.addEventListener('click', () => {
        const checkedTermsCount = document.querySelectorAll(
            '.signup-terms:checked'
        ).length;

        if (checkedTerms.length !== checkedTermsCount) {
            selectAllButton.checked = false;
        } else {
            selectAllButton.checked = true;
        }
    });
});

document.querySelector('#id_password_re').addEventListener('input', (e) => {
    const targetValue = document.querySelector('#id_password').value;
    const messageContainer = document.querySelector('#password-valid');
    const validCheck = document.querySelector('#password-re-valid-check');

    if (targetValue === e.target.value) {
        messageContainer.innerHTML = '✓ 비밀번호가 일치합니다';
        messageContainer.classList.toggle(
            'invalid-form',
            messageContainer.classList.contains('invallid-form')
        );

        validCheck.setAttribute('valid', true);
    } else {
        messageContainer.innerHTML = '✕ 비밀번호가 일치하지 않습니다';
        messageContainer.classList.toggle(
            'invalid-form',
            !messageContainer.classList.contains('invallid-form')
        );

        validCheck.setAttribute('valid', false);
    }
});

document.querySelector('form').addEventListener('keydown', (e) => {
    if (e.keyCode === 13) {
        e.preventDefault();
    }
});

document.querySelector('#id_password').addEventListener('input', (e) => {
    const isSameToID =
        e.target.value === document.querySelector('#id_username').value;
    const passwordLength = e.target.value.length;
    const isOnlyAlphabet = !/[!@#$%^*()\-_=+\\\|\[\]{};:\'",.<>\/?]/.test(
        e.target.value
    );

    const sameToID = document.querySelector('#password-valid-overlap-id');
    const lengthCheck = document.querySelector('#password-valid-length');
    const characterCheck = document.querySelector('#password-valid-character');
    const messageContainer = document.querySelector('#password-valid');

    sameToID.innerHTML = '';
    lengthCheck.innerHTML = '';
    characterCheck.innerHTML = '';
    messageContainer.innerHTML = '';

    document
        .querySelector('#password-valid-check')
        .setAttribute('valid', false);
    document
        .querySelector('#password-re-valid-check')
        .setAttribute('valid', false);

    if (isSameToID) {
        sameToID.innerHTML = '✕ 비밀번호는 아이디와 같을 수 없습니다.';
    }

    if (passwordLength < 8) {
        lengthCheck.innerHTML = '✕ 비밀번호는 최소 8자리 이상이여야 합니다.';
    }

    if (isOnlyAlphabet) {
        characterCheck.innerHTML = '✕ 비밀번호는 특수문자를 포함하여야 합니다.';
    }

    if (!(isSameToID || passwordLength < 8 || isOnlyAlphabet)) {
        document
            .querySelector('#password-valid-check')
            .setAttribute('valid', true);
    }
});

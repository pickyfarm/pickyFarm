function setCookie(name, value, exp) {
    var date = new Date();
    date.setTime(date.getTime() + exp * 24 * 60 * 60 * 1000);
    document.cookie =
        name + '=' + value + ';expires=' + date.toUTCString() + ';path=/';
}

function getCookie(name) {
    var value = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return value ? value[2] : null;
}

function addCookie(name, id) {
    var value = getCookie(name);
    if (value && value != id) {
        var itemArray = value.split(',');
        if (!itemArray.includes(id)) { // 중복 제거
            itemArray.push(id);
            value = itemArray.join(',');
            setCookie(name, value);
        }
    }
    else {
        setCookie(name, id);
    }
  }

function deleteCookie(name) {
    document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

const handleDoNotShowInOneDayButton = () => {
    !getCookie('pickyfarm_modal') && setCookie('pickyfarm_modal', 'close', 1);
};

const shootToastMessage = (
    message = '메세지 예시',
    duration = 2,
    type = 'confirm'
) => {
    const toastMessageContainer = document.querySelector('#toast-container');
    const status = toastMessageContainer.classList.contains('toast-animation');
    const toastMessageContent = document.querySelector('#toast-message');
    const toastStatus = document.querySelector('#toast-status');

    switch (type) {
        case 'confirm':
            break;
        case 'alert':
            break;
        case 'error':
            break;
        default:
            throw new Error('shootToastMessage(): unexpected message type.');
    }

    const toggleAnimation = (status) => {
        toastMessageContainer.classList.add('toast-animation');
        toastMessageContent.innerHTML = message;
        toastMessageContent.classList.add('toast-message-animation');
        toastMessageContainer.style['animation-duration'] = `${duration}s`;
        toastMessageContent.style['animation-duration'] = `${duration}s`;
    };

    toggleAnimation();
    toastMessageContainer.onanimationend = () => {
        toastMessageContainer.classList.remove('toast-animation');
        toastMessageContent.classList.remove('toast-message-animation');
    };
};

const modalType = {
    event: 'event',
    alert: 'alert',
};

const showModalMessage = (
    message = '메세지를 입력하세요.',
    cb = null,
    type = modalType.alert
) => {
    if (getCookie('pickyfarm_modal') && type == modalType.event) {
        return;
    }

    const modalSection = document.querySelector('#modal-section');

    const displayModal = () => {
        modalSection.style.display = 'flex';
    };

    const hideModal = () => {
        modalSection.style.display = 'none';
    };

    document.querySelector('#modal-message').innerHTML = message;

    displayModal();

    document
        .querySelector('#modal-cancel')
        .addEventListener('click', () => hideModal());

    document
        .querySelector('#modal-close')
        .addEventListener('click', () => hideModal());

    if (type != 'event') {
        document.querySelector('#modal-close-24h').style.display = 'none';
    }

    document.querySelector('#modal-close-24h').addEventListener('click', () => {
        handleDoNotShowInOneDayButton();
        hideModal();
    });

    document.querySelector('#modal-accept').style.display = 'block';

    document.querySelector('#modal-accept').addEventListener('click', () => {
        if (cb) {
            cb();
        }
        hideModal();
    });
};

// 구독 기능 강화 모달
const subscribeModalMessage = (
    url,
    args,
    cb = null,
    buttonText = '방문하기'
) => {
    const modalSection = document.querySelector('#modal-section');
    const displayModal = () => {
        modalSection.style.display = 'flex';
    };
    const hideModal = () => {
        modalSection.style.display = 'none';
    };

    $.ajax({
        type: 'POST',
        url: url,
        data: {
            // "csrfmiddlewaretoken": csrftoken,
            farmer_pk: args,
            'farmer_pk[]': JSON.stringify(args),
        },
        success: function (data) {
            document.querySelector('#modal-message').innerHTML = data;
            displayModal();
        },
        error: (error) => {
            console.log(error);
        },
    });

    document
        .querySelector('#modal-cancel')
        .addEventListener('click', () => hideModal());

    document
        .querySelector('#modal-close')
        .addEventListener('click', () => hideModal());

    document.querySelector('#modal-accept').style.display = 'block';
    document.querySelector('#modal-accept').innerHTML = buttonText;

    document.querySelector('#modal-accept').addEventListener('click', () => {
        if (cb) {
            cb();
        }
        hideModal();
    });
};

const cartIn = (pk) => {
    addCookie('cart_list', pk)
    $.ajax({
        type: 'POST',
        url: '/user/cartIn/',
        data: {
            pk: pk,
            csrfmiddlewaretoken: csrftoken,
        },
        dataType: 'json',
        success: function (response) {
            shootToastMessage(response.message, 2);
        },
        error: function (request, status, error) {
            shootToastMessage('관리자에게 문의하세요.', 2, 'error');
        },
    });
};

const wish = (pk) => {
    $.ajax({
        type: 'POST',
        url: '/user/wish/',
        dataType: 'json',
        data: {
            pk: pk,
            csrfmiddlewaretoken: csrftoken,
        },
        success: function (response) {
            if (response.status == 0) {
                shootToastMessage('이미 찜한 무난이 입니다!');
            } else if (response.status == 1) {
                shootToastMessage('무난이를 찜했습니다');
            }
        },
        error: function (request, status, error) {
            shootToastMessage('로그인이 필요합니다.');
        },
    });
};

const subscribeCancel = (pk) => {
    let data = { pk: pk };
    $.ajax({
        type: 'POST',
        url: '/user/cancelSubs/',
        dataType: 'json',
        data: data,
        success: function (response) {
            if (response.success == 0) {
                shootToastMessage('다시 시도해주세요', 2.5, error);
            } else {
                console.log(response.success);
                shootToastMessage(response.msg, 2.5);
                $(`#${pk}-sub-farmer`).remove();
            }
        },
        error: function (request, status, error) {
            alert(
                'code:' +
                    request.status +
                    '\n' +
                    'message:' +
                    request.responseText +
                    '\n' +
                    'error:' +
                    error
            );
        },
    });
};

const subscribeFarmer = (farmerPk) => {
    $.ajax({
        type: 'POST',
        url: '/user/subs/',
        dataType: 'json',
        data: {
            farmer_pk: farmerPk,
            csrfmiddlewaretoken: csrftoken,
        },
        success: (res) => {},
    });
};

let csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
    },
});

const prohibitAccessFromMobile = (selectors) => {
    const mediaQuery = window.matchMedia('screen and (max-width: 768px)');
    const selectorArray = convertSelectorNameToNode(selectors);

    const handleProhibitedElementClick = (e) => {
        if (mediaQuery.matches) {
            e.preventDefault();
            alert('모바일에서 사용 불가능한 페이지입니다. PC로 접속해주세요.');
        }
    };

    selectorArray.forEach((selector) => {
        selector.addEventListener('click', handleProhibitedElementClick);
    });
};

const convertSelectorNameToNode = (selectors) => {
    let convertedSelectorArr = [];
    selectors.forEach((selector) => {
        convertedSelectorArr = [
            ...convertedSelectorArr,
            document.querySelector(selector),
        ];
    });

    return convertedSelectorArr;
};

const showModalMessage = (message = '메세지를 입력하세요.', cb = null) => {
    if (getCookie('pickyfarm_modal')) {
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

    document.querySelector('#modal-close-24h').addEventListener('click', () => {
        handleDoNotShowInOneDayButton();
        hideModal();
    });

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

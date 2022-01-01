const farmName = document.querySelector('#farm_name').innerText;

const url = window.location.href.split('/');

window.onload = () => {
    let eventImage = null;

    if (farmName === '시민원' && url[url.length - 2] !== '19') {
        eventImage = '/static/images/modal/siminwon_apple_trio_modal.jpg';

        const eventImgTag = `<img src=${eventImage} style="width: 380px">`;
        document.querySelector('#modal-accept').style.display = 'none';
        showModalMessage(eventImgTag, null, 'event');
    }

    if (
        farmName === '부자지간' &&
        !(url[url.length - 2] == '36' || url[url.length - 2] == '35')
    ) {
        eventImage = '/static/images/modal/bjjg_sweetp_ugly_modal.jpg';

        const eventImgTag = `<img src=${eventImage} style="width: 380px">`;
        document.querySelector('#modal-accept').style.display = 'none';
        showModalMessage(eventImgTag, null, 'event');
    }
};

// Must refactor!

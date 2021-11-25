const farmName = document.querySelector('#farm_name').innerText;

const url = window.location.href.split('/');

window.onload = () => {
    if (farmName === '시민원' && url[url.length - 2] !== '19') {
        const eventImage = '/static/images/event/siminwon_event_modal.jpg';

        const eventImgTag = `<img src=${eventImage} style="width: 380px">`;
        document.querySelector('#modal-accept').style.display = 'none';
        showModalMessage(eventImgTag);
    }
};

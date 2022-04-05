const dDay = new Date('April 30, 2022, 00:00:00');

const dateTenDOM = document.querySelector('#countdown-ten');
const dateOneDOM = document.querySelector('#countdown-one');
const hoursDOM = document.querySelector('#countdown-hours');

const render = () => {
    const diff = dDay.getTime() - new Date(Date.now()).getTime();

    const date = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const mimutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));

    const dateTen = parseInt(date / 10);
    const dateOne = date % 10;

    dateTenDOM.innerText = dateTen;
    dateOneDOM.innerText = dateOne;
    hoursDOM.innerText = `${hours} : ${mimutes}`;
};

setInterval(render, 1000);

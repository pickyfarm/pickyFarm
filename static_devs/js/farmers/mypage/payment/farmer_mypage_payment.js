const startDate = document.querySelector('#start-date');
const endDate = document.querySelector('#end-date');

document
    .querySelector('#recent-one-month')
    .addEventListener('click', () => setDateFilter(1));

document
    .querySelector('#recent-three-month')
    .addEventListener('click', () => setDateFilter(3));

document.querySelector('.date-filter-submit').addEventListener('click', () => {
    !(startDate.value && endDate.value) && alert('날짜를 모두 입력해주세요.');
});

startDate.addEventListener('change', (e) => {
    if (DateTime.fromISO(e.target.value) > DateTime.now()) {
        startDate.value = endDate.value = DateTime.now().toISODate();
    }
});

const setDateFilter = (month) => {
    const today = DateTime.now();
    const pastDate = today.minus({ months: month });

    startDate.value = pastDate.toISODate();
    endDate.value = today.toISODate();
};

if (window.matchMedia('(max-width: 768px)').matches) {
    document.querySelector('#button-payment-manage').classList.add('active');

    document.querySelector('#selected_line').style.gridArea = 'line3';
}

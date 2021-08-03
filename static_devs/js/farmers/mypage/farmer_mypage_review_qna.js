const startDate = document.querySelector('#start-date');
const endDate = document.querySelector('#end-date');

document
    .querySelector('#today')
    .addEventListener('click', () => setTodayFilter());

document
    .querySelector('#recent-one-week')
    .addEventListener('click', () => setWeekFilter(1));

document
    .querySelector('#recent-one-month')
    .addEventListener('click', () => setMonthFilter(1));

document.querySelector('.date-filter-submit').addEventListener('click', (e) => {
    !(startDate.value && endDate.value) && e.preventDefault();
    !(startDate.value && endDate.value) && shootToastMessage('날짜를 모두 입력해주세요.');
});

startDate.addEventListener('change', (e) => {
    if (DateTime.fromISO(e.target.value) > DateTime.now()) {
        startDate.value = endDate.value = DateTime.now().toISODate();
    }
});

const setTodayFilter = () => {
    const today = DateTime.now();

    startDate.value = today.toISODate();
    endDate.value = today.toISODate();
}

const setWeekFilter = (week) => {
    const today = DateTime.now();
    const pastDate = today.minus({ weeks: week});

    startDate.value = pastDate.toISODate();
    endDate.value = today.toISODate();
}

const setMonthFilter = (month) => {
    const today = DateTime.now();
    const pastDate = today.minus({ months: month });

    startDate.value = pastDate.toISODate();
    endDate.value = today.toISODate();
};
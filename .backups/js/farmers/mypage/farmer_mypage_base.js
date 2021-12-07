const handleFarmNewsUpdateButtonClick = () => {
    const farmNews = document.querySelector('#farm-news-content');
    const farmNewsUpdateButton = document.querySelector(
        '#farm-news-update-button'
    );
    const newInputBox = document.createElement('input');

    newInputBox.id = 'farm-news-content';
    newInputBox.value = farmNews.innerText;

    farmNews.replaceWith(newInputBox);
    newInputBox.focus();
    farmNewsUpdateButton.innerHTML = '확인';

    farmNewsUpdateButton.removeEventListener(
        'click',
        handleFarmNewsUpdateButtonClick
    );
    farmNewsUpdateButton.addEventListener('click', handleFarmNewsUpdateSubmit);
};

const handleFarmNewsUpdateSubmit = () => {
    const farmNewsContent = document.querySelector('#farm-news-content').value;

    $.ajax({
        type: 'POST',
        url: farmNewsUpdateURL,
        data: {
            csrfmiddlewaretoken: csrfToken,
            farm_news: farmNewsContent,
        },
        success: (data, statusText, xhr) => {
            if (xhr.status == 200) {
                alert('변경이 완료되었습니다.');
                location.reload();
            }
        },
    });
};

document
    .querySelector('#farm-news-update-button')
    .addEventListener('click', handleFarmNewsUpdateButtonClick);

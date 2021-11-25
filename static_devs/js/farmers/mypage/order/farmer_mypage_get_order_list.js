const downloadButton = document.querySelector('#order-list-download-button');

const getOrderList = async () => {
    const ajaxRequestArgs = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            isHyphened: document.querySelector(
                'input[name="phone-number-type"]:checked'
            ).value,
        }),
    };

    downloadButton.innerHTML = '변환중...';
    const response = await fetch(ajaxRequestURL, ajaxRequestArgs);

    if (response.ok) {
        const data = await response.json();
        location.href = `/download/${data['path']}`;
    } else {
        alert(await response.text());
    }
};

downloadButton.addEventListener('click', getOrderList);

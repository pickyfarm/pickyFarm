const getOrderList = async () => {
    const ajaxRequestArgs = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: {},
    };

    const response = await fetch(ajaxRequestURL, ajaxRequestArgs);

    try {
        const data = await response.json();
        location.href = `/download/${data['path']}`;
    } catch (error) {
        alert(error);
    }
};

document
    .querySelector('#order-list-download-button')
    .addEventListener('click', getOrderList);

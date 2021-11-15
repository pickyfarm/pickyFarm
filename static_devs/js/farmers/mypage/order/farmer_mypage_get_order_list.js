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

    if (response.status == 200) {
        const data = await response.json();
        location.href = `/download/${data['path']}`;
    } else {
        throw new Error('Something went wrong with fetching order lists');
    }
};

document
    .querySelector('#order-list-download-button')
    .addEventListener('click', getOrderList);

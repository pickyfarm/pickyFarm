const PRODUCT_URL = '/product/list';

const modalImage = `
    <a href=${PRODUCT_URL}>
        <img src='/static/images/index/end.jpg' alt='피키팜 끝' style='width: 380px;'/>
    </a>
`;

window.onload = () =>
    showModalMessage(
        modalImage,
        () => {
            location.href = PRODUCT_URL;
        },
        'event'
    );

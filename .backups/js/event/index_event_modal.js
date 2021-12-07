const PRODUCT_URL = '/product/detail/37';

const modalImage = `
    <a href=${PRODUCT_URL}>
        <img src='/static/images/event/index_event_image.jpg' alt='플래음 이벤트' style='width: 380px;'/>
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

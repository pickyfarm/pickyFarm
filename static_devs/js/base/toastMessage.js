const shootToastMessage = (
    message = '메세지 예시',
    duration = 2,
    type = 'confirm'
) => {
    const toastMessageContainer = document.querySelector('#toast-container');
    const status = toastMessageContainer.classList.contains('toast-animation');
    const toastMessageContent = document.querySelector('#toast-message');
    const toastStatus = document.querySelector('#toast-status');

    switch (type) {
        case 'confirm':
            break;
        case 'alert':
            break;
        case 'error':
            break;
        default:
            throw new Error('shootToastMessage(): unexpected message type.');
    }

    const toggleAnimation = (status) => {
        toastMessageContainer.classList.add('toast-animation');
        toastMessageContent.innerHTML = message;
        toastMessageContent.classList.add('toast-message-animation');
        toastMessageContainer.style['animation-duration'] = `${duration}s`;
        toastMessageContent.style['animation-duration'] = `${duration}s`;
    };

    toggleAnimation();
    toastMessageContainer.onanimationend = () => {
        toastMessageContainer.classList.remove('toast-animation');
        toastMessageContent.classList.remove('toast-message-animation');
    };
};

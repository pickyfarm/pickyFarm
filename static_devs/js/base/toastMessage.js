const shootToastMessage = (message = '메세지 예시') => {
  const toastMessageContainer = document.querySelector('#toast-container');
  const status = toastMessageContainer.classList.contains('toast-animation');
  const toastMessageContent = document.querySelector('#toast-message');

  const toggleAnimation = (status) => {
    toastMessageContainer.classList.add('toast-animation');
    toastMessageContent.innerHTML = message;
    toastMessageContent.classList.add('toast-message-animation');
  };

  toggleAnimation();
  toastMessageContainer.onanimationend = () => {
    toastMessageContainer.classList.remove('toast-animation');
    toastMessageContent.classList.remove('toast-message-animation');
  };
};

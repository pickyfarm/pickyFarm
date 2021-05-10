const shootToastMessage = () => {
  const toastMessageContainer = document.querySelector('#toast-container');
  const status = toastMessageContainer.classList.contains('toast-animation');

  const toggleAnimation = (status) => {
    toastMessageContainer.classList.add('toast-animation');
  };

  toggleAnimation();
  toastMessageContainer.onanimationend = () => {
    toastMessageContainer.classList.remove('toast-animation');
  };
};

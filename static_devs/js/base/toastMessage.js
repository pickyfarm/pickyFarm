"use strict";

var shootToastMessage = function shootToastMessage() {
  var message = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '메세지 예시';
  var duration = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 2;
  var type = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : 'confirm';
  var toastMessageContainer = document.querySelector('#toast-container');
  var status = toastMessageContainer.classList.contains('toast-animation');
  var toastMessageContent = document.querySelector('#toast-message');
  var toastStatus = document.querySelector('#toast-status');

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

  var toggleAnimation = function toggleAnimation(status) {
    toastMessageContainer.classList.add('toast-animation');
    toastMessageContent.innerHTML = message;
    toastMessageContent.classList.add('toast-message-animation');
    toastMessageContainer.style['animation-duration'] = "".concat(duration, "s");
    toastMessageContent.style['animation-duration'] = "".concat(duration, "s");
  };

  toggleAnimation();

  toastMessageContainer.onanimationend = function () {
    toastMessageContainer.classList.remove('toast-animation');
    toastMessageContent.classList.remove('toast-message-animation');
  };
};
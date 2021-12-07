"use strict";

var modalType = {
  event: 'event',
  alert: 'alert'
};

var showModalMessage = function showModalMessage() {
  var message = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : '메세지를 입력하세요.';
  var cb = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : null;
  var type = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : modalType.alert;

  if (getCookie('pickyfarm_modal') && type == modalType.event) {
    return;
  }

  var modalSection = document.querySelector('#modal-section');

  var displayModal = function displayModal() {
    modalSection.style.display = 'flex';
  };

  var hideModal = function hideModal() {
    modalSection.style.display = 'none';
  };

  document.querySelector('#modal-message').innerHTML = message;
  displayModal();
  document.querySelector('#modal-cancel').addEventListener('click', function () {
    return hideModal();
  });
  document.querySelector('#modal-close').addEventListener('click', function () {
    return hideModal();
  });

  if (type != 'event') {
    document.querySelector('#modal-close-24h').style.display = 'none';
  }

  document.querySelector('#modal-close-24h').addEventListener('click', function () {
    handleDoNotShowInOneDayButton();
    hideModal();
  });
  document.querySelector('#modal-accept').style.display = 'block';
  document.querySelector('#modal-accept').addEventListener('click', function () {
    if (cb) {
      cb();
    }

    hideModal();
  });
}; // 구독 기능 강화 모달


var subscribeModalMessage = function subscribeModalMessage(url, args) {
  var cb = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : null;
  var buttonText = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : '방문하기';
  var modalSection = document.querySelector('#modal-section');

  var displayModal = function displayModal() {
    modalSection.style.display = 'flex';
  };

  var hideModal = function hideModal() {
    modalSection.style.display = 'none';
  };

  $.ajax({
    type: 'POST',
    url: url,
    data: {
      // "csrfmiddlewaretoken": csrftoken,
      farmer_pk: args,
      'farmer_pk[]': JSON.stringify(args)
    },
    success: function success(data) {
      document.querySelector('#modal-message').innerHTML = data;
      displayModal();
    },
    error: function error(_error) {
      console.log(_error);
    }
  });
  document.querySelector('#modal-cancel').addEventListener('click', function () {
    return hideModal();
  });
  document.querySelector('#modal-close').addEventListener('click', function () {
    return hideModal();
  });
  document.querySelector('#modal-accept').style.display = 'block';
  document.querySelector('#modal-accept').innerHTML = buttonText;
  document.querySelector('#modal-accept').addEventListener('click', function () {
    if (cb) {
      cb();
    }

    hideModal();
  });
};
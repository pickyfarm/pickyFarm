"use strict";

var cartIn = function cartIn(pk) {
  $.ajax({
    type: 'POST',
    url: '/user/cartIn/',
    data: {
      pk: pk,
      csrfmiddlewaretoken: csrftoken
    },
    dataType: 'json',
    success: function success(response) {
      shootToastMessage(response.message, 2);
    },
    error: function error(request, status, _error) {
      shootToastMessage('로그인이 필요합니다.', 2, 'error');
    }
  });
};
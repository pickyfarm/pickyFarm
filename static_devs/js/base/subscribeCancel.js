"use strict";

var subscribeCancel = function subscribeCancel(pk) {
  var data = {
    'pk': pk
  };
  $.ajax({
    type: 'POST',
    url: '/user/cancelSubs/',
    dataType: "json",
    data: data,
    success: function success(response) {
      if (response.success == 0) {
        shootToastMessage("다시 시도해주세요", 2.5, error);
      } else {
        console.log(response.success);
        shootToastMessage(response.msg, 2.5);
        $("#".concat(pk, "-sub-farmer")).remove();
      }
    },
    error: function (_error) {
      function error(_x, _x2, _x3) {
        return _error.apply(this, arguments);
      }

      error.toString = function () {
        return _error.toString();
      };

      return error;
    }(function (request, status, error) {
      alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
    })
  });
};
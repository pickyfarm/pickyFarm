"use strict";

var recommentDelete = function recommentDelete(pk) {
  showModalMessage('답글을 삭제하시겠습니까?', function () {
    $.ajax({
      type: 'POST',
      url: recommentDeleteURL,
      dataType: 'json',
      data: {
        pk: pk,
        csrfmiddlewaretoken: csrftoken
      },
      success: function success(data) {
        if (data.status) {
          alert('답글이 삭제되었습니다.');
          location.reload();
        }
      }
    });
  });
};
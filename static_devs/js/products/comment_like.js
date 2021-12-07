"use strict";

var recommentLike = function recommentLike(e) {
  comment = e.target.closest('.recomment');
  pk = parseInt(comment.getAttribute('name'));
  $.ajax({
    type: 'POST',
    url: recommentLikeURL,
    dataType: 'json',
    data: {
      'pk': pk,
      'csrfmiddlewaretoken': csrftoken
    },
    success: function success(data) {
      comment.querySelector('.recomment-like-count').innerHTML = data['likes'];
      data.status ? shootToastMessage('답글에 좋아요를 눌렀습니다') : shootToastMessage('답글에 좋아요를 취소하였습니다');
    },
    error: function error(_error) {
      shootToastMessage(_error);
    }
  });
};

document.querySelectorAll('.recomment-like-button-wrap').forEach(function (elem) {
  elem.addEventListener('click', function (e) {
    return recommentLike(e);
  });
});
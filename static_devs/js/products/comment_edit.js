"use strict";

var recommentEditForm = "\n    <div class=\"comment-edit-form-container recomment-edit-form-container mx-auto\">\n        <form class=\"flex flex-col comment-edit-form recomment-edit-form w-full\">\n            <input type=\"text\" class=\"comment-edit-form-input recomment-edit-form-input\">\n            <div class=\"flex items-center justify-between\">\n                <div></div>\n                <button type=\"submit\" class=\"comment-edit-submit-button\">\uC218\uC815\uD558\uAE30</button>\n                <p class=\"comment-edit-cancel recomment-edit-cancel button\">\uCDE8\uC18C</p>\n            </div>\n        </form>\n    </div>\n    ";

var recommentEdit = function recommentEdit(targetComment, pk) {
  var comment = targetComment.closest('.recomment-text-options-wrap').previousElementSibling.innerHTML;
  targetForm = targetComment.closest('.recomment-text');
  targetForm.innerHTML = recommentEditForm;
  targetInput = targetForm.querySelector('.recomment-edit-form-input');
  targetInput.value = comment;
  targetInput.focus();
  document.querySelector('.recomment-edit-cancel').addEventListener('click', function () {
    showModalMessage('수정을 취소하시겠습니까?', function () {
      location.reload();
    });
  });
  document.querySelector('.recomment-edit-form').addEventListener('submit', function (e) {
    e.preventDefault();
    recommentEditSubmit(pk);
  });
};

var recommentEditSubmit = function recommentEditSubmit(pk) {
  var text = document.querySelector('.recomment-edit-form-input').value;
  $.ajax({
    type: 'POST',
    url: recommentEditURL,
    dataType: 'json',
    data: {
      pk: pk,
      text: text,
      csrfmiddlewaretoken: csrftoken
    },
    success: function success(data) {
      if (data.status) {
        alert('답글을 수정하였습니다.');
        location.reload();
      }
    }
  });
};
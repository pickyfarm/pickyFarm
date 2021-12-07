"use strict";

function _toConsumableArray(arr) { return _arrayWithoutHoles(arr) || _iterableToArray(arr) || _unsupportedIterableToArray(arr) || _nonIterableSpread(); }

function _nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function _unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return _arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen); }

function _iterableToArray(iter) { if (typeof Symbol !== "undefined" && iter[Symbol.iterator] != null || iter["@@iterator"] != null) return Array.from(iter); }

function _arrayWithoutHoles(arr) { if (Array.isArray(arr)) return _arrayLikeToArray(arr); }

function _arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

var recommentSubmit = function recommentSubmit(pk) {
  var textBox = document.querySelectorAll('.recomment-input-box');

  var targetComment = _toConsumableArray(textBox).find(function (elem) {
    return parseInt(elem.getAttribute('name')) === pk;
  });

  $.ajax({
    type: 'POST',
    url: "/comment/product/".concat(productPK, "/comment/").concat(pk, "/recomment/"),
    dataType: 'json',
    data: {
      text: targetComment.value,
      csrfmiddlewaretoken: csrftoken
    },
    success: function success(data) {
      targetComment.parentElement.nextElementSibling.insertAdjacentHTML('afterend', recommentComponent(data));
      targetComment.value = '';
      var t = document.querySelector("div[class=\"recomment relative\"][name=\"".concat(data.pk, "\"] .recomment-like-button-wrap")).addEventListener('click', function (e) {
        return recommentLike(e);
      });
      shootToastMessage('답글이 등록되었습니다.');
    }
  });
};
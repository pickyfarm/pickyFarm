'use strict';

var PRODUCT_URL = '/product/detail/37';
var modalImage = '\n    <a href='.concat(
    PRODUCT_URL,
    ">\n        <img src='/static/images/event/index_event_image.jpg' alt='\uD50C\uB798\uC74C \uC774\uBCA4\uD2B8' style='width: 380px;'/>\n    </a>\n"
);

window.onload = function () {
    return showModalMessage(
        modalImage,
        function () {
            location.href = PRODUCT_URL;
        },
        'event'
    );
};

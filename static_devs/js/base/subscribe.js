"use strict";

var subscribeFarmer = function subscribeFarmer(farmerPk) {
  $.ajax({
    type: 'POST',
    url: '/user/subs/',
    dataType: 'json',
    data: {
      farmer_pk: farmerPk,
      csrfmiddlewaretoken: csrftoken
    },
    success: function success(res) {}
  });
};
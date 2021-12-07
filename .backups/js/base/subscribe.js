const subscribeFarmer = (farmerPk) => {
    $.ajax({
        type: 'POST',
        url: '/user/subs/',
        dataType: 'json',
        data: {
            farmer_pk: farmerPk,
            csrfmiddlewaretoken: csrftoken,
        },
        success: (res) => {},
    });
};

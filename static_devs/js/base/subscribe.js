const subscribeFarmer = (farmerPk) => {
    $.ajax({
        type: 'POST',
        url: '/user/subs',
        dataType: 'json',
        data: {
            pk: farmerPk,
            csrfmiddlewaretoken: csrftoken,
        },
        success: (res) => {},
    });
};

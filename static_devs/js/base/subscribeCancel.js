

const subscribeCancel = (pk)=>{
    let data = { 'pk': pk };
    $.ajax({
        type: 'POST',
        url: '/user/cancelSubs/',
        dataType: "json",
        data: data,
        success: function (response) {
            if (response.success == 0) {
                shootToastMessage("다시 시도해주세요", 2.5, error);
            }
            else {
                console.log(response.success)
                shootToastMessage(response.msg, 2.5);
                $(`#${pk}-sub-farmer`).remove();

            }
        },
        error: function (request, status, error) {
            alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
        }
    })
}
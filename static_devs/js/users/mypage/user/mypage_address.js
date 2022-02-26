$('#set-default-addr-btn').click(function (e) {
    const addrPK = document.querySelector('input[name="default_address"]:checked').value;
    $.ajax({
        type: 'POST',
        url: setDefaultAddrURL,
        data: {
            'pk': addrPK,
        },
        success: function (response) {
            if (response['status'] == true) {
                alert("기본 주소지 변경이 완료되었습니다.")
            } else {
                alert("기본 주소지 변경 실패하였습니다.")
            }
        },
    });
})


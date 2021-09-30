function getAddress() {
    new daum.Postcode({
        oncomplete: function (data) {
            let addr = '';
            let extraAddr = '';

            if (data.userSeletedType === 'R') {
                addr = data.roadAddress;
            } else {
                addr = data.roadAddress;
            }

            if (data.userSelectedType === 'R') {
                if (data.bname !== '' && /[동|로|가]$/g.test(data.bname)) {
                    extraAddr += data.bname;
                }

                if (data.buildingName !== '' && data.apartment === 'Y') {
                    extraAddr +=
                        extraAddr !== ''
                            ? ', ' + data.buildingName
                            : data.buildingName;
                }

                if (extraAddr !== '') {
                    extraAddr = ' (' + extraAddr + ')';
                }

                document.getElementById('id_extra_address').value = extraAddr;
            } else {
                document.getElementById('id_extra_address').value = '';
            }

            document.getElementById('id_full_address').value = addr;
            if (document.getElementById('delivery-address')) {
                document.getElementById('delivery-address').value = addr;
            }
            document.getElementById('id_sido').value = data.sido;
            document.getElementById('id_sigungu').value = data.sigungu;
            document.getElementById('id_zipcode').value = data.zonecode;

            document.getElementById('id_detail_address').focus();
        },

        shorthand: false,
        animation: true,
    }).open({
        q: document.getElementById('id_full_address').value,
    });
}

document.querySelector('#id_full_address').addEventListener('keydown', (e) => {
    if (e.keyCode === 13) {
        getAddress();
    }
});

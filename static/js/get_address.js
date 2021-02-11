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

            // 사용자가 선택한 주소가 도로명 타입일때 참고항목을 조합한다.
            if (data.userSelectedType === 'R') {
                // 법정동명이 있을 경우 추가한다. (법정리는 제외)
                // 법정동의 경우 마지막 문자가 "동/로/가"로 끝난다.
                if (data.bname !== '' && /[동|로|가]$/g.test(data.bname)) {
                    extraAddr += data.bname;
                }
                // 건물명이 있고, 공동주택일 경우 추가한다.
                if (data.buildingName !== '' && data.apartment === 'Y') {
                    extraAddr += (extraAddr !== '' ? ', ' + data.buildingName : data.buildingName);
                }
                // 표시할 참고항목이 있을 경우, 괄호까지 추가한 최종 문자열을 만든다.
                if (extraAddr !== '') {
                    extraAddr = ' (' + extraAddr + ')';
                }
                // 조합된 참고항목을 해당 필드에 넣는다.
                document.getElementById("id_extra_address").value = extraAddr;

            } else {
                document.getElementById("id_extra_address").value = '';
            }

            document.getElementById("id_full_address").value = addr;
            document.getElementById("id_sido").value = data.sido;
            document.getElementById("id_sigungu").value = data.sigungu;

            document.getElementById("id_detail_address").focus();
        },

        shorthand: false,
        animation: true,
    }).open({
        q: document.getElementById("id_full_address").value,
    });
}
const initinalFriendList = [
    {
        info: {
            id: 0,
            name: `friend`,
            phoneNum: '01000000000',
            address: {
                sigungu: '서울시 어쩌구 저쩌구',
                detail: '머선 아파트 머선동',
                zipCode: '00000',
            },
        },
        message: '',
        infoScope: '',
        quantity: 1,
    },
];

const purchaseApp = new Vue({
    delimiters: ['[[', ']]'],
    el: '#payment-app',
    data: {
        friendCount: 1,
        productPrice: 10000,
        friends: initinalFriendList,
    },

    computed: {
        numberOfFriend: function () {
            return this.friends.length;
        },
        sumOfQuantity: function () {
            // friend들의 quantity의 합계 구함
            return this.friends.reduce(
                (prev, next) => prev + (parseInt(next.quantity) || 1),
                0
            );
        },
        orderTotalPrice: function () {
            return this.sumOfQuantity * this.productPrice;
        },
    },

    methods: {
        addFriend: function () {
            this.friends.push({
                info: {
                    id: this.friendCount++,
                    name: `friend${this.friendCount}`,
                    phoneNum: '01000000000',
                    address: {
                        sigungu: '서울시 어쩌구 저쩌구',
                        detail: '머선 아파트 머선동',
                        zipCode: '00000',
                    },
                },
                infoScope: '',
                message: '',
                quantity: 1,
            });
        },
        deleteFriend: function (id) {
            this.friends = this.friends.filter((el) => el.info.id !== id);
        },
        handleSubmitButtonClick: function (e) {
            this.friends = this.friends.filter((el) => el.infoScope);
            e.preventDefault();
        },
        handleAddressFindButtonClick: function (idx) {
            // callback 형태로 다음 우편번호 API의 결과값을 내부 변수에 할당할 수 있음
            executeDaumPostcodeAPI((data) => {
                this.friends[idx].info.address.sigungu = data.address;
                this.friends[idx].info.address.zipCode = data.zipCode;
            });
        },
    },
});

function executeDaumPostcodeAPI(cb) {
    const addressInfo = {
        address: '',
        zipCode: '',
    };

    new daum.Postcode({
        oncomplete: function (data) {
            // 팝업에서 검색결과 항목을 클릭했을때 실행할 코드를 작성하는 부분.

            // 도로명 주소의 노출 규칙에 따라 주소를 표시한다.
            // 내려오는 변수가 값이 없는 경우엔 공백('')값을 가지므로, 이를 참고하여 분기 한다.
            var roadAddr = data.roadAddress; // 도로명 주소 변수
            var extraRoadAddr = ''; // 참고 항목 변수

            // 법정동명이 있을 경우 추가한다. (법정리는 제외)
            // 법정동의 경우 마지막 문자가 "동/로/가"로 끝난다.
            if (data.bname !== '' && /[동|로|가]$/g.test(data.bname)) {
                extraRoadAddr += data.bname;
            }
            // 건물명이 있고, 공동주택일 경우 추가한다.
            if (data.buildingName !== '' && data.apartment === 'Y') {
                extraRoadAddr +=
                    extraRoadAddr !== ''
                        ? ', ' + data.buildingName
                        : data.buildingName;
            }
            // 표시할 참고항목이 있을 경우, 괄호까지 추가한 최종 문자열을 만든다.
            if (extraRoadAddr !== '') {
                extraRoadAddr = ' (' + extraRoadAddr + ')';
            }

            // 우편번호와 주소 정보를 해당 필드에 넣는다.
            addressInfo.zipCode = data.zonecode;
            addressInfo.address = roadAddr;

            cb(addressInfo);
        },
    }).open();
}

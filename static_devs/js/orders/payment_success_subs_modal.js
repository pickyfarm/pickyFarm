const unsubFarmersPk = [
    [
        ...document.querySelectorAll(
            '.order-payment-success-unsubfarmer-appreciate-message-card-section'
        ),
    ].map((elem) => elem.dataset.farmerpk),
];

const subscribeFarmers = (farmers) => {
    farmers.forEach((farmer) => {
        subscribeFarmer(parseInt(farmer));
    });

    alert('구독을 완료하였습니다!');
};

if (unsubFarmerCount > 0) {
    window.onload = () =>
        subscribeModalMessage(
            '/order/payment/subscribe',
            unsubFarmersPk,
            () => subscribeFarmers(unsubFarmersPk),
            '구독하기'
        );
}

const app = new Vue({
    el: '#gift_address_input_section',
    data: {
        sigungu: '',
        detail: '',
        zipCode: '',
    },

    methods: {
        handleAddressFindClick: function () {
            executeDaumPostcodeAPI((data) => {
                this.sigungu = data.address;
                this.zipCode = data.zipCode;
            });

            this.$refs.detail.focus();
        },
    },
});

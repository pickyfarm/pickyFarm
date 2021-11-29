const handleDoNotShowInOneDayButton = () => {
    !getCookie('pickyfarm_modal') && setCookie('pickyfarm_modal', 'close', 1);
};

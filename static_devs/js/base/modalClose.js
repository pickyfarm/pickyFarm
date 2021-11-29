import { getCookie, setCookie } from './cookieHandler';

const handleDoNotShowInOneDayButton = () => {
    !getCookie('pickyfarm_modal') && setCookie('pickyfarm_modal', 'close', 1);
};

export default handleDoNotShowInOneDayButton;

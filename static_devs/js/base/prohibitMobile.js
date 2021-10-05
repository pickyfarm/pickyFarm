const prohibitAccessFromMobile = (selectors) => {
    const mediaQuery = window.matchMedia('screen and (max-width: 768px)');
    const selectorArray = convertSelectorNameToNode(selectors);

    const handleProhibitedElementClick = (e) => {
        if (mediaQuery.matches) {
            e.preventDefault();
            alert('모바일에서 사용 불가능한 페이지입니다. PC로 접속해주세요.');
        }
    };

    selectorArray.forEach((selector) => {
        selector.addEventListener('click', handleProhibitedElementClick);
    });
};

const convertSelectorNameToNode = (selectors) => {
    let convertedSelectorArr = [];
    selectors.forEach((selector) => {
        convertedSelectorArr = [
            ...convertedSelectorArr,
            document.querySelector(selector),
        ];
    });

    return convertedSelectorArr;
};

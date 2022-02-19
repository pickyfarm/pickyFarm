function isProductDetailPage(url) {
    const PRODUCT_DETAIL_URL_PATTERN = 'product/detail';

    return url.includes(PRODUCT_DETAIL_URL_PATTERN);
}

document.addEventListener('DOMContentLoaded', function () {
    const traceData = isProductDetailPage(location.href) ?? productTraceData;

    BootPay.startTrace(traceData);
});

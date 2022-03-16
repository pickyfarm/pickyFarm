const cartButtons = document.querySelectorAll('.cart-button');

Array.from(cartButtons).forEach((el) => {
    el.addEventListener('click', (e) => {
        cartIn(el.dataset.pk);
    });
});

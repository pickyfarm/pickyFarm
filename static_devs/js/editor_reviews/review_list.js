const articleList = document.querySelectorAll('.article');

document.querySelectorAll('.category-in').forEach((elem) => {
    elem.addEventListener('click', () => {
        articleList.forEach((elem) => {
            elem.style.display = 'flex';
        });

        Array.from(articleList)
            .filter((el) => {
                return el.getAttribute('category') !== elem.getAttribute('id');
            })
            .forEach((el) => {
                el.style.display = 'none';
            });
    });
});

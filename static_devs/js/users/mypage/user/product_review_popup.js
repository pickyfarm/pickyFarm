$('input:radio').on('change', function () {
    if (this.value == 5) {
        $(this).parent().addClass('checked');
        $(this)
            .parent()
            .parent()
            .siblings()
            .find('input:radio[value=3]')
            .parent()
            .removeClass('checked');
        $(this)
            .parent()
            .parent()
            .siblings()
            .find('input:radio[value=1]')
            .parent()
            .removeClass('checked');
    }
    if (this.value == 3) {
        $(this).parent().addClass('checked');
        $(this)
            .parent()
            .parent()
            .siblings()
            .find('input:radio[value=5]')
            .parent()
            .removeClass('checked');
        $(this)
            .parent()
            .parent()
            .siblings()
            .find('input:radio[value=1]')
            .parent()
            .removeClass('checked');
    }
    if (this.value == 1) {
        $(this).parent().addClass('checked');
        $(this)
            .parent()
            .parent()
            .siblings()
            .find('input:radio[value=5]')
            .parent()
            .removeClass('checked');
        $(this)
            .parent()
            .parent()
            .siblings()
            .find('input:radio[value=3]')
            .parent()
            .removeClass('checked');
    }
});

const clipBox = document.querySelector('.clip-box');
const addfile = document.querySelector('.add-file');
clipBox.addEventListener('click', () => {
    addfile.click();
    addfile.style.display = 'block';
    console.log('click!');
});

// review rating form

document
    .querySelector('#product-review-form')
    .addEventListener('change', () => {
        const freshness = document.querySelector(
            'input[name="freshness"]:checked'
        )
            ? parseInt(
                  document.querySelector('input[name="freshness"]:checked')
                      .value
              )
            : undefined;

        const flavor = document.querySelector('input[name="flavor"]:checked')
            ? parseInt(
                  document.querySelector('input[name="flavor"]:checked').value
              )
            : undefined;

        const costPerformance = document.querySelector(
            'input[name="cost_performance"]:checked'
        )
            ? parseInt(
                  document.querySelector(
                      'input[name="cost_performance"]:checked'
                  ).value
              )
            : undefined;

        if (freshness && flavor && costPerformance) {
            const avgRating = Math.floor(
                (freshness + flavor + costPerformance) / 3
            );

            document.querySelectorAll('.star-img').forEach((elem, idx) => {
                elem.src = idx < avgRating ? yellowStar : greyStar;
            });

            document.querySelector('.starRating').value = avgRating;
        }
    });

// star
// const starRating = document.querySelector('.starRating');
// const stars = document.querySelectorAll('.star-img');
// console.log(stars.length);
// console.log(stars);
// for (i = 0; i < stars.length; i++) {
//     stars[i].addEventListener('click', function (e) {
//         const elem = e.target;
//         for (k = 0; k < stars.length; k++) {
//             if (stars[k] == elem) {
//                 tempNumber = k;
//             }
//         }

//         for (j = 0; j <= tempNumber; j++) {
//             stars[j].src =
//                 "{% static 'images/users/mypage/user/star-yellow.svg' %}";
//             starRating.value = j + 1;
//         }
//         if (tempNumber < 4) {
//             for (l = tempNumber + 1; l <= 4; l++) {
//                 stars[l].src =
//                     "{% static 'images/users/mypage/user/gray-star.svg' %}";
//             }
//         }
//     });
// }

const check_btn = document.querySelector('.review-reason-submit-wrap');
const check_img = document.querySelector('.review-reason-submit-img');
const switchCheckImgHoverIn = function (e) {
    check_img.setAttribute(
        'src',
        "{% static 'images/users/mypage/user/check_hover.svg' %}"
    );
};
const switchCheckImgHoverOut = function (e) {
    check_img.setAttribute(
        'src',
        "{% static 'images/users/mypage/user/check_nohover.svg' %}"
    );
};
check_btn.addEventListener('mouseover', switchCheckImgHoverIn);
check_btn.addEventListener('mouseleave', switchCheckImgHoverOut);

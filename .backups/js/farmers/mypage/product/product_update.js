$('input:radio[value=delivery]').parent().addClass('checked');

$('input:radio[name=farm_cat]').on('change', function () {
    if (this.value == 'delivery') {
        console.log(this.value);
        $('input:radio[value=delivery]').parent().addClass('checked');
        $('input:radio[value=jeju-delivery]').parent().removeClass('checked');
    }

    if (this.value == 'jeju-delivery') {
        $('input:radio[value=jeju-delivery]').parent().addClass('checked');
        $('input:radio[value=delivery]').parent().removeClass('checked');
    }
});

$('input:radio[name=legal-box]').on('change', function () {
    if (this.value == 'delivery') {
        console.log(this.value);
        $('input:radio[value=delivery]').parent().addClass('checked');
        $('input:radio[value=jeju-delivery]').parent().removeClass('checked');
    }

    if (this.value == 'jeju-delivery') {
        $('input:radio[value=jeju-delivery]').parent().addClass('checked');
        $('input:radio[value=delivery]').parent().removeClass('checked');
    }
});

$('input:checkbox[name=yearly-yield]').on('click', function () {
    if (
        $('input:checkbox[value=yearly]').parent().hasClass('checked') === true
    ) {
        $('input:checkbox[value=yearly]').parent().removeClass('checked');
        $('input:checkbox[value=yearly]').prop('checked', false);
    } else {
        $('input:checkbox[value=yearly]').parent().addClass('checked');
        $('input:checkbox[value=yearly]').prop('checked', true);
    }
});

$('input:checkbox[name=normal-yearly-yield]').on('click', function () {
    if (
        $('input:checkbox[value=normal-yearly]')
            .parent()
            .hasClass('checked') === true
    ) {
        $('input:checkbox[value=normal-yearly]')
            .parent()
            .removeClass('checked');
        $('input:checkbox[value=normal-yearly]').prop('checked', false);
    } else {
        $('input:checkbox[value=normal-yearly]').parent().addClass('checked');
        $('input:checkbox[value=normal-yearly]').prop('checked', true);
    }
});

const normalProductCheckbox = document.querySelector('#submit-normal');
const uglyProductCheckbox = document.querySelector('#submit-ugly');
const normal = document.querySelector('.normal-product');
const ugly = document.querySelector('.ugly-product');

const addTodo = (e, target) => {
    target.style.display = e.target.checked ? 'none' : 'block';
};

normalProductCheckbox.addEventListener('click', (e) => addTodo(e, normal));
uglyProductCheckbox.addEventListener('click', (e) => addTodo(e, ugly));

document.querySelector('.product-form').addEventListener('submit', (e) => {
    !normalProductCheckbox &&
        !uglyProductCheckbox &&
        alert('상품을 한개 이상 등록해주세요!');
});

// 모바일에서 버튼 이름 변경
if (window.matchMedia('(max-width: 768px)').matches) {
    const submitBtn = document.getElementById('submit_btn');
    submitBtn.value = '확인';
}

// 연중생산 체크시 수확일자 비활성화
const uglyCropHarvestStartDate = document.querySelectorAll(
    "input[name='harvest-start-date']"
)[0];
const uglyCropHarvestEndDate = document.querySelectorAll(
    "input[name='harvest-end-date']"
)[0];

const normalCropHarvestStartDate = document.querySelectorAll(
    "input[name='normal-harvest-start-date']"
)[0];
const normalCropHarvestEndDate = document.querySelectorAll(
    "input[name='normal-harvest-end-date']"
)[0];

const disableDateInput = (inputElements) => {
    inputElements.forEach((elem) => {
        elem.disabled = true;
    });
};

const enableDateInput = (inputElements) => {
    inputElements.forEach((elem) => {
        elem.disabled = false;
    });
};

const toggleDateInputAvailablity = (inputElements) => {
    inputElements[0].disabled
        ? enableDateInput(inputElements)
        : disableDateInput(inputElements);
};

document
    .querySelector("input[name='yearly-yield']")
    .addEventListener('input', (e) => {
        toggleDateInputAvailablity([
            uglyCropHarvestStartDate,
            uglyCropHarvestEndDate,
        ]);
    });

document
    .querySelector("input[name='normal-yearly-yield']")
    .addEventListener('input', (e) => {
        toggleDateInputAvailablity([
            normalCropHarvestStartDate,
            normalCropHarvestEndDate,
        ]);
    });

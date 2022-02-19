let menuBtns = []
menuBtns.push(document.getElementById('menu_carts'))
menuBtns.push(document.getElementById('menu_likes'))
menuBtns.push(document.getElementById('menu_deliveries'))
menuBtns.push(document.getElementById('menu_infos'))

$('#menu_boughts').css({
    "background-color": "#5c6754",
    "color": "white",
})


menuBtns.forEach(item => {
    item.addEventListener('mouseover', function () {
        $(this).css({
            "background-color": "#5c6754",
            "color": "white",

        })
    })
    item.addEventListener('mouseout', function () {
        $(this).css({
            "background-color": "white",
            "color": "#5c6754"
        })
    })
})

let cartInbtns = document.querySelectorAll('#cartIn_btn')
cartInbtns.forEach(item => {
    item.addEventListener('click', function () {
        let pk = item.getAttribute('name')
        console.log(pk);
        cartIn(pk)
    })
})

// let filter6Month = document.getElementById('filter-6month')

// filter6Month.addEventListener('click', function () {
//     let sDateInput = document.getElementById('filter-start-date')
//     let eDateInput = document.getElementById('filter-end-date')
//     let submitBtn = document.getElementById('filter-submit')
//     const now = new Date()

//     let nowMonth = now.getMonth() + 1

//     let startMonth = nowMonth - 6
//     let year = now.getFullYear()
//     let startYear = year

//     if (startMonth <= 0) {
//         if (startMonth == 0) {
//             startMonth = 12
//             startYear -= 1
//         }
//         else {
//             startMonth = 12 + startMonth + 1
//             startYear -= 1
//         }
//     }
//     if (startMonth < 10)
//         startMonth = '0' + startMonth

//     startDate = startYear + '-' + startMonth + '-01'

//     sDateInput.setAttribute('value', startDate)

//     nowDate = now.getDate()
//     if (nowDate < 10)
//         nowDate = '0' + nowDate

//     if (nowMonth < 10)
//         nowMonth = '0' + nowMonth

//     endDate = year + '-' + nowMonth + '-' + nowDate
//     console.log(endDate)
//     eDateInput.setAttribute('value', endDate)

//     submitBtn.click()

// })
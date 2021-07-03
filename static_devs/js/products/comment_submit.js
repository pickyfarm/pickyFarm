const btns = document.querySelectorAll('#rec_submit')
btns.forEach(btn => btn.addEventListener('click', recommentSubmit));

const recommentSubmit = () => {
    let comment_id = $(this).attr('name') // {{comment.id}}
    let parent = $(this).parent(); // recommentform_{{comment.id}}
    let text = parent.children('#id_text').val() // recomment text value
    console.log(text);

    $.ajax({
        type: 'POST',
        url: `/comment/${productPK}/recomment/create/`,
        dataType: 'json',
        data: {
            'text': text,
            'pk': productPK,
            'user': userPK,
            'csrfmiddlewaretoken': csrftoken,
        },
        success: function (data) {
            if (text === '') {
                alert('댓글을 입력해주세요');
                return;
            }
            let recomment = `
            <div class="recomment_list text-center m-4 p-4" id="recomment_list_${comment_id}">
                <div class="flex flex-row" id="recomment">
                    <div class="mr-4" style="width: 10px; height: 10px; 
                                        border-left: 2px solid #5c6754; 
                                        border-bottom: 2px solid #5c6754;"></div>
                    <div class="">
                        <img id="consumer_img" src="${data.user_image}" alt="">
                    </div>
                    <div class="flex items-center ml-6">
                        <div class="flex flex-row" style="font-size: 15px;">
                            <div class="text-left" style="width: 175px; border-right: solid 3px #999999;">${data.author}</div>
                            <div class="" style="width: 340px; border-right: solid 3px #999999; color:#989898;">${data.create_at}</div>
                            <div class="flex flex-row" id="report" style="margin-left:87.8px">
                                <img src="{% static 'images/report.svg' %}" alt="">
                                <div class="text-black text-opacity-40 pl-2">신고하기</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="mt-6 mb-6 text-left pl-8" style="font-size: 17px;">
                    ${data.text}
                </div>
            </div>`
            let list = parent.parent().children(`div[name=${comment_id}]`);
            list.append(recomment);
            parent.children('#id_text').val('')
            const [...recomment_forms] = document.querySelectorAll('.recomment_form')
            recomment_forms.forEach((form) => {
                form.scrollBy(0, 10000)
            });
        },
        error: function () {
            alert('error');
        }
    });
}

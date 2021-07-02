let editInfoBtn = document.getElementById('edit-info');
let editProfileBtn = document.getElementById('edit-profile');

let profileContentSection = document.getElementById('profile-content-section');

editProfileBtn.addEventListener('click', function () {
    let nickNameSection = document.getElementById('nickname');
    let nickName = nickNameSection.innerHTML;
    nickNameSection.innerHTML = ' ';
    console.log(nickName);
    editProfileBtn.remove();

    console.log(nickName);

    nickNameInnerHTML = `<input id="nickname-input" type="text" value=${nickName}>`;
    nickNameSection.innerHTML = nickNameInnerHTML;

    let editProfileImage = document.getElementById('edit-profile-image');
    editProfileImage.setAttribute('class', 'flex mx-auto mt-5');

    let profileSection = document.getElementById('profile-section');
    let completeBtn = document.getElementById('profile-edit-complete');
    completeBtn.setAttribute('class', 'mx-auto mt-10');
    console.log(completeBtn);
    profileSection.appendChild(completeBtn);
});

let imgTag = document.getElementById('profile-image');
let imageInput = document.getElementById('edit-profile-image-input');

imageInput.addEventListener('change', function () {
    console.log(this.files);
    let file = this.files[0];

    if (!file.type.startsWith('image/')) return;

    let reader = new FileReader();
    reader.onload = function (e) {
        let src = e.target.result;
        imgTag.setAttribute('src', src);
    };
    reader.readAsDataURL(file);
});

let profileEditCompleteBtn = document.getElementById('profile-edit-complete');

profileEditCompleteBtn.addEventListener('click', function () {
    let nickName = document.getElementById('nickname-input').value;
    console.log(nickName);

    let imageFile = document.getElementById('edit-profile-image-input')
        .files[0];
    console.log(imageFile);

    let formData = new FormData();
    formData.append('nick_name', nickName);
    formData.append('profile_img', imageFile);

    for (var key of formData.keys()) {
        console.log(key);
    }

    for (var value of formData.values()) {
        console.log(value);
    }

    // data = {
    //   'nick_name':nickName,
    //   'profile_image':imageFile,
    //   "csrfmiddlewaretoken": "{{csrf_token}}",
    // }
    // console.log(formData)
    /*이미지를 보내려면 ajax가 아닌 http post를 써야 하는가 */
    // axios.post("{% url 'users:profileUpdate'%}", formData,{
    //   headers:{
    //     'Content-Type':'multipart/form-data'
    //   }
    // })
    // .then((response)=>{
    //   alert("프로필 정보 수정 완료")
    //   window.location.reload()
    // })
    // .catch((error)=>{
    //   alert("프로필 정보 수정 실패")
    // })

    $.ajax({
        type: 'POST',
        url: profileUpdateURL,
        data: formData,
        processData: false,
        contentType: false,
        success: function () {
            alert('프로필 정보 수정 완료');
            window.location.reload();
        },
    });
});

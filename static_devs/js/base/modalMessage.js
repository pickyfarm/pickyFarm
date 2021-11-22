const showModalMessage = (message = '메세지를 입력하세요.', cb = null) => {
    const modalSection = document.querySelector('#modal-section');

    const displayModal = () => {
        modalSection.style.display = 'flex';
    };

    const hideModal = () => {
        modalSection.style.display = 'none';
    };

    // document.querySelector('#modal-message').innerHTML = message;

    displayModal();

    document
        .querySelector('#modal-cancel')
        .addEventListener('click', () => hideModal());

    document
        .querySelector('#modal-close')
        .addEventListener('click', () => hideModal());

    document.querySelector('#modal-accept').addEventListener('click', () => {
        if (cb) {
            cb();
        }
        hideModal();
    });
};


// 구독 기능 강화 모달
const subscribeModalMessage = (url, args, cb = null) => {
  const subModalSection = '#modal-section'

  $.ajax({
    type: 'POST',
    url: url,
    dataType: 'json',
    data: {
      "csrfmiddlewaretoken": csrftoken,
      "unsub_pk": args,
    },
    success: function(data){
        $(subModalSection).html(data)
    }
  })

  document.querySelector('#modal-accept').addEventListener('click', () => {
    if (cb) {
      cb();
    }
    hideModal();
  });
}
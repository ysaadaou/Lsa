const initApp = () => {

  const openModalButtons = document.querySelectorAll('[data-modal-target]')
  const closeModalButtons = document.querySelectorAll('[data-close-button]')

  const overlay = document.getElementById('overlay')

  openModalButtons.forEach(button => {
    button.addEventListener('click', () => {
      const modal = document.querySelector(button.dataset.modalTarget)
      const elem = document.getElementById("sumy");
      if(elem != null)
      elem.remove()
      const textarea = document.getElementById("text");
      textarea.value = ""
      openModal(modal)
    })
  })
   
  overlay.addEventListener('click', () => {
    const modals = document.querySelectorAll('.modal.active')
    modals.forEach(modal => {
      closeModal(modal)
    })

  })

function openModal(modal) {
  if(modal == null) return
  modal.classList.add('active')
  overlay.classList.add('active')
}


function closeModal(modal) {
  if(modal == null) return
  modal.classList.remove('active')
  overlay.classList.remove('active')
}
  const droparea = document.querySelector('.droparea');

  const active = () => droparea.classList.add("green-border");

  const inactive = () => droparea.classList.remove("green-border");

  const prevents = (e) => e.preventDefault();


  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(evtName => {
    droparea.addEventListener(evtName, prevents);
  });

  ['dragenter', 'dragover'].forEach(evtName => {
    droparea.addEventListener(evtName, active);
  });


  ['dragleave', 'drop'].forEach(evtName => {
    droparea.addEventListener(evtName, inactive);
  });

  droparea.addEventListener("drop", handleDrop);

}

document.addEventListener("DOMContentLoaded", initApp);

const handleDrop = (e) => {
  const dt = e.dataTransfer;
  const files = dt.files[0];
  const formData = new FormData();
    formData.append('file', files);
    fetch('/process_file', {
    method: 'POST',
    body: formData
  })
  .then((response) => response.json())
  .then((data) => {

    const textarea = document.getElementById('text');
    textarea.value = data.original_text;
  })
  .catch((error) => {
    console.error(error);
  });
}

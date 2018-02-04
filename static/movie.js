const loaded = () => {
    let loadingGif = document.querySelector('.loading-gif');
    let recContent = document.querySelector('.recommendation');
    let submitBtn = document.querySelector('#submitMovie');

    submitBtn.addEventListener('click', event => {
        loadingGif.classList.add('is-submitted');
        recContent.classList.add('new-rec');
    })
}


document.addEventListener('DOMContentLoaded', loaded)
const loaded = () => {
    let loadingGif = document.querySelector('.loading-gif');
    let submitBtn = document.querySelector('#submit');

    submitBtn.addEventListener('click', event => {
        loadingGif.classList.add('is-submitted')
    })
}


document.addEventListener('DOMContentLoaded', loaded)
const loaded = () => {
    let loadingGif = document.querySelector('.loading-gif');
    let recContent = document.querySelector('.recommendation');
    let recIntro = document.querySelector('.recommendation-intro');
    let movieBtn = document.querySelector('#submitMovie');

    movieBtn.addEventListener('click', event => {
        loadingGif.classList.add('is-submitted');
        recContent.classList.add('new-rec');
        recIntro.classList.add('new-rec');
    })

    let thanks = document.querySelector('#feedback-thanks');
    let feedbackBtn = document.querySelector('#submitFeedback');

    if (thanks && feedbackBtn) {
        feedbackBtn.addEventListener('click', event => {
            thanks.classList.add('is-submitted');
        })        
    }
}


document.addEventListener('DOMContentLoaded', loaded)
const loaded = () => {
    let loadingGif = document.querySelector('.loading-gif');
    let recContent = document.querySelectorAll('.recommendation');
    let recIntro = document.querySelector('.recommendation-intro');
    let feedbackForm = document.querySelector('.feedback-form');
    let otherLikes = document.querySelector('.other-likes-count');
    let movieBtn = document.querySelector('#submitMovie');

    movieBtn.addEventListener('click', event => {
        loadingGif.classList.add('is-submitted');
        for (var i = 0; i < recContent.length; i++) {
           recContent[i].classList.add('new-rec');
        }
        recIntro.classList.add('new-rec');
        feedbackForm.classList.add('new-rec');
        otherLikes.classList.add('new-rec');
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
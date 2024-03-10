/*This code for Read More sectioon */

const btn = document
    .querySelector('.read-more-btn');

const text = document
    .querySelector('.card__read-more');

const cardcontents = document
    .querySelector('.services-list');

cardcontents
    .addEventListener('click', e => {

        const current = e.target;

        const isReadMoreBtn = current.className.includes('read-more-btn');

        if (!isReadMoreBtn)
            return;

        const currentText = e.target.parentNode.querySelector('.card__read-more');

        currentText.classList.toggle('card__read-more--open');

        current.textContent = current.textContent.includes('Read More...') ? 'Read Less...' : 'Read More...';

    });
/* Ending this code for Read More sectioon */
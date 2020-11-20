'use strict';

// document.querySelector('#create-bookshelf').addEventListener('submit', (event) => {
//     event.preventDefault();
//     const bookshelfName = document.querySelector('#bookshelf-name').value;
//     const bookshelfLocation = document.querySelector('#bookshelf-location');
//     const newH3 = document.createElement("h3");
//     newH3.appendChild(document.createTextNode(bookshelfName));
//     const bottomOfBookshelf = document.querySelector('#bottom-of-bookshelf');
//     document.body.insertBefore(bottomOfBookshelf, newH3)
//     (bookshelfLocation.innerHTML = bookshelfName)
// }
// );



const modal = document.getElementById('modal');
const modalContent = document.getElementById('modal-content');
const newBookshelfButton = document.getElementById('create-bookshelf-button');
const cancelButton = document.getElementById('cancel');

newBookshelfButton.addEventListener('click', function() {
  modalContent.style.display = 'flex'
  modal.style.display ='block'
  console.log('open')
});

cancelButton.addEventListener('click', function() {
  modalContent.style.display = 'none'
  modal.style.display ='none'
  console.log('closed')
});



$('#create-bookshelf').on('submit', (evt) => {
    evt.preventDefault();

    const formInput = {
    melonWaffles: $('#bookshelf-name').val()
    };

    $.post('/create-bookshelf.json', formInput, (res) => {
        const bookshelfName = res.name;
        const location = $('#bookshelf-names').prepend('<li></li>');
        $('#bookshelf-names li:first-child').html(bookshelfName);
        modalContent.style.display = 'none';
        modal.style.display ='none';
        });
});







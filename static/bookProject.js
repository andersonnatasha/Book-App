'use strict';


/// Creates modal for adding a new bookshelf
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


/// Takes user input to create new bookshelf in db and then display on page
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







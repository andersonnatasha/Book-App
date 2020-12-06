'use strict';


/// Creates modal for adding a new bookshelf
const modal = document.getElementById('modal');
const modalContent = document.getElementById('modal-content');
const newBookshelfButton = document.getElementById('create-bookshelf-button');
const cancelButton = document.getElementById('cancel');


newBookshelfButton.addEventListener('click', function() {
  modalContent.style.display = 'flex'
  modal.style.display ='block'
});

cancelButton.addEventListener('click', function() {
  modalContent.style.display = 'none'
  modal.style.display ='none'
});


/// Takes user input to create new bookshelf in db and then display on page as a link
$('#create-bookshelf').on('submit', (evt) => {
    evt.preventDefault();

    const formInput = {
    bookshelfName: $('#bookshelf-name').val()
    };

    $.post('/create-bookshelf.json', formInput, (res) => {
        const bookshelfName = res.name;
        $('#bookshelf-names').prepend('<li></li>');
        $('#bookshelf-names li:first-child').html(`<a href=${bookshelfName}-bookshelf>${bookshelfName}</a>`);
        $('#bookshelf-name').val("")
        modalContent.style.display = 'none';
        modal.style.display ='none';
        });
});

$('.book-image').on('click', (evt) => {
  const button = $(evt.target);
  const buttonId = button.attr('id');
  $('.book-description').style.display = 'block'
  // modal.style.display ='block'
});




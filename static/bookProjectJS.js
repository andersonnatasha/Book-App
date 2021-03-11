'use strict';
$('.fa-home').on('click', () => {
  const spinner = $('.spinner-border');
  const quote = $('.loading-quote');
  console.log(quote[0])
  spinner[0].style.display = "block";
  quote[0].style.display = "block";
})


$('.navbar-brand').on('click', () => {
  const spinner = $('.spinner-border');
  const quote = $('.loading-quote');
  console.log(quote[0])
  spinner[0].style.display = "block";
  quote[0].style.display = "block";
})


$('#interest-button').on('click', () => {
  const spinner = $('.spinner-border');
  const quote = $('.loading-quote');
  console.log(quote[0])
  spinner[0].style.display = "block";
  quote[0].style.display = "block";
})



/// Creates modal for adding a new bookshelf
const bookshelfModal = document.getElementById('modal');
const bookshelfModalContent = document.getElementById('modal-content');
const newBookshelfButton = document.getElementById('create-bookshelf-button');
const cancelButton = document.getElementById('cancel');


newBookshelfButton.addEventListener('click', function() {
  bookshelfModalContent.style.display = 'flex'
  bookshelfModal.style.display ='block'
});

cancelButton.addEventListener('click', function() {
  bookshelfModalContent.style.display = 'none'
  bookshelfModal.style.display ='none'
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
        $('#bookshelf-name').val("");
        bookshelfModalContent.style.display = 'none';
        modal.style.display ='none';
        });
});

$('.book-image').on('click', (evt) => {
  const button = $(evt.target);
  const buttonId = button.attr('id');
  const description = $(`#book-description${buttonId}`)
  console.log(description[0])

  description[0].style.display = 'block'

  $(description[0]).on('click', (evt) => {
    description[0].style.display = 'none'

  })
});








$('.read-button').on('click', (evt) => {
  evt.preventDefault();
  const button = $(evt.target);
  const buttonId = button.attr('id');

  const formInput = {
    title: $(`#read-book-title${buttonId}`).val(),
    subtitle: $(`#read-book-subtitle${buttonId}`).val(),
    authors: $(`#read-book-authors${buttonId}`).val(),
    image_link: $(`#read-book-image-link${buttonId}`).val(),
    categories: $(`#read-book-categories${buttonId}`).val(),
    description: $(`#read-book-description${buttonId}`).val(),
    isbn_13: $(`#read-book-isbn-13${buttonId}`).val(),
  };

  $.post('/mark-as-read', formInput, (res) => {
  $(`#read-message${formInput['isbn_13']}`).html(res).delay(1000).fadeOut(2500, 'linear' );
  })
});


$('.fa-heart').on('click', (evt) => {
  evt.preventDefault();
  const button = $(evt.target);
  const buttonId = button.attr('id');

  // $('#button').toggleClass('heart-icon-selected');

  // if (button.attr("style", "color:white")){
  //   button.attr("style", "color:green");
  if (button.hasClass('heart-icon')){
    button.removeClass('heart-icon').addClass('heart-icon-selected');}
    else{button.removeClass('heart-icon-selected').addClass('heart-icon')}


  const formInput = {
    title: $(`#liked-book-title${buttonId}`).val(),
    subtitle: $(`#liked-book-subtitle${buttonId}`).val(),
    authors: $(`#liked-book-authors${buttonId}`).val(),
    image_link: $(`#liked-book-image-link${buttonId}`).val(),
    categories: $(`#liked-book-categories${buttonId}`).val(),
    description: $(`#liked-book-description${buttonId}`).val(),
    isbn_13: $(`#liked-book-isbn-13${buttonId}`).val(),
  };

  $.post('/mark-as-liked', formInput, (res) => {
  $(`#liked-message${formInput['isbn_13']}`).html(res).fadeIn().delay(1000).fadeOut(2500, 'linear' );
  })
});


$('.to-be-read-button').on('click', (evt) => {
  evt.preventDefault();
  const button = $(evt.target);
  const buttonId = button.attr('id');


  const formInput = {
    title: $(`#to-be-read-book-title${buttonId}`).val(),
    subtitle: $(`#to-be-read-book-subtitle${buttonId}`).val(),
    authors: $(`#to-be-read-book-authors${buttonId}`).val(),
    image_link: $(`#to-be-read-book-image-link${buttonId}`).val(),
    categories: $(`#to-be-read-book-categories${buttonId}`).val(),
    description: $(`#to-be-read-book-description${buttonId}`).val(),
    isbn_13: $(`#to-be-read-book-isbn-13${buttonId}`).val(),
  };

  $.post('/mark-as-to-be-read', formInput, (res) => {
  $(`#to-be-read-message${formInput['isbn_13']}`).html(res).delay(1000).fadeOut(2500, 'linear' );
  })
});



$('.add-to-bookshelf').on('submit', (evt) => {
  evt.preventDefault();
  const button = $(evt.target);
  const buttonId = button.attr('id');

  const modal = $(`#modal-bookshelf${buttonId}`);
  const modalContent = $(`#modal-content-bookshelf${buttonId}`);
  const cancelButton = $(`#cancel${buttonId}`);


  modalContent[0].style.display = 'flex';
  modal[0].style.display ='block';

  cancelButton.on('click', () => {
    modalContent[0].style.display = 'none'
    modal[0].style.display ='none'
  });

  const formInput = {
    title: $(`#add-to-bookshelf-title${buttonId}`).val(),
    subtitle: $(`#add-to-bookshelf-subtitle${buttonId}`).val(),
    authors: $(`#add-to-bookshelf-authors${buttonId}`).val(),
    image_link: $(`#add-to-bookshelf-image-link${buttonId}`).val(),
    categories: $(`#add-to-bookshelf-categories${buttonId}`).val(),
    description: $(`#add-to-bookshelf-description${buttonId}`).val(),
    isbn_13: $(`#add-to-bookshelf-isbn-13${buttonId}`).val(),
    bookshelf_name: $(`#add-to-bookshelf-name${buttonId}`).val(),
  };

  console.log(formInput['bookshelf_name']);

  $(`#book-on-bookshelf-status${buttonId}`).on('click', formInput, (evt) => {
    evt.preventDefault();
    const target = $(evt.target)

  formInput['book_tag'] = target.val();

    console.log(target)
    console.log(formInput['book_tag']);
    console.log(buttonId);

  if (formInput['book_tag'] !== 'cancel') {
    $.post('/handle-adding-book-to-bookshelf', formInput, (res) => {
      $(`#add-to-bookshelf-message${formInput['isbn_13']}`).html(res).delay(1000).fadeOut(2500, 'linear' );
      modalContent[0].style.display = 'none';
      modal[0].style.display ='none';
      $(".dropdown-menu show").removeClass(".show");
    })
  }
});
});


const bookRows = document.querySelectorAll('.book-row');
const bookCols = document.querySelectorAll('.book-col');

let bookCounter = 0
for (const bookRow of bookRows){
  let bookColCounter = 0;
  while (bookColCounter < 4 && bookCols[bookCounter] !== undefined) {
    bookRow.append(bookCols[bookCounter]);
    bookColCounter += 1;
    bookCounter +=1;
  }
}

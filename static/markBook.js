'use strict';

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


$('.heart-icon').on('click', (evt) => {
  evt.preventDefault();
  const button = $(evt.target);
  const buttonId = button.attr('id');

  if (button[0].style === "color: green"){
    (button[0].style = "color: white");
    console.log("first condition");
    console.log(button[0]);
  } else {
      button[0].style = "color:green";
      console.log("first condition");
  };


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


  modalContent[0].style.display = 'flex'
  modal[0].style.display ='block'

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

'use strict';

$('.mark-as-read').on('submit', (evt) => {
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
  $(`#read-message${formInput['isbn_13']}`).html(res);
  console.log($('.read-book-isbn-13').val());
  })
});


$('.mark-as-liked').on('submit', (evt) => {
  evt.preventDefault();
  const button = $(evt.target);
  const buttonId = button.attr('id');

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
  $(`#liked-message${formInput['isbn_13']}`).html(res);
  console.log($('.liked-book-isbn-13').val());
  })
});


$('.mark-as-to-be-read').on('submit', (evt) => {
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
  $(`#to-be-read-message${formInput['isbn_13']}`).html(res);
  console.log($('.to-be-read-book-isbn-13').val());
  })
});



/////




$('.add-to-bookshelf').on('submit', (evt) => {
  evt.preventDefault();
  const button = $(evt.target);
  const buttonId = button.attr('id');

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

  console.log(formInput);
  console.log(formInput['bookshelf_name']);

  const modal = $(`#modal-bookshelf${buttonId}`);
  const modalContent = $(`#modal-content-bookshelf${buttonId}`);
  const bookshelfName = $(`#bookshelf-name${buttonId}`);
  const cancelButton = $('#cancel');

  console.log(modal)


  modalContent[0].style.display = 'flex'
  modal[0].style.display ='block'

  cancelButton.on('click', () => {
    modalContent[0].style.display = 'none'
    modal[0].style.display ='none'
  });


  $(`#bookshelf-name${buttonId}`).on('submit', formInput, (evt) => {
    evt.preventDefault();

    const modalFormInput = {
      book_tag: $(`#read-book-on-bookshelf${buttonId}`).val()
    };

    console.log(modalFormInput['book_tag']);
    console.log(buttonId);
    console.log(modalFormInput)
  }
  )


  $.post('/add-book-to-bookshelf', formInput, (res) => {
    $(`#add-to-bookshelf-message${formInput['isbn_13']}`).html(res);
  console.log($('.add-to-bookshelf-isbn-13').val());
  })
});



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
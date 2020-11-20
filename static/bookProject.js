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




$('#create-bookshelf').on('submit', (evt) => {
    evt.preventDefault();

    const formInput = {
    melonWaffles: $('#bookshelf-name').val()
    };

    $.post('/create-bookshelf.json', formInput, (res) => {
        const newDiv = $('#bottom-of-bookshelf').append(res.name);
        // const newH3 = $newDiv.append('h3');
        // newH3.after(res.name)
        });
});




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
  console.log(modal)



// document.querySelector('#create-bookshelf-button').addEventListener('click', (event) => {
//    console.log('hi');
// }

// $('#create-bookshelf-button').on('click', (evt) => {

//   $('#create-bookshelf-modal').showModal()

//   const formInput = {
//   melonWaffles: $('#bookshelf-name').val()
//   };

//   $.post('/create-bookshelf.json', formInput, (res) => {
//       const newDiv = $('#bottom-of-bookshelf').append(res.name);
//       // const newH3 = $newDiv.append('h3');
//       // newH3.after(res.name)
//       });
// });




// $.get('https://pokeapi.co/api/v2/berry/', (res) => {
//   const berryNames = [];
//   for (const berry of res.results) {
//     berryNames.push(berry.name);
//   }

//   $('#berries').append(berryNames.join(', '));
// });


/// could loop on 36, and for each thing looped over could append or make children to the H3 div.


/// could prepopulate the page.
///Could load stuff into HTML page.
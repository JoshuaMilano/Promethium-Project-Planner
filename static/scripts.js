lucide.createIcons();

// Const variables
const idOfBoard = window.location.pathname.split('/').pop();
// Board
const createBoardButton = document.getElementById('prm-create-board-button');
const deleteBoardButton = document.getElementById('delete-board-button');
const activeBoardTab = document.getElementById('ActiveBoardTab');
const boardTitle = document.getElementById('prm-board-title');
// List
const addListBtn = document.getElementById('add-list-btn');
// List and Cards
const listContainer = document.getElementById('prm-list-container');

// Listeners
if (createBoardButton) createBoardButton.addEventListener('click', createBoard);
if (deleteBoardButton) deleteBoardButton.addEventListener('click', deleteBoard);
// Board
if (boardTitle) {
    boardTitle.addEventListener('keydown', boardTitleEnterSupport);
    boardTitle.addEventListener('blur', updateTitle);
}
// List
if (addListBtn) addListBtn.addEventListener('click', createList);
// List and Cards
if (listContainer) {
    listContainer.addEventListener('click', handleListContainerButtons);
    listContainer.addEventListener('keydown', boardEnterSupport);
    listContainer.addEventListener('focusout', handleBoardEdits);
}
// Functions for board

function handleListContainerButtons(event) {
    // Handle Create Card Buttons
    if (event.target.closest('.add-card-button')) {
        createCard(event);
    }

    // Handle Delete List Buttons
    if (event.target.closest('.prm-delete-list-button')) {
        deleteList(event);
    }

    // Handle Delete Card Buttons
    if (event.target.closest('.prm-delete-card-button')) {
        deleteCard(event);
    }
}


function createBoard() {
    fetch('/api/create_board', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = `/board/${data.new_board_id}`;
        } else {
            console.error('Failed to create board')
        }
    })
}

function createList() {
    fetch('/api/add_list', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            board_id: idOfBoard // ID of board (pulled from URL)
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const newListId = data.new_id;

            const newListHTML = `
                <div class="prm-list" data-list-id="${newListId}">
                    <h2 class="prm-list-title" spellcheck="false" contenteditable="true">New List</h2>
                    <button class="prm-delete-list-button"><i data-lucide="x"></i></button>
                    <div class="prm-card-container">
                        <button class="prm-button add-card-button">Add Card</button>
                    </div>
                </div>
            `;
            addListBtn.insertAdjacentHTML('beforebegin', newListHTML);
            lucide.createIcons();
        } else {
            console.error('Failed to create list');
        }
    });
}

function createCard(event) {
    const listElement = event.target.closest('.prm-list');
    const listId = listElement.getAttribute('data-list-id');
    
    fetch('/api/add_card', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            board_id: idOfBoard,
            column_id: listId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const newCardId = data.new_id;
            
            const newCardHTML = `
            <div class="prm-card" data-card-id="${newCardId}">
            <p class="prm-card-content" spellcheck = "false" contenteditable="true">New Card!</p>
            <button class="prm-delete-card-button"><i data-lucide="x"></i></button>
            </div>
            `
            event.target.insertAdjacentHTML('beforebegin', newCardHTML);
            lucide.createIcons();
        } else {
            console.error('Card not added');
        }
    });
}

function deleteBoard() {
    fetch('/api/delete_item', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            item_id: idOfBoard,
            table_name: 'boards'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/';
        } else {
            console.error('Yeah, that didn\'t work');
        }
    });
}

function deleteList(event) {
    // Grab the list
    const listElement = event.target.closest('.prm-list');

    // Fetch the delete request
    fetch('/api/delete_item', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            item_id: listElement.getAttribute('data-list-id'),
            table_name: 'lists'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            listElement.remove();
        } else {
            console.error('Couldn\'t delete list');
        }
    });
}

function deleteCard(event) {
    // Grab the list
    const cardElement = event.target.closest('.prm-card');

    // Fetch the delete request
    fetch('/api/delete_item', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            item_id: cardElement.getAttribute('data-card-id'),
            table_name: 'cards'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            cardElement.remove();
        } else {
            console.error('Couldn\'t delete card');
        }
    });
}

function updateTitle() {
    // Clean Title
    let newContent = sanitizeTitle(this.innerText.trim(), 'Untitled Board');
    this.innerText = newContent;
    activeBoardTab.innerText = newContent;

    // Update the board title
    fetch('/api/update_board', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            element: 'boards', // Name of the Element (Board, List, or card) // NOTE: Update this variable to table
            item_id: idOfBoard, // ID of board (pulled from URL)
            board_id: idOfBoard, // ID of board (pulled from URL)
            field: 'title', // Field in DB to update
            value: this.innerText // Value to  replace field with
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Title Successfully Updated');
        }
    });
}

function handleBoardEdits(event) {
    if (event.target.classList.contains('prm-list-title')) {
        
        const listElement = event.target.closest('.prm-list');
        const listId = listElement.getAttribute('data-list-id');
        let newContent = sanitizeTitle(event.target.innerText.trim(), 'Untitled List');
        event.target.innerText = newContent;

        console.log('List title was clicked');

        fetch('/api/update_board', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                element: 'lists',
                item_id: listId,
                board_id: idOfBoard,
                field: 'title',
                value: newContent
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Title successfully updated');
            } else {
                console.error('Yeah, it\'s broke :(');
            }
        });
    }
    if (event.target.classList.contains('prm-card-content')) {
        
        const cardElement = event.target.closest('.prm-card');
        const cardId = cardElement.getAttribute('data-card-id');
        // let newContent = sanitizeTitle(event.target.innerText.trim(), 'Untitled List');
        // event.target.innerText = newContent;

        console.log('card title was clicked');

        fetch('/api/update_board', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                element: 'cards',
                item_id: cardId,
                board_id: idOfBoard,
                field: 'content',
                value: event.target.innerText.trim()
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Title successfully updated');
            } else {
                console.error('Yeah, it\'s broke :(');
            }
        });
    }
}

// Enter (keyboard) support
function boardTitleEnterSupport(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        event.target.blur();
    }
}

function boardEnterSupport(event) {
    const element = event.target;
    if (element.classList.contains('prm-list-title') || element.classList.contains('prm-card-content')) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            element.blur();
        }
    }
}

// TODO: Remove console.logs - They exists for debug purposes ONLY.
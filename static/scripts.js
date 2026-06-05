// Event listeners for the board
document.getElementById('prm-board-title').addEventListener('blur', updateTitle);

// Functions for board
function updateTitle() {
    let cleanText = this.innerText.trim();

    this.innerText = newText === '' ? 'Untitled Board' : cleanText
}
import streamlit as st
import chess
import chess.svg
from chess import Board
from streamlit.components.v1 import html

# Function to render the chess board using SVG
def render_board(board, selected_square=None):
    arrows = []
    if selected_square is not None:
        # Draw arrows for all legal moves from the selected square
        arrows = [(selected_square, move.to_square) for move in board.legal_moves if move.from_square == selected_square]
    svg = chess.svg.board(board=board, size=400, arrows=arrows)
    html(f'<div style="display: flex; justify-content: center;">{svg}</div>', height=420)

# Function to handle square selection
def handle_square_click(square):
    if 'selected_square' not in st.session_state:
        # If no square is selected, select the clicked square
        st.session_state.selected_square = square
    else:
        # If a square is already selected, try to make a move
        move = chess.Move(st.session_state.selected_square, square)
        if move in st.session_state.board.legal_moves:
            st.session_state.board.push(move)
            st.session_state.selected_square = None  # Clear selection after move
        else:
            # If the move is invalid, select the new square instead
            st.session_state.selected_square = square

# Initialize the chess board
if 'board' not in st.session_state:
    st.session_state.board = chess.Board()

# Title and description
st.title("Interactive Chess Game")
st.write("Click on a piece to select it, then click on the destination square to make a move.")

# Display the chess board
render_board(st.session_state.board, st.session_state.get('selected_square'))

# JavaScript to handle square clicks
square_click_js = """
<script>
function sendSquareClick(squareId) {
    // Send the square ID to Streamlit
    window.parent.postMessage({type: 'squareClick', squareId: squareId}, '*');
}

document.addEventListener('DOMContentLoaded', () => {
    const svgElement = document.querySelector('svg');
    svgElement.querySelectorAll('rect[data-square-id]').forEach(rect => {
        rect.addEventListener('click', () => {
            const squareId = rect.getAttribute('data-square-id');
            sendSquareClick(squareId);
        });
    });
});
</script>
"""
html(square_click_js)

# Handle square clicks from JavaScript
if 'square_click' in st.session_state:
    handle_square_click(st.session_state.square_click)
    del st.session_state.square_click

# Sidebar for controls
with st.sidebar:
    st.header("Controls")
    if st.button("Reset Board"):
        st.session_state.board.reset()
        st.session_state.selected_square = None
        st.success("Board reset!")

    if st.button("Undo Last Move"):
        if len(st.session_state.board.move_stack) > 0:
            st.session_state.board.pop()
            st.session_state.selected_square = None
            st.success("Last move undone!")
        else:
            st.warning("No moves to undo!")

# Display game status
if st.session_state.board.is_checkmate():
    st.error("Checkmate! Game over.")
elif st.session_state.board.is_stalemate():
    st.warning("Stalemate! Game over.")
elif st.session_state.board.is_insufficient_material():
    st.warning("Insufficient material! Game over.")
elif st.session_state.board.is_check():
    st.info("Check!")
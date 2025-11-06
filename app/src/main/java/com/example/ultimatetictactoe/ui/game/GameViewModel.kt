package com.example.ultimatetictactoe.ui.game

import androidx.lifecycle.ViewModel
import com.example.ultimatetictactoe.domain.model.Game
import com.example.ultimatetictactoe.domain.model.Player
import com.example.ultimatetictactoe.domain.model.WinningLine
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.update

class GameViewModel : ViewModel() {

    private val _gameState = MutableStateFlow(Game())
    val gameState: StateFlow<Game> = _gameState

    fun onCellClicked(smallBoardIndex: Int, cellIndex: Int) {
        _gameState.update { currentState ->
            if (currentState.winner != null || currentState.board.flatten().all { it != null }) {
                return@update currentState
            }

            if (currentState.board[smallBoardIndex][cellIndex] != null) {
                return@update currentState
            }
            if (currentState.activeSmallBoard != null && currentState.activeSmallBoard != smallBoardIndex) {
                return@update currentState
            }

            val newBoard = currentState.board.map { it.toMutableList() }.toMutableList()
            val currentPlayer = currentState.currentPlayer
            newBoard[smallBoardIndex][cellIndex] = currentPlayer

            val (newStreaks, updatedLines) = checkForNewStreaks(
                smallBoard = newBoard[smallBoardIndex],
                existingLines = currentState.winningLines[smallBoardIndex],
                player = currentPlayer
            )

            val newWinningLines = currentState.winningLines.toMutableList()
            newWinningLines[smallBoardIndex] = updatedLines

            val newXScore = if (currentPlayer == Player.X) currentState.xScore + newStreaks else currentState.xScore
            val newOScore = if (currentPlayer == Player.O) currentState.oScore + newStreaks else currentState.oScore

            val isBoardFull = newBoard.flatten().all { it != null }
            val gameWinner = if (isBoardFull) {
                when {
                    newXScore > newOScore -> Player.X
                    newOScore > newXScore -> Player.O
                    else -> null
                }
            } else {
                null
            }

            val nextPlayer = if (currentPlayer == Player.X) Player.O else Player.X
            val isNextBoardFull = newBoard.getOrNull(cellIndex)?.all { it != null } ?: true
            val nextActiveBoard = if (isBoardFull || isNextBoardFull) null else cellIndex

            currentState.copy(
                board = newBoard,
                currentPlayer = nextPlayer,
                activeSmallBoard = nextActiveBoard,
                xScore = newXScore,
                oScore = newOScore,
                winningLines = newWinningLines,
                winner = gameWinner
            )
        }
    }

    private fun checkForNewStreaks(
        smallBoard: List<Player?>,
        existingLines: List<WinningLine>,
        player: Player
    ): Pair<Int, List<WinningLine>> {
        val winningCombinations = listOf(
            listOf(0, 1, 2), listOf(3, 4, 5), listOf(6, 7, 8),
            listOf(0, 3, 6), listOf(1, 4, 7), listOf(2, 5, 8),
            listOf(0, 4, 8), listOf(2, 4, 6)
        )

        var newStreaksCount = 0
        val allLines = existingLines.toMutableList()

        for (combination in winningCombinations) {
            val (c1, c2, c3) = combination
            if (smallBoard[c1] == player && smallBoard[c2] == player && smallBoard[c3] == player) {
                val newLine = WinningLine(c1, c3)
                if (!allLines.contains(newLine)) {
                    allLines.add(newLine)
                    newStreaksCount++
                }
            }
        }
        return Pair(newStreaksCount, allLines)
    }
}
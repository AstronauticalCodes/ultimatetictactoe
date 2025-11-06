package com.example.ultimatetictactoe

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import com.example.ultimatetictactoe.ui.game.GameScreen
import com.example.ultimatetictactoe.ui.theme.UltimateTicTacToeTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            UltimateTicTacToeTheme {
                Scaffold(
                    modifier = Modifier
                        .fillMaxSize()
                ) {
                    Box {
                        Image(
                            painter = painterResource(id = R.drawable.game_background),
                            contentDescription = "Background",
                            contentScale = ContentScale.FillHeight,
                            modifier = Modifier
                                .fillMaxHeight()
                        )

                        Box(
                            modifier = Modifier
                                .padding(it)
                        ) {
                            GameScreen()
                        }
                    }
                }
            }
        }
    }
}
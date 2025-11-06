package com.example.ultimatetictactoe.ui.game

import android.content.Context
import android.media.AudioAttributes
import android.media.SoundPool
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.platform.LocalContext
import com.example.ultimatetictactoe.R

class GameSounds(
    val tap: Int,
    val score: Int,
    val win: Int
)

@Composable
fun rememberSoundPlayer(): SoundPlayer {
    val context = LocalContext.current

    val soundPlayer = remember {
        SoundPlayer(context)
    }

    DisposableEffect(Unit) {
        onDispose {
            soundPlayer.release()
        }
    }

    return soundPlayer
}

class SoundPlayer(context: Context) {

    private val soundPool: SoundPool
    private var sounds: GameSounds? = null

    init {
        val audioAttributes = AudioAttributes.Builder()
            .setUsage(AudioAttributes.USAGE_GAME)
            .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
            .build()

        soundPool = SoundPool.Builder()
            .setMaxStreams(3)
            .setAudioAttributes(audioAttributes)
            .build()

        sounds = GameSounds(
            tap = soundPool.load(context, R.raw.tap_sound, 1),
            score = soundPool.load(context, R.raw.score_sound, 1),
            win = soundPool.load(context, R.raw.win_sound, 1)
        )
    }

    fun playTap() {
        sounds?.tap?.let { soundPool.play(it, 1.0f, 1.0f, 0, 0, 1.0f) }
    }

    fun playScore() {
        sounds?.score?.let { soundPool.play(it, 0.8f, 0.8f, 0, 0, 1.0f) }
    }

    fun playWin() {
        sounds?.win?.let { soundPool.play(it, 1.0f, 1.0f, 0, 0, 1.0f) }
    }

    fun release() {
        soundPool.release()
    }
}
[app]
title = FishingGame
package.name = fishing_game
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,mp3,ogg,wav
version = 1.0
orientation = portrait
fullscreen = 1

main.py = main.py

requirements = python3, pygame

android.entrypoint = org.kivy.android.PythonActivity

android.minapi = 21
android.sdk = 34
android.ndk = 25b

android.archs = arm64-v8a, armeabi-v7a

android.add_libs_armeabi = libs/

android.presplash_color = #000000
android.presplash_lottie = 

[buildozer]
log_level = 2
warn_on_root = 1

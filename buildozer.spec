[app]
title = Fishing Game
package.name = fishinggame
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3,wav

version = 0.1
requirements = python3,pygame,kivy
osx.python_version = 3
osx.kivy_version = 1.9.1

fullscreen = 0
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 1

[app]
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Pygame specific settings
android.entrypoint = main.main

# Build settings
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 28

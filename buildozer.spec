[app]
title = Fishing Game
package.name = fishinggame
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3,wav

version = 0.1
requirements = python3,pygame,kivy

fullscreen = 0
orientation = portrait

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21

[buildozer]
log_level = 2

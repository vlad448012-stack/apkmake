[app]
title = Tetris
package.name = tetris
package.domain = org.example

source.dir = ./
source.include_exts = py,png,jpg,kv,atlas

version = 0.1
requirements = python3,kivy

orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.1.0

# Ключевые настройки для Android
android.permissions = INTERNET
android.ndk = 23b
android.sdk = 30
android.api = 30
android.minapi = 21
android.gradle_dependencies =

# Отключаем лишнее для ускорения сборки
android.archs = armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1

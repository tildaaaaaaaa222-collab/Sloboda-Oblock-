[app]

title = Sloboda Oblock
package.name = slobodaoblock
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,mp3,ogg,wav
source.exclude_dirs = .github, bin, .buildozer

version = 0.1

requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 1

icon.filename = %(source.dir)s/icon.png

android.accept_sdk_license = True
android.skip_update = False

android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 24
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.permissions = INTERNET

android.logcat_pid = False
android.debug = True

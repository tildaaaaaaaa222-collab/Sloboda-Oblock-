[app]
title = Sloboda Oblok
package.name = slobodaoblock
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

android.accept_sdk_license = True
android.skip_update = False

version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 1

android.api = 33
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

android.add_src = bg.jpg

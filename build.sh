python3.11 setup.py py2app --packages=imp,panda3d --arch=universal2

cp -R ./models ./dist/mincraft.app/Contents/Resources/
cp -R ./assets ./dist/mincraft.app/Contents/Resources/
cp -R ./modules ./dist/mincraft.app/Contents/Resources/

dist/mincraft.app/Contents/MacOS/mincraft
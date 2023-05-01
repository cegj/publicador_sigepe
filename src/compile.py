import PyInstaller.__main__

PyInstaller.__main__.run([
    'app.py',
    '--onefile',
    '--noconsole',
    '--windowed',
    # '--add-data',
    # '../config;config',
    '--clean',
    '--icon=ico.ico',
    '--name=Publicador Sigepe',
])
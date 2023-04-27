import PyInstaller.__main__

PyInstaller.__main__.run([
    'src/app.py',
    '--onefile',
    '--console',
    '--clean',
    '--icon=ico.ico',
    '--name=Publicador Sigepe',
])
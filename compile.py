import PyInstaller.__main__

PyInstaller.__main__.run([
    'src/app.py',
    '--onefile',
    '--hidden-import ',
    '--console',
    '--clean',
    '--icon=ico.ico',
    '--name=Publicador Sigepe',
])
import PyInstaller.__main__

PyInstaller.__main__.run([
    'publicador.py',
    '--onefile',
    '--console',
    '--clean',
    '--icon=ico.ico',
    '--name=publicador',
])
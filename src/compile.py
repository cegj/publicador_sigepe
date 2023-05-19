import PyInstaller.__main__

PyInstaller.__main__.run([
    'app.py',
    # '--onefile',
    '--noconsole',
    '--clean',
    '--icon=../static/ico.ico',
    '--name=publicador_sigepe',
])
from views import Login as l
from controllers import CheckUpdates as c

class Application:
    def __init__(self):
      pass

    def executar(self):
      c.CheckUpdates.checkRelease()
      start = l.Login()

app = Application()
app.executar()
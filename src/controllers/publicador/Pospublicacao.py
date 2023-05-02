import os
import shutil

class Pospublicacao:
  @staticmethod
  def renomearArquivo(file, term):
    try:
      directory = os.path.dirname(file.name)
      filename = os.path.basename(file.name)
      filenameArray = filename.split('.', 1)
      filenameWithoutExt = filenameArray[0]
      extension = filenameArray[1]
      newFilename = str(filenameWithoutExt + " " + term + '.' + extension)
      file_oldname = os.path.join(directory, filename)
      file_newname = os.path.join(directory, newFilename)
      os.rename(file_oldname, file_newname)
      return [True, newFilename]
    except Exception as e:
      return [False, e]

  @staticmethod
  def copiarMoverArquivo(file, action, targetDirectory, newFilename = None):
    try:
      originDirectory = os.path.normcase(os.path.dirname(file.name))
      targetDirectory = os.path.normcase(targetDirectory)
      filename = os.path.basename(file.name)
      origin = os.path.join(originDirectory, newFilename if (newFilename != None) else filename)
      target = os.path.join(targetDirectory, newFilename if (newFilename != None) else filename)

      if (action == "Mover para..."):
          shutil.move(origin, target)
          return [True, targetDirectory]
      elif (action == "Copiar para..."):
          shutil.copy(origin, target)
          return [True, targetDirectory]
      else:
          raise Exception("A ação para pós-publicação definida é inválida (diferente de copiar ou mover)")

    except Exception as e:
      print(e)
      return [False, e]

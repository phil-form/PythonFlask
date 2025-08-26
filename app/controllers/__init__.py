import os
import glob

# Si vous voulez comprendre le principe décommenter les trois lignes suivantes
# print(glob.glob(os.path.dirname(__file__))
# print(glob.glob(os.path.dirname(__file__) + "/*.py")
# print([os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + "/*.py")])
# tu vas sélectionner tous les fichiers .py dans le dossier actuel
# et tu les mets dans un tableau en supprimant l'extension .py ([:-3])
# et je place ce tableau dans __all__ qui sera importer quand je fais un
# from module_name import *
# exemple :
# module/
#       user.py
#       product.py
# résultat => ['user', 'product']
__all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + "/*.py")]
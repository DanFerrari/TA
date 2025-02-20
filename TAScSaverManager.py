import shutil
from glob import glob

import os


class TAScSaverPicsUpdate(object):
    """ """

    def __init__(self):
        """ """

        self._mediaList = glob("/media/eyetec/*")
        self._mediaList.sort()

    def checkPicsDirectory(self):
        """
        Arguments:
        - `self`:
        """
        print("entraou")
        for media in self._mediaList:

            if os.path.isdir(media + "/Eyetec-TA/Imagens"):
                if not os.path.isdir(media + "/Eyetec-TA/Imagens-backup"):
                    os.system("mkdir -p %s" % (media + "/Eyetec-TA/Imagens-backup"))

                # back up
                src_files = os.listdir("/home/eyetec/Pictures/")
                for file_name in src_files:
                    full_file_name = os.path.join("/home/eyetec/Pictures/", file_name)
                    if os.path.isfile(full_file_name):
                        shutil.copy(full_file_name, media + "/Eyetec-TA/Imagens-backup")

                # removing pics
                file_list = glob("/home/eyetec/Pictures/*")
                for f in file_list:
                    os.remove(f)

                # refreshing the screensaver pics
                src_files = os.listdir(media + "/Eyetec-TA/Imagens")
                for file_name in src_files:
                    full_file_name = os.path.join(
                        media + "/Eyetec-TA/Imagens", file_name
                    )
                    if os.path.isfile(full_file_name):
                        shutil.copy(full_file_name, "/home/eyetec/Pictures/")

                os.system("xscreensaver-command -restart")
                os.system("sudo sync")

                return True

        return False


if __name__ == "__main__":
    sc = TAScSaverPicsUpdate()
    sc.checkPicsDirectory()

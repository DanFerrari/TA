from glob import glob

import os


class TADisplayImage(object):
    """ """

    def __init__(self):
        """ """

        self._mediaList = glob("/media/eyetec/*")
        self._mediaList.sort()
        self.picsDirectory = None

    def checkPicsDirectory(self):
        """
        Arguments:
        - `self`:
        """

        for media in self._mediaList:
            if os.path.isdir(media + "/Eyetec-TA/Slides"):
                self.picsDirectory = media + "/Eyetec-TA/Slides"
                return True

        return False


if __name__ == "__main__":
    sc = TADisplayImage()
    sc.checkPicsDirectory()

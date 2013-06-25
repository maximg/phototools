import os
import sys
import datetime
import time
from collections import defaultdict
import shutil

def is_video(aFile):
    extension = os.path.splitext(aFile)[1]
    return extension.lower() == ".mp4"  # todo

def make_thumbnails(aFile, destdir):
    print "Generating thumbnails for %s" % (aFile)

def make_all_thumbnails(sourcedir, destdir):
    for root, subFolders, files in os.walk(sourcedir):
        for aFile in files:
            if is_video(aFile):
                fullpath = os.path.join(root, aFile)
                make_thumbnails(fullpath, destdir)
                #print "%s has file %s, mod date %s" % (root, ff, mod_date)

def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise
                    
if __name__ == "__main__":
    rootroot = "c:\\Users\\golov\\Documents"
    #rootroot = "d:\\Projects"
    root = rootroot + "\\GitHub\\phototools\\test\\make_thumbnails"
    workdir = os.path.join(root, "workdir")
    if os.path.exists(workdir):
        shutil.rmtree(workdir, onerror=onerror)
    time.sleep(0.2) # race condition with removing the tree above
    os.makedirs(workdir)
    for dir in ("source", "dest"):
        shutil.copytree(os.path.join(root, dir), os.path.join(workdir, dir))

    make_all_thumbnails(
        os.path.join(workdir, "source"),
        os.path.join(workdir, "dest"))

    if False:
        if not compare_tree( workdir, os.path.join(root, "expected")):
            print "ERROR: test failed"

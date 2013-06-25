import os
import sys
import datetime
from collections import defaultdict
import shutil

def is_video(aFile):
    extension = os.path.splitext(filename)[1]
    return extension.toLower == ".mp4"  # todo

def make_thumbnails(aFile, destdir):
    print "Generating thumbnails for %s" % (aFile)

def make_all_thumbnails(sourcedir, destdir):
    for root, subFolders, files in os.walk(sourcedir):
        for aFile in files:
            if is_video(aFile):
                fullpath = os.path.join(root, aFile)
                make_thumbnails(fullpath, destdir)
                #print "%s has file %s, mod date %s" % (root, ff, mod_date)
	
if __name__ == "__main__":
    root = "c:\\Users\\golov\\Documents\\GitHub\\phototools\\test\\make_thumbnails"
    workdir = os.path.join(root, "workdir")
    shutil.rmtree(workdir)
    for dir in ("source", "dest"):
        shutil.copytree(os.path.join(root, dir), os.path.join(workdir, dir))

    make_all_thumbnails(
        os.path.join(workdir, "source"),
        os.path.join(workdir, "dest"))

	if False:
		if not compare_tree( workdir, os.path.join(root, "expected")):
			print "ERROR: test failed"

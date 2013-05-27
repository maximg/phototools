import os
import sys
import datetime
from collections import defaultdict
import shutil
from PIL import Image

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

def capture_date(filename):
    img = Image.open(filenae)
    exif_data = img._getexif()
    return exif_data[36867]
    
def is_media(filename):
    extension = os.path.splitext(filename)[1]
    return extension == ".jpg"  # todo
    
def select_media_group_by_capture_date(rootdir):
    groups = defaultdict(list)
    for root, subFolders, files in os.walk(rootdir):
        for ff in files:
            if is_media(ff):
                full_path = os.path.join(root, ff)
                mod_date =  capture_date(full_path).strftime("%Y%m%d")
                #print "%s has file %s, mod date %s" % (root, ff, mod_date)
                groups[mod_date].append(full_path)
    return groups

def safe_move_file(target, full_path):
    root, basename = os.path.split(full_path)
    if os.path.exists( os.path.join(target, basename) ):
        print "ERROR: %s already exists in %s, skipped" % (basename, target)
        return
    shutil.move(target, full_path)
    
def move_files(target, files):
    print "Moving files to %s..." % (target)
    if not os.path.exists(target): 
        os.makedirs(target)
    elif not os.path.isdir(target):
        print "ERROR: %s already exists but not a directory" % (target)
        return
    for ff in files:
        safe_move_file(target, ff)

def group_media_by_capture_date(source, dest):
    groups = select_media_group_by_capture_date(source)
    for folder in groups.keys():
        move_files(os.path.join(dest, folder), groups[folder])

def compare_tree(pathA, pathB):
    #todo
    return false

if __name__ == "__main__":
    root = "d:\\Projects\\GitHub\\phototools\\test\\group_by_capture_date"
    workdir = os.path.join(root, "workdir")
    shutil.rmtree(workdir)
    for dir in ("source", "dest"):
        shutil.copytree(os.path.join(root, dir), os.path.join(workdir, dir))

    group_media_by_capture_date(
        os.path.join(workdir, "source"),
        os.path.join(workdir, "dest"))

    if not compare_tree( workdir, os.path.join(root, "expected")):
        print "ERROR: test failed"

import os
import sys
import datetime
import time
import glob
from collections import defaultdict
import shutil
from PIL import Image


total_files = 0
total_ok = 0
total_skipped = 0

def report_job(source, target):
    print "--------------------------------------"
    print "Grouping files by shoot date"
    print "Source:  %s" % (source)
    print "Target:  %s" % (target)
    print "--------------------------------------"

def report_processed_file(full_path, target, result):
    print "    %s -> %s .... %s" % (basename(full_path), basename(target), "OK" if result else "skipped")
    global  total_ok, total_skipped
    if result:
        total_ok += 1
    else:
        total_skipped += 1

def report_file(filename):
    global total_files
    total_files += 1
    
def report_totals():
    print "--------------------------------------"
    print "    Total:    %d" % (total_files)
    print "    OK:       %d" % (total_ok)
    print "    Skipped:  %d" % (total_skipped)
    print "    Extra:    %d" % (total_files - total_ok - total_skipped)
    print ""


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

def capture_date(filename):
    img = Image.open(filename)
    exif_data = img._getexif()
    return datetime.datetime.strptime(exif_data[36867],"%Y:%m:%d %H:%M:%S")
    
def is_jpg(filename):
    extension = os.path.splitext(filename)[1]
    #print "file: %s ext: %s" % (filename, extension)
    if extension.lower() == ".jpg":
        return True
    
def select_media_group_by_capture_date(rootdir):
    groups = defaultdict(list)
    for root, subFolders, files in os.walk(rootdir):
        for ff in files:
            if is_jpg(ff):
                full_path = os.path.join(root, ff)
                mod_date =  capture_date(full_path).strftime("%Y%m%d")
                #print "%s has file %s, mod date %s" % (root, ff, mod_date)
                groups[mod_date].append(full_path)
            report_file(ff)
    return groups

def safe_move_file(full_path, target):
    #print "safe move: file %s, target %s" % (full_path, target)
    root, basename = os.path.split(full_path)
    if os.path.exists( os.path.join(target, basename) ):
        return False
    shutil.move(full_path, target)
    return True

def basename(full_path):
    return os.path.split(full_path)[1]

def copy_all(fullpath, target):
    for aFile in glob.glob(os.path.splitext(fullpath)[0] + ".*"):
        if (os.path.isfile(aFile)):
            res = safe_move_file(aFile, target)
            report_processed_file(aFile, target, res)

def move_files(files, target):
    #print "Moving files to %s..." % (target)
    if not os.path.exists(target): 
        os.makedirs(target)
    elif not os.path.isdir(target):
        print "ERROR: %s already exists but not a directory" % (target)
        return
    for aFile in files:
        copy_all(aFile, target)

def group_media_by_capture_date(source, dest):
    report_job(source, dest)
    groups = select_media_group_by_capture_date(source)
    for folder in groups.keys():
        move_files(groups[folder], os.path.join(dest, folder))
    report_totals()

def compare_tree(pathA, pathB):
    #todo
    return False

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
        
def runTest():
    root = "d:\\Projects\\GitHub\\phototools\\test\\group_by_capture_date"
    workdir = os.path.join(root, "workdir")
    if os.path.exists(workdir):
        shutil.rmtree(workdir, onerror=onerror)
    time.sleep(0.2)
    os.makedirs(workdir)
    for dir in ("source", "dest"):
        shutil.copytree(os.path.join(root, dir), os.path.join(workdir, dir))

    group_media_by_capture_date(
        os.path.join(workdir, "source"),
        os.path.join(workdir, "dest"))

    if not compare_tree( workdir, os.path.join(root, "expected")):
        print "ERROR: test failed"
    
if __name__ == "__main__":
    if 1 == 0:
        runTest()
        exit
    if len(sys.argv) < 3:
        print "Usage: group_by_date.py source_folder dest_folder"
        exit()
        
    group_media_by_capture_date(
        sys.argv[1],
        sys.argv[2])

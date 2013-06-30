# Generate thumbnails and the shoot html pages

import os
import sys
import datetime
import time
from collections import defaultdict
import shutil
from subprocess import call
import jinja2

# download ffmpeg from the web
ffmpeg_bin = "d:\\bin\\ffmpeg\\bin\\ffmpeg.exe"

templateLoader = jinja2.FileSystemLoader( searchpath="D:\\Projects\\GitHub\\phototools\\templates" )
templateEnv = jinja2.Environment( loader=templateLoader )

def build_shot_html(shotId, thumbnails, destdir):
    template = templateEnv.get_template( "shot.jinja" )
    templateVars = { "title" : "Shot: %s" % shotId,
                     "description" : "TODO",
                     "thumbnails" : thumbnails
                   }
    with open(os.path.join(destdir, "%s.html" % shotId), "w") as text_file:
        text_file.write( template.render( templateVars ) )

def build_shoot_html(shots, destdir):
    template = templateEnv.get_template( "shoot.jinja" )
    templateVars = { "title" : "Shoot",
                     "description" : "TODO",
                     "shots" : shots
                   }
    with open(os.path.join(destdir, "index.html"), "w") as text_file:
        text_file.write( template.render( templateVars ) )

def file_basename(aFile):
    return os.path.splitext(os.path.basename(aFile))[0]

def is_video(aFile):
    extension = os.path.splitext(aFile)[1]
    return extension.lower() == ".mp4"  # todo

def make_thumbnails(aFile, destdir):
    print "Generating thumbnails for %s" % (aFile)
    call([ffmpeg_bin, "-i", aFile, "-r", "1", "%s.%%04d.jpg" % os.path.join(destdir, file_basename(aFile))])
    thumbnails = []
    for root, subFolders, files in os.walk(destdir):
        for aFile in files:
            extension = os.path.splitext(aFile)[1]
            if extension.lower() == ".jpg":
                thumbnails.append(  os.path.join(destdir, aFile) )
    return thumbnails

def index_shoot(sourcedir, destdir):
    shots = []
    for root, subFolders, files in os.walk(sourcedir):
        for aFile in files:
            if is_video(aFile):
                fullpath = os.path.join(root, aFile)
                file_destdir = os.path.join(destdir, file_basename(aFile))
                if os.path.exists(file_destdir):
                    continue
                os.makedirs(file_destdir)
                thumbnails = make_thumbnails(fullpath, file_destdir)
                build_shot_html(aFile, thumbnails, file_destdir)
                shots.append( {
                  "thumbnail": os.path.join(file_destdir, "%s.0001.jpg" % file_basename(aFile)),
                  "location": os.path.join(file_destdir, "%s.html" % aFile)
                } )
                #print "%s has file %s, mod date %s" % (root, ff, mod_date)
    build_shoot_html(shots, destdir)

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

def run_test():
    rootroot = "c:\\Users\\golov\\Documents"
    rootroot = "d:\\Projects"
    root = rootroot + "\\GitHub\\phototools\\test\\make_thumbnails"
    workdir = os.path.join(root, "workdir")
    if os.path.exists(workdir):
        shutil.rmtree(workdir, True, onerror=onerror)
    time.sleep(0.2) # race condition with removing the tree above
    os.makedirs(workdir)
    for dir in ("source", "dest"):
        shutil.copytree(os.path.join(root, dir), os.path.join(workdir, dir))

    index_shoot(
        os.path.join(workdir, "source"),
        os.path.join(workdir, "dest"))

    if False:
        if not compare_tree( workdir, os.path.join(root, "expected")):
            print "ERROR: test failed"

if __name__ == "__main__":
    if 1 == 0:
        run_test()
        exit
    if len(sys.argv) < 3:
        print "Usage: make_shoot_index.py source_folder dest_folder"
        exit()
        
    index_shoot(
        sys.argv[1],
        os.path.join(sys.argv[2], sys.argv[1]))
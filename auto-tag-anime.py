import argparse
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import model
import tag

class addAnimeTags():
    def __init__(self, skip=False):
        self.model = model.deepdanbooruModel()
        self.skip=skip

    def navigateDir(self, path):
        if os.path.isdir(path): 
            for root, dirs, files in os.walk(path):
                for filename in files:
                    self.addTagsToImage(root + '/' + filename)
        else:
            self.addTagsToImage(path)

    def addTagsToImage(self, path):
        
        if sys.platform == 'win32':   
            file_ext = os.path.splitext(path)[1]
            if file_ext != '.jpg' and file_ext != '.jpeg':
                return path + " is not a JPEG, no exif data"
        
        status, tags = self.model.classify_image(path)
        if status == 'success':
            self.add_tags(path, tags)
        else:
            print('failed to add tags for ', path)
            
    def add_tags(self, file, tags):
        if sys.platform == "linux" or sys.platform == "darwin":
            tag.osx_writexattrs(file, tags)
        elif sys.platform == 'win32':
            tag.win_addInfo(file, tags, self.skip)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automatically tag images")
    parser.add_argument("path", metavar="P", type=str, help="Path to directory or image")
    parser.add_argument("--skip", dest="skip", action="store_true",help="Skip already tagged images")
    args=parser.parse_args()
    addAnimeTags = addAnimeTags(args.skip)
    addAnimeTags.navigateDir(args.path)
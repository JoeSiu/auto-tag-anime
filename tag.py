import sys
if sys.platform == 'win32':
    import os
    from PIL import Image
    patched = False
else:
    import xattr

def patch_IPTCInfo(*args, **kwargs):
    import os, sys

    class HiddenPrints:
        def __enter__(self):
            self._original_stdout = sys.stdout
            sys.stdout = open('/dev/null', 'w')

        def __exit__(self, exc_type, exc_val, exc_tb):
            sys.stdout = self._original_stdout

    with HiddenPrints():
        return origianl_IPTCInfo(*args, **kwargs)

def osx_writexattrs(F,TagList):

    """ writexattrs(F,TagList):
    writes the list of tags to three xattr field:
    'kMDItemFinderComment','_kMDItemUserTags','kMDItemOMUserTags'
       This version uses the xattr library """

    plistFront = '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd"><plist version="1.0"><array>'
    plistEnd = '</array></plist>'
    plistTagString = ''
    for Tag in TagList:
        plistTagString = plistTagString + '<string>{}</string>'.format(Tag)
    TagText = plistFront + plistTagString + plistEnd

    OptionalTag = "com.apple.metadata:"
    XattrList = ["kMDItemFinderComment","_kMDItemUserTags","kMDItemOMUserTags"]
    for Field in XattrList:
        xattr.setxattr (F,OptionalTag+Field,TagText.encode('utf8'))
            # Equivalent shell command is xattr -w com.apple.metadata:kMDItemFinderComment [PLIST value] [File name]

def win_addInfo(F,TagList, skip):
    try:
        # Ref: https://stackoverflow.com/questions/63981971/xpcomment-and-xpkeywords-does-not-appear-when-writing-exif-metadata
        image = Image.open(F)

        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        # Get image metadata
        exifdata = image.getexif()
        XPKeywords = 0x9C9E
        try:
            # See if tag exists already
            exifdata[XPKeywords]
        except:
            # No tag exists
            exifdata[XPKeywords] = ';'.join(TagList).encode("utf16")
            image.save(F, exif=exifdata, optimize=False, icc_profile=image.info.get('icc_profile'))
            print('added ', str(len(TagList)), ' tags to ', F)
        else:
            # Tag exists
            if (skip):
                print('skipping ', F, ' as it has existing tags already')
            else:
                exifdata[XPKeywords] = ';'.join(TagList).encode("utf16")
                image.save(F, exif=exifdata, optimize=False)
                print('re-added ', str(len(TagList)), ' tags to ', F)

    except Exception as e:
        print('error on', F, ': ', e)

# Auto Anime Tag

Automatically adds booru style tags to an image or directory of images by using this neural net model: https://github.com/KichangKim/DeepDanbooru

## Changes in this fork
### Fixes for problems I am facing
* Fixed model not in folder error when using the newer pre-trained model (Updated tensorflow requirement to 2.8.0)
* Fixed program not detecting JPEG
* Fixed tags not adding to the image for Window (Use Pillow instead of IPTCInfo3)

### Additional changes
* Added skip function based on [winterNebs's fork](https://github.com/winterNebs/auto-tag-anime)
* Removed image optimization/compression when saving the image
* Maintain image's color profile when saving the image that have it

## Updated Instructions

1. Download the pre-trained model deepdanbooru-v3 from https://github.com/KichangKim/DeepDanbooru/releases (last tested stable version: ```v3-20211112-sgd-e28```), create a "model" folder in the auto-tag-anime folder, then put the pre-trained model files inside

2. `python3 -m venv ./env`

3. On osx: `source env/bin/activate`

   On Windows: `./env/Scripts/activate`

2. `python setup.py install`

## How to use
`python3 auto-tag-anime.py "example.jpg"`

`python3 auto-tag-anime.py "/path/to/directory/"`


## Notes
* windows version only works with jpegs
* See a list of tags the model will predict in 'tags.txt' inside of the deepdanbooru-v3 folder
* checks for images in subdirectories 

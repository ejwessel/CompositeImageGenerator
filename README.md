# CompositeImagesGenerator

- all.png - Generated file with all images conslidated into one file
- database.txt - CSV file with all the attributes
- images/ - Directory with all the assets used to generate composite images
- generated/ - Individual composite images
- generator.py - Code for generating the composite images

## Setting up `venv`
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
```
usage: generator.py [-h] [-a ALL] [--all-output ALL_OUTPUT] [-t TEMPLATE] [-f FEATURES] [--none-features NONE_FEATURES] [-m MODE] [--csv CSV]
                    [--input INPUT] [--output OUTPUT]

Generate Composite Images using an input directory and identifying the features

options:
  -h, --help            show this help message and exit
  -a ALL, --all ALL     flag to indicate to compile all the composed images into a single image (Default: False)
  --all-output ALL_OUTPUT
                        the output file name for the image to contain all composite images. Relevant only if 'all' flag is set (Default: False)
  -t TEMPLATE, --template TEMPLATE
                        the base template directory to work off of to constructed composed images (Default: 'background')
  -f FEATURES, --features FEATURES
                        list of directories to pull features from (Default: [])
  --none-features NONE_FEATURES
                        flag to determine if features can have an empty value (Default: False)
  -m MODE, --mode MODE  image mode. (Default: 'RGBA') See: https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes
  --csv CSV             the csv output file name (Default: 'database.txt')
  --input INPUT         the directory of the assets to use for composition (Default: 'images')
  --output OUTPUT       the directory of the generated composite images (Default: 'generated')
```

## Example:
given that the body, shoulder, and face directories exist
```
python generator.py -f body,shoulder,face
```

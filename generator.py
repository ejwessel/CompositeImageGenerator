import itertools
import random
import os
from PIL import Image
import argparse

parser = argparse.ArgumentParser(
    description='Generate Composite Images using an input directory and identifying the features')
parser.add_argument(
    '-a',
    '--all',
    default=False,
    help='flag to indicate to compile all the composed images into a single image (Default: False)'
)
parser.add_argument(
    '--all-output',
    default='all.png',
    help='the output file name for the image to contain all composite images. Relevant only if \'all\' flag is set (Default: False)'
)
parser.add_argument(
    '-t',
    '--template',
    default='background',
    help='the base template directory to work off of to constructed composed images (Default: \'background\')'
)
parser.add_argument(
    '-f',
    '--features',
    default=[],
    help='list of directories to pull features from (Default: [])'
)
parser.add_argument(
    '--none-features',
    default=False,
    help='flag to determine if features can have an empty value (Default: False)'
)
parser.add_argument(
    '-m',
    '--mode',
    default='RGBA',
    help='image mode. (Default: \'RGBA\') See: https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes'
)
parser.add_argument(
    '--csv',
    default='database.txt',
    help='the csv output file name (Default: \'database.txt\')'
)
parser.add_argument(
    '--input',
    default='images',
    help='the directory of the assets to use for composition (Default: \'images\')'
)
parser.add_argument(
    '--output',
    default='generated',
    help='the directory of the generated composite images (Default: \'generated\')'
)

args = parser.parse_args()

shuffle = True
spritesheet_max_columns = 10
features = args.features.split(',')
image_mode = args.mode
none_features = args.none_features
csv_name = args.csv
input_directory = args.input
output_directory = args.output
generate_all = args.all
all_generated_images = args.all_output
base_template_directory = args.template
base_template = 'base_template'
csv_header = '#number,base,attributes..\n'


def list_image_files(path: str):
    # Return list file names of all image files in a folder
    files = []
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        if os.path.isfile(filepath):
            try:
                Image.open(filepath).close()
            except Image.UnidentifiedImageError:
                continue
            else:
                files.append(filepath)
    return files


def list_to_name(list):
    string = ""
    for element in list:
        string += "-" + element

    # remove the first '-'
    return string[1:]


def compose_image(feature_files):
    composite_image = Image.new(image_mode, image_size, )
    for feature_file in feature_files:
        if feature_file is None:
            continue
        # if there is an attribute to apply overlap it
        try:
            print(f'\t composing {feature_file}')
            with Image.open(feature_file) as feature_image:
                composite_image.alpha_composite(feature_image)
        except:
            print(f'\t an issue occured on composing ${feature_file}')
            return None
    return composite_image


random.seed(0)

feature_files = {
    base_template: list_image_files(
        os.path.join(input_directory, base_template_directory))
}
for feature_file in features:
    path = os.path.join(input_directory, feature_file)
    if none_features:
        # [None] is a valid feature; nothing is applied
        feature_files[feature_file] = [None] + list_image_files(path)
    else:
        feature_files[feature_file] = list_image_files(path)

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

with Image.open(feature_files[base_template][0]) as image:
    image_size = image.size

csv_file = open(csv_name, 'w')
csv_file.write(csv_header)

# all possible permutations including the usage of None as an attribute
# num_bases * (num_eyes + 1) * (num_head + 1) * (num_mouth + 1)
permutations = list(itertools.product(*feature_files.values()))
total = len(permutations)

if shuffle:
    random.shuffle(permutations)

cols = min(total, spritesheet_max_columns)
rows = (total // spritesheet_max_columns) + 1
width = cols * image_size[0]
height = rows * image_size[1]
spritesheet = Image.new(image_mode, (width, height))
x = 0
y = 0

for (number, feature_files) in enumerate(permutations):
    print(f'Generating image {number+1}/{total} {feature_files}')
    composite_image = compose_image(feature_files)

    if composite_image is None:
        continue

    composite_image = composite_image.resize(
        (composite_image.width, composite_image.height), 0)

    features_list = []
    for feature in feature_files:
        feature_name = os.path.basename(feature).split('.')[0]
        features_list.append(feature_name)

    composite_image.save(os.path.join(
        output_directory, f'img_{list_to_name(features_list)}.png'))

    # write the list of attributes to the csv file
    csv_file.write(','.join(features_list) + '\n')

    if generate_all:
        spritesheet.paste(composite_image, (x, y))
        x += image_size[0]
        if x >= spritesheet.width:
            x = 0
            y += image_size[1]

if generate_all:
    spritesheet = spritesheet.resize(
        (spritesheet.width, spritesheet.height), 0)
    spritesheet.save(all_generated_images)

csv_file.close()

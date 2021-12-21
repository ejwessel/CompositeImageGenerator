import itertools
import random
import os
from PIL import Image


output_individual_sprites = True
shuffle = True
spritesheet_max_columns = 10
image_mode = 'RGBA'
csv_header = '#number,base,attributes..\n'
csv_name = 'database.txt'
images_path = 'images'
individual_image_path = 'sprites'
all_generated_images = 'all.png'
base_templates = 'base'
features = [
    'eyes',
    'head',
    'mouth'
]


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


def list_to_string(list):
    string = ""
    for element in list:
        string += "-" + element

    # remove the first '-'
    return string[1:]


random.seed(0)

feature_files = {
    'base': list_image_files(os.path.join(images_path, base_templates))
}
for feature in features:
    path = os.path.join(images_path, feature)
    # [None] is a valid feature; nothing is applied
    feature_files[feature] = [None] + list_image_files(path)

if output_individual_sprites and not os.path.exists(individual_image_path):
    os.mkdir(individual_image_path)

with Image.open(feature_files['base'][0]) as image:
    image_size = image.size

csv_file = open(csv_name, 'w')
csv_file.write(csv_header)

# all possible combinations including the usage of None as an attribute
# num_bases * (num_eyes + 1) * (num_head + 1) * (num_mouth + 1)
combinations = list(itertools.product(*feature_files.values()))
total = len(combinations)

# randomization of the order
if shuffle:
    random.shuffle(combinations)

cols = min(total, spritesheet_max_columns)
rows = (total // spritesheet_max_columns) + 1
width = cols * image_size[0]
height = rows * image_size[1]
spritesheet = Image.new(image_mode, (width, height))

x = 0
y = 0

for (number, files) in enumerate(combinations):
    print(f'Generating image {number+1}/{total}', end='\r')

    composite_image = Image.new(image_mode, image_size, )
    attributes_list = []

    for file in files:
        if file is None:
            continue

        # if there is an attribute to apply overlap it
        with Image.open(file) as feature_image:
            composite_image.alpha_composite(feature_image)

        attributes = os.path.basename(file).split('.')[0]
        attributes_list.append(attributes)

    spritesheet.paste(composite_image, (x, y))
    x += image_size[0]
    if x >= spritesheet.width:
        x = 0
        y += image_size[1]

    if output_individual_sprites:
        # increase the size of the individual image 10x
        composite_image = composite_image.resize(
            (composite_image.width * 10, composite_image.height * 10), 0)
        composite_image.save(os.path.join(
            individual_image_path, f'img_{list_to_string(attributes_list)}.png'))

    csv_file.write(','.join(attributes_list) + '\n')

# increase overall sprite sheet 10x
spritesheet = spritesheet.resize(
    (spritesheet.width * 10, spritesheet.height * 10), 0)
spritesheet.save(all_generated_images)

csv_file.close()

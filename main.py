import cv2
import json
import math
import os
from mosaic_utils import MosaicCreator

# Constants and configurations
CONFIG = {
    'TILE_SIZE': (100, 100),
    'NUM_TILES': 10000,
    'TILE_AVG_COLORS_FILE': 'tile_images_avg_colors.npy',
    'BASE_IMAGE_FILE': 'target.png',
    'TILE_IMAGES_DIR': 'tiles/',
    'OUTPUT_JSON': 'mosaic.json',
    'OUTPUT_IMAGE': 'mosaic.png'
}

def main():
    # Create a MosaicCreator object
    mosaic_creator = MosaicCreator(CONFIG)

    # Calculate grid size
    grid_size = int(math.sqrt(CONFIG['NUM_TILES']))
    mosaic_width = grid_size * CONFIG['TILE_SIZE'][0]
    mosaic_height = grid_size * CONFIG['TILE_SIZE'][1]

    # Load base image and tile images
    base_img = mosaic_creator.load_base_image(CONFIG['BASE_IMAGE_FILE'])
    tile_imgs = mosaic_creator.load_tile_images(CONFIG['TILE_IMAGES_DIR'])

    # Calculate average colors
    base_img_avg_colors = mosaic_creator.calculate_base_image_average_colors(base_img, grid_size)
    tile_imgs_avg_colors = mosaic_creator.calculate_tile_image_average_colors(tile_imgs)

    # Find matching tiles
    matching_tile_indices = mosaic_creator.find_best_matching_tiles(base_img_avg_colors, tile_imgs_avg_colors, grid_size)

    # Write matching tiles to JSON to be used later for example in the web app
    # Convert int64 values to int
    # matching_tile_indices_json = [int(index) for index in matching_tile_indices]

    # with open(CONFIG['OUTPUT_JSON'], 'w') as f:
    #     json.dump(matching_tile_indices_json, f)

    # Create the mosaic
    mosaic = mosaic_creator.create_mosaic(matching_tile_indices, tile_imgs, grid_size)

    # Save the mosaic image
    cv2.imwrite(CONFIG['OUTPUT_IMAGE'], mosaic)

    print(f'Mosaic created with size {mosaic_width}x{mosaic_height}')


if __name__ == '__main__':
    main()

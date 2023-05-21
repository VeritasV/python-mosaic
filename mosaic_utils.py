import cv2
import numpy as np
from sklearn.neighbors import NearestNeighbors
import os
import itertools
from random import shuffle
from colorspacious import cspace_converter
from tqdm import tqdm
from scipy.spatial import cKDTree

def rgb2lab(image):
    # Create a converter from RGB to Lab
    converter = cspace_converter("sRGB1", "CIELab")
    return converter(image)

def coords_from_middle(x_count, y_count, y_bias=1, shuffle_first=0):
    x_mid = int(x_count / 2)
    y_mid = int(y_count / 2)
    coords = list(itertools.product(range(x_count), range(y_count)))
    coords.sort(key=lambda c: abs(c[0] - x_mid) * y_bias + abs(c[1] - y_mid))
    coords = shuffle_first_items(coords, shuffle_first)
    return coords

def shuffle_first_items(items, shuffle_count):
    if shuffle_count == 0:
        return items

    shuffled_items = items[:shuffle_count]
    shuffle(shuffled_items)
    return shuffled_items + items[shuffle_count:]

class MosaicCreator:

    def __init__(self, config):
        self.config = config

    def load_base_image(self, filepath):
        return cv2.imread(filepath)

    def load_tile_images(self, tile_dir):
        tile_images = []
        for filename in os.listdir(tile_dir):
            img_path = os.path.join(tile_dir, filename)
            img = cv2.imread(img_path)
            if img is not None:
                img_resized = cv2.resize(img, self.config['TILE_SIZE'])
                tile_images.append(img_resized)
        return np.array(tile_images)

    def calculate_base_image_average_colors(self, base_img, grid_size):
        base_img_resized = cv2.resize(base_img, (grid_size, grid_size))
        return rgb2lab(base_img_resized.reshape(-1, 3))

    def calculate_tile_image_average_colors(self, tile_images):
        avg_colors = np.zeros((len(tile_images), 3))

        for i, img in enumerate(tile_images):
            avg_color = np.mean(img, axis=(0, 1))
            avg_colors[i] = avg_color

        
        # Save the average colors to a file for later use if you use the same tile images
        # if not os.path.exists(self.config['TILE_AVG_COLORS_FILE']):
        #     np.save(self.config['TILE_AVG_COLORS_FILE'], avg_colors)
        # else:
        #     avg_colors = np.load(self.config['TILE_AVG_COLORS_FILE'])

        return rgb2lab(avg_colors)


    def find_best_matching_tiles(self, base_img_avg_colors, tile_imgs_avg_colors, grid_size):
        tree = cKDTree(tile_imgs_avg_colors)

        used_tile_indices = set()
        matching_tile_indices = [None] * (grid_size * grid_size)

        cell_indices = coords_from_middle(grid_size, grid_size)

        pbar = tqdm(total=len(cell_indices))

        for y, x in cell_indices:
            base_color_index = y * grid_size + x
            avg_color = base_img_avg_colors[base_color_index]
            
            # Using KDTree for nearest neighbor search
            distances, indices = tree.query([avg_color], k=len(tile_imgs_avg_colors))

            pbar.update(1)

            for index in indices[0]:
                if index not in used_tile_indices:
                    used_tile_indices.add(index)
                    # Ensure that the tile_index is an integer, not a one-element array
                    matching_tile_indices[base_color_index] = index
                    break
        
        pbar.close()

        return matching_tile_indices



    def create_mosaic(self, matching_tile_indices, tile_imgs, grid_size):
        mosaic = np.zeros((grid_size * self.config['TILE_SIZE'][1], grid_size * self.config['TILE_SIZE'][0], 3))

        cell_indices = coords_from_middle(grid_size, grid_size)

        for y, x in cell_indices:
            base_color_index = y * grid_size + x
            tile_index = matching_tile_indices[base_color_index]
            tile = tile_imgs[tile_index]

            mosaic[y * self.config['TILE_SIZE'][1]:(y + 1) * self.config['TILE_SIZE'][1],
                   x * self.config['TILE_SIZE'][0]:(x + 1) * self.config['TILE_SIZE'][0]] = tile
            

        return mosaic

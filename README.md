# Photomosaic Generator

This repository contains a Python implementation of a photomosaic generator. A photomosaic is a large image composed of smaller tile images. This project allows you to create your own photomosaic using a base image and a directory of tile images.

## How it Works

The photomosaic generator works by first calculating the average color of each tile image and the corresponding region in the base image. It then uses a K-D tree, an efficient data structure for nearest-neighbor searches, to find the tile image that most closely matches the color of each region in the base image. The result is a mosaic image that closely resembles the original base image.

## Requirements

- Python 3.7 or above
- NumPy
- OpenCV
- scikit-learn
- colorspacious

To install these packages, run:

```sh
pip install numpy opencv-python scikit-learn colorspacious
```

## Usage

1. Clone the repository:

```sh
git clone https://github.com/VeritasV/python-mosaic.git
```

2. Navigate to the repository directory:

```sh
cd python-mosaic
```

3. Place your base image in the repository directory and name it target.png
4. Create a tiles directory in the repository and place your tile images inside it.
5. Run the script:

```sh
python main.py
```

5. The resulting mosaic image will be saved in the current directory.

## Contributing

Your contributions are always welcome! Please create a pull request to add new algorithms, improve the current implementation, or fix bugs.

## Support

If you find this project helpful or interesting, please consider supporting me on [BuyMeACoffee](https://www.buymeacoffee.com/UH0mejbw8U).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

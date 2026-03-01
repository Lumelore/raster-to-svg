#!/usr/bin/env python3
# Script by Lumelore, GNU-GPLv3

import argparse
import os
import xml.etree.ElementTree as ET
from PIL import Image


def run():
    parser = argparse.ArgumentParser(description="Converts raster images to svg by replacing pixels with rectangles. Intended for small images such as pixel art.",
                                     prog="RasterToSVG")    

    parser.add_argument('rasterfile',
                        help="The raster graphics file to convert"
                       )
    parser.add_argument('-o', '--output',
                        default='output.svg',
                        help="The output destination and file name (default: %(default)s)"
                       )

    args = parser.parse_args()
    
    raster_to_svg(args.rasterfile, args.output)


def raster_to_svg(rasterfile, outputfile):
    # Create tree with blank svg root
    tree = ET.ElementTree(ET.Element('svg'))
    root = tree.getroot()
    
    with Image.open(rasterfile) as img:
        # Load all pixels
        px = img.load()
        current_pixel = px[0, 0]
        
        root.set('width', f'{img.width}')
        root.set('height', f'{img.height}')
        root.set('viewBox', f'0 0 {img.width} {img.height}')

        # Iterate over all pixels
        for h in range(img.height):
            for w in range(img.width):
                current_pixel = px[w, h]
                # Place non fully transparent pixels in svg
                if current_pixel[3] != 0:
                    # Calculate hex and opacity
                    hex_color = f'{current_pixel[0]:x}{current_pixel[1]:x}{current_pixel[2]:x}'
                    opacity_percent = current_pixel[3]/255
                    
                    root.append(ET.Element('rect',
                                           attrib={
                                               'style' : f'fill:#{hex_color};fill-opacity:{opacity_percent};stroke:none;stroke-width=0;stroke-linecap:square;stroke-linejoin:miter;stroke-dasharray:none;stroke-opacity:1;paint-order:markers fill stroke',
                                               'x' : f'{w}',
                                               'y' : f'{h}',
                                               'width' : '1',
                                               'height' : '1',
                                               'id' : f'{w}-{h}'
                                               }
                                           ))

    # Write out SVG
    ET.indent(tree, ' ')
    tree.write(f'{os.getcwd()}/{outputfile}')

if __name__ == "__main__":
    run()

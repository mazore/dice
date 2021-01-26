import cv2  # pip install opencv-python
import pygame as pg
from math import ceil
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', dest='img', action='store', required = True)
    parser.add_argument('--output', '-o', dest='outname', action='store', type=str, default = 'output.png')
    return parser.parse_args()

DIE_WIDTH = 25
RESOLUTION_FACTOR = 2

pg.init()

HEIGHT, WIDTH, DOT_RADIUS, GRID_WIDTH, GRID_HEIGHT, w = [None] * 6

DOT_CENTERS = {
    1: [(0, 0)],
    2: [(1, -1), (-1, 1)],
    3: [(1, -1), (0, 0), (-1, 1)],
    4: [(-1, -1), (1, -1), (-1, 1), (1, 1)],
    5: [(-1, -1), (1, -1), (-1, 1), (1, 1), (0, 0)],
    6: [(-1, -1), (1, -1), (-1, 1), (1, 1), (-1, 0), (1, 0)]
}

def init_globals(img):
    global HEIGHT, WIDTH, DOT_RADIUS, GRID_WIDTH, GRID_HEIGHT, w
    HEIGHT, WIDTH = img.shape
    WIDTH *= RESOLUTION_FACTOR
    HEIGHT *= RESOLUTION_FACTOR
    DOT_RADIUS = DIE_WIDTH // 10
    GRID_WIDTH = WIDTH // DIE_WIDTH
    GRID_HEIGHT = HEIGHT // DIE_WIDTH
    w = pg.display.set_mode((GRID_WIDTH * DIE_WIDTH, GRID_HEIGHT * DIE_WIDTH))

def draw_dice(img):
    for pixel_x in range(GRID_WIDTH):
        for pixel_y in range(GRID_HEIGHT):
            brightness = img[pixel_y][pixel_x]

            die_number = ceil(brightness / 42.5)  # Map to 1-6
            
            if die_number == 0:
                continue

            die_x = pixel_x*DIE_WIDTH + 0.5*DIE_WIDTH
            die_y = pixel_y*DIE_WIDTH + 0.5*DIE_WIDTH

            for dotCenter in DOT_CENTERS[die_number]:
                dot_x = die_x + dotCenter[0]*DIE_WIDTH*0.25
                dot_y = die_y + dotCenter[1]*DIE_WIDTH*0.25
                pg.draw.circle(w, [255, 255, 255], (int(dot_x), int(dot_y)), DOT_RADIUS)


def draw_lines(img):
    for i in range(GRID_WIDTH):
        x = i * DIE_WIDTH
        pg.draw.line(w, [50, 50, 50], (x, 0), (x, HEIGHT))

    for i in range(GRID_HEIGHT):
        y = i * DIE_WIDTH
        pg.draw.line(w, [50, 50, 50], (0, y), (WIDTH, y))


if __name__ == '__main__':
    args = parse_args()
    img = cv2.imread(args.img, 0)
    init_globals(img)
    # Downscale image
    img = cv2.resize(img, (GRID_WIDTH, GRID_HEIGHT), interpolation=cv2.INTER_AREA)

    draw_dice(img)
    draw_lines(img)
    pg.display.update()
    pg.image.save(w, args.outname)
    pg.quit()

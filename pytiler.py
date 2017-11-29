#!/usr/bin/env python

# PyTiler: Python script to generate tiled textures
#
# Author: Oxben <oxben@free.fr>
#
# Examples:
# ./pytiler.py -a -f ~/media/blender/9\ Boulevard\ Clemenceau/textures/Birch.jpg -n 20 -H 32 -W 128 --brick --border=1
# ./pytiler.py -a -f ~/media/blender/textures/seamless/rock\ cave\ mountain\ brown\ texture\ 1024.jpg -n 30 -H 32 -W 32 --border=3
# ./pytiler.py -a -f ~/media/blender/textures/seamless/rock\ cave\ mountain\ brown\ texture\ 1024.jpg -n 128 -H 64 -W 128 --border=4 -w 1024 -h 1024 --brick --rand_width -S 1976 --border_shade=48
# ./pytiler.py -a -f ~/media/blender/textures/wood/oak-plank.png -n 12 -w 1024 -h 1024 -W 1024 -H 128 -o oak-planks.png
# TILESIZE=64 ~/src/pytiler/pytiler.py -p face-2017112 -H $TILESIZE -W $TILESIZE -h $((20 * TILESIZE)) -w $((20 * TILESIZE)) --remove-after-use -o poster.png

import getopt
import os
import random
import sys
import time
import pygame


def error(msg):
    print("Error: %s\n") % (msg)


#-------------------------------------------------------------------------------
class Tile():
    def __init__(self, filename=None, surface=None):
        if filename != None:
            print("Load %s") % (filename)
            self.filename = filename
            self.surface = pygame.image.load(filename)
        elif surface != None:
            self.surface = surface
        self.rect = self.surface.get_rect()

    def __str__(self):
        s = self.filename
        return s

    def draw_at(self, display, x, y, width, height, angle):
        #surface = pygame.transform.rotozoom(self.surface, angle, 1.0)
        surface = pygame.transform.rotate(self.surface, angle)
        surface = pygame.transform.smoothscale(surface, (width, height))
        display.blit(surface, self.rect.move(x, y))


#-------------------------------------------------------------------------------
class PyTiler():
    def __init__(self):
        self.display = None
        self.auto = False
        self.nr_tiles = 8
        self.filename = ""
        self.prefix = 'tile-'
        self.rotate = False
        self.brick = False
        self.demo = False
        self.seed = 0
        self.tile_width = 64
        self.tile_height = 64
        self.random_width = False
        self.width = 512
        self.height = 512
        self.border = 0
        self.border_shade = 64
        self.outfilename = "out.png"
        self.remove_after_use = False
        self.tiles = []
        self.tiles_trash = []

    def __str__(self):
        s = ""
        return s

    def usage(self):
        print("Usage: " +  os.path.basename(sys.argv[0]) + \
              " -w width -h height -o filename -p tile-prefix -s seed -r")
        print("       " +  os.path.basename(sys.argv[0]) + \
             " -a -w width -h height -W tile_width -H tile_height -f -f input_filename -o output_filename")
        print("\nOptions:\n")
        print("  -a                 Auto-generate tiles")
        print("  -f filename        Input texture filename")
        print("  -h height          Output texture height")
        print("  -H height          Individual tile height")
        print("  -n num             Number of tiles to generate")
        print("  -o filename        Output filename")
        print("  -p prefix          Prefix of tiles files")
        print("  -r                 Randomly rotate tiles by 90 degree increment")
        print("  -s                 Random seed")
        print("  -w width           Output texture width")
        print("  -W width           Individual tile width")
        print("  --brick            Use brick pattern")
        print("  --border=num       Tiles border width")
        print("  --border-shade=num Border shade (0..255) (greater values give darker border)")
        print("  --rand-width       Random tile width")
        print("  --remove-after-use Remove tile from list after is has been used once")
        print("                     This makes sure every tiles have been used before reusing one")

    def parse_args(self):
	try:
            opts, args = getopt.getopt(sys.argv[1:], "abf:h:H:n:o:p:rs:S:w:W:",
                                       ["demo", "brick", "border=", "border-shade=", "rand-width", "remove-after-use"])
	except getopt.GetoptError as err:
            error(str(err))
            self.usage()
            exit(1)

	for o, a in opts:
            if o == "-a":
                self.auto = True
            elif o == "-f":
                self.filename = a
            elif o == "-h":
                self.height = int(a)
            elif o == "-H":
                self.tile_height = int(a)
            elif o == "-n":
                self.nr_tiles = int(a)
            elif o == "-o":
                self.outfilename = a
            elif o == "-p":
                self.prefix = a
            elif o == "-r":
                self.rotate = True
            elif o == "-s":
                self.tile_height = self.tile_width = int(a)
            elif o == "-S":
                self.seed = int(a)
            elif o == "-w":
                self.width = int(a)
            elif o == "-W":
                self.tile_width = int(a)
            elif o == "--brick":
                self.brick = True
            elif o == "--demo":
                self.demo = True
            elif o == "--border":
                self.border = int(a)
            elif o == "--border-shade":
                shade = int(a)
                if 0 <= shade <= 255:
                    self.border_shade = shade
                else:
                    error(("Invalid border shade %d") % (shade))
                    self.usage()
                    exit(1)
            elif o == "--rand-width":
                self.random_width = True
            elif o == "--remove-after-use":
                self.remove_after_use = True

    def run(self):
        """Initialize and run infinite event loop"""
        if self.seed == 0:
            self.seed = random.randrange(sys.maxsize)
        random.seed(self.seed)

        print("Random Seed: %d" % self.seed)

        pygame.key.set_repeat(100,100)

        # Load or create tiles
        if self.auto == False:
            for path in os.listdir('.'):
                if os.path.isfile(path) and \
                   path.startswith(self.prefix) and \
                   path.endswith('.png') or path.endswith('.jpg'):
                    self.tiles.append(Tile(filename=path))
            print("%d tiles loaded" % (len(self.tiles)))
        else:
            if not os.path.isfile(self.filename):
                print("Error: No file '%s' found") % (self.filename)
                sys.exit(1)
            surface = pygame.image.load(self.filename)

            for i in range(0, self.nr_tiles):
                x = random.randrange(0, surface.get_width() - self.tile_width)
                y = random.randrange(0, surface.get_height() - self.tile_height)
                if self.random_width:
                    tile_width = random.randrange(self.tile_width/2, self.tile_width)
                else:
                    tile_width = self.tile_width
                print tile_width
                subsurface = surface.subsurface(pygame.Rect(x, y, tile_width, self.tile_height)).copy()
                if self.border > 0:
                    r = pygame.Rect(0, 0, tile_width, self.tile_height)
                    border_surf = pygame.Surface((tile_width, self.tile_height), pygame.SRCALPHA)
                    border_surf.fill((0,0,0,0))
                    if self.border < 4:
                        border_surf.fill((0,0,0,0))
                        #col = (16, 16, 16) # Good for wood floor
                        col = (self.border_shade, self.border_shade, self.border_shade)
                        pygame.draw.line(border_surf, col, (0, 0), (tile_width-1, 0), self.border)
                        pygame.draw.line(border_surf, col, (0, 0), (0, self.tile_height-1), self.border)
                        subsurface.blit(border_surf, r, special_flags=pygame.BLEND_RGBA_SUB)
                    else:
                        col = (self.border_shade, self.border_shade, self.border_shade)
                        pygame.draw.rect(border_surf, col, (0, 0, tile_width, self.tile_height), self.border)
                        col = (min(self.border_shade+32, 255), min(self.border_shade+32, 255), min(self.border_shade+32, 255))
                        pygame.draw.rect(border_surf, col, (0, 0, tile_width, self.tile_height), 1)
                        #subsurface.blit(border_surf, r)
                        subsurface.blit(border_surf, r, special_flags=pygame.BLEND_RGBA_SUB)
                self.tiles.append(Tile(surface=subsurface))

        # Init window attribute
        pygame.display.set_caption("PyTiler")
        try:
            pygame.display.set_icon(pygame.image.load("PatternBrick.png"))
        except:
            print("Error: Icon %s not found" % "PatternBrick.png")

        # Set screen size
        size = self.width, self.height
        self.display = pygame.display.set_mode(size)
        self.draw()

        while True:
            # Process events
            if pygame.event.peek():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    elif event.type == pygame.KEYDOWN:
                        if event.unicode in ('q', 'Q') or \
                           event.key == pygame.K_ESCAPE:
                            return
                        elif event.key == pygame.K_SPACE:
                            self.draw()
                        elif event.unicode == 'b':
                            self.brick = not self.brick
                            self.draw()
                        elif event.unicode == 'r':
                            self.rotate = not self.rotate
                            self.draw()
                        elif event.unicode == 's':
                            self.save()
            if self.demo:
                time.sleep(1/5.0)
                self.draw()
            else:
                time.sleep(1/60.0)

    def draw(self):
        '''Draw tiles'''
        self.display.fill(pygame.Color('#00000000'))
        y = 0
        while y < self.height:
            # Set first tile offset
            if self.brick:
                x = -random.randrange(0, self.tile_width)
                print "X offset = " + str(x)
            else:
                x = 0
            first_tile = None
            first_tile_angle = 0

            while x < self.width:
                # Choose next tile
                if len(self.tiles) == 0:
                    if len(self.tiles_trash) > 0:
                        # Swap tile list
                        self.tiles = self.tiles_trash
                        self.tiles_trash = []
                    else:
                        raise Exception("Error: tile list is empty")
                tile = random.choice(self.tiles)
                if self.remove_after_use:
                    self.tiles_trash.append(tile)
                    self.tiles.remove(tile)

                # Set rotation
                if self.rotate:
                    angle = random.choice([0,90,180,270])
                    #angle = random.randrange(0, 360)
                else:
                    angle = 0

                # Save first tile of current line
                # It is used to complete end of line, so wrapping is correct
                if first_tile == None:
                    first_tile = tile
                    first_tile_angle = angle

                if self.brick and (x + first_tile.rect.width) > self.width:
                    tile = first_tile
                    angle = first_tile_angle

                # Draw tile
                if self.random_width:
                    width = tile.rect.width
                else:
                    width = self.tile_width
                tile.draw_at(self.display, x, y, width, self.tile_height, angle)

                x += width
            y += self.tile_height

        pygame.display.flip()

    def save(self):
        '''Save tiles to output file'''
        pygame.image.save(self.display, self.outfilename)
        print("Saved tiles into " + self.outfilename)


#-------------------------------------------------------------------------------
if __name__ == '__main__':
    pygame.init()
    tiler = PyTiler()
    tiler.parse_args()
    tiler.run()
    pygame.quit()
    sys.exit();

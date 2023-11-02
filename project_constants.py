# Number of rows and columns
ROW_COUNT = 100
COLUMN_COUNT = 60

# This sets the WIDTH and HEIGHT of each grid location
TILE_WIDTH = 15
TILE_HEIGHT = 15

MARGIN = 2

# This needs to be changed later I just have it like this for
# an example sprite
SPRITE_SCALING = TILE_HEIGHT / 1920

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (TILE_WIDTH + MARGIN) * COLUMN_COUNT + MARGIN
SCREEN_HEIGHT = (TILE_HEIGHT + MARGIN) * ROW_COUNT + MARGIN
SCREEN_TITLE = "Rogue Testing"

from generals_io_client import generals
import logging
import sys
import math

userid = sys.argv[1]
username = sys.argv[2]
gameid = sys.argv[3]

logging.basicConfig(level=logging.DEBUG)

g = generals.Generals(userid, username, 'private', gameid)

rows = 20
cols = 20
pidx = 0
general_y, general_x = 0,0
tiles = []
armies = []
cities = []

def calc_distance(position1,position2):
	return math.fabs(position1[0] - position2[0]) + math.fabs(position1[1] - position2[1])

def is_in_map(y, x):
	if y+1<cols and y-1>=0 and x-1>=0 and x+1<rows:
		return True
	return False

def is_interior(y, x):
	valid_neighbors = (pidx, generals.MOUNTAIN)
	if (is_in_map(y, x) and
		tiles[y][x+1] in valid_neighbors and
		tiles[y][x-1] in valid_neighbors and
		tiles[y-1][x] in valid_neighbors and
		tiles[y+1][x] in valid_neighbors):
		return True
	else:
		return False

def is_frontier(y, x):
	invalid_neighbors = (pidx, generals.MOUNTAIN)
	if is_in_map(y, x) and (
		tiles[y][x+1] not in invalid_neighbors or 
		tiles[y][x-1] not in invalid_neighbors or
		tiles[y-1][x] not in invalid_neighbors or
		tiles[y+1][x] not in invalid_neighbors):
		return True
	else:
		return False

def get_topology(tiles):
	interior = []
	frontier = []
	for y, row in enumerate(tiles):
		for x, t in enumerate(row):
			if t == pidx:
				if is_interior(y, x):
					interior.append((y, x))
				if is_frontier(y, x):
					frontier.append((y, x))
	return interior, frontier

def find_nearest_frontier(y, x, frontier):
	return

for update in g.get_updates():
	pidx = update['player_index']
	try:
		general_y, general_x = update['generals'][pidx]
	except KeyError:
		break

	rows, cols = update['rows'], update['cols']

	tiles = update['tile_grid']
	armies = update['army_grid']
	cities = update['cities']
	turn = update['turn']

	interior, frontier = get_topology(tiles)


	basic_turn_info = '''
	interior: %s
	frontier: %s
	''' %(interior, frontier)

	print(basic_turn_info)

	# for tile in interior:

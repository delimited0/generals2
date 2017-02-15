from generals_io_client import generals
import math


def calc_distance(p, q):
	return math.fabs(p[0] - q[0]) + math.fabs(p[1] - q[1])

class Bot(object):
	def __init__(self, pidx):
		self.pidx = pidx
		self.interior = []
		self.frontier = []
		self.armies = {}
		self.rows = 20
		self.cols = 20
		self.non_neighbors = (self.pidx, generals.MOUNTAIN)

	def is_in_map(self, p):
		y, x = p
		if y+1 < self.cols and y-1 >= 0 and x-1 >= 0 and x+1 < self.rows:
			return True
		return False

	def neighbors_in_map(self, p):
		y, x = p[0], p[1]
		if (self.is_in_map((y, x+1)) and	
			self.is_in_map((y, x-1)) and
			self.is_in_map((y+1, x)) and
			self.is_in_map((y-1, x))):
			return True
		else:
			return False

	def is_interior(self, p, tiles):
		y, x = p[0], p[1]
		if (self.is_in_map(p) and self.neighbors_in_map(p) and
			tiles[y][x+1] in self.non_neighbors and
			tiles[y][x-1] in self.non_neighbors and
			tiles[y-1][x] in self.non_neighbors and
			tiles[y+1][x] in self.non_neighbors):
			return True
		else:
			return False

	def is_frontier(self, p, tiles):
		y, x = p[0], p[1]
		if (self.is_in_map(p) and self.neighbors_in_map(p) and
			tiles[y][x+1] not in self.non_neighbors or 
			tiles[y][x-1] not in self.non_neighbors or
			tiles[y-1][x] not in self.non_neighbors or
			tiles[y+1][x] not in self.non_neighbors):
			return True
		else:
			return False

	def update_status(self, tiles, armies):
		self.armies = {}
		self.interior = []
		self.frontier = []
		for y, row in enumerate(tiles):
			for x, t in enumerate(row):
				p = (y, x)
				if t == self.pidx:
					self.armies[p] = armies[y][x]
					if self.is_interior(p, tiles):
						self.interior.append(p)
					if self.is_frontier(p, tiles):
						self.frontier.append(p)

	def find_nearest_frontier(self, p):
		dists = [calc_distance(p, q) for q in self.frontier]
		min_dist = min(dists)
		min_idx = dists.index(min_dist)	
		return self.frontier[min_idx]

	def reinforce(self, g):
		commands = 0
		for p in self.interior:
			y, x = p[0], p[1]
			if self.armies[p] > 1 and commands < 3:
				target = self.find_nearest_frontier(p)
				g.move(y, x, target[0], target[1])
				commands += 1

	def expand(self, g, tiles):
		for p in self.frontier:
			y, x = p[0], p[1]
			if self.armies[p] > 1:
				if self.is_in_map((y+1, x)) and tiles[y+1][x] != self.pidx:
					print "moving down!"
					g.move(y, x, y+1, x)
				elif self.is_in_map((y-1, x)) and tiles[y-1][x] != self.pidx:
					print "moving up!"
					g.move(y, x, y-1, x)		
				elif self.is_in_map((y, x+1)) and tiles[y][x+1] != self.pidx:
					print "moving right!"
					g.move(y, x, y, x+1)
				elif self.is_in_map((y, x-1)) and tiles[y][x-1] != self.pidx:
					print "moving left!"
					g.move(y, x, y, x-1)	




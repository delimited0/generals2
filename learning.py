from generals_io_client import generals
import logging
import sys

userid = sys.argv[1]
username = sys.argv[2]
gameid = sys.argv[3]

logging.basicConfig(level=logging.DEBUG)

g = generals.Generals(userid, username, 'private', gameid)

def print_type(x):
	print "type: " + type(x).__name__

for state in g.get_updates():
	# {k: print_type(x) for k, x in state.items()}
	#for k, v in state.iteritems():
	#	print k
	
	# what is army_grid?
	# it tells you how much army in each grid
	# here, print out the number of army in bot's general
	# pi = state['player_index']
	# y, x = state['generals'][pi]
	# print str(state['army_grid'][y][x])

	# what is cities?
	for c in state['cities']:
		print "cities: " + str(c)

	
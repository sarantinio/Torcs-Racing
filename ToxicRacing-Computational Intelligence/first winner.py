#! /usr/bin/env python3

from pytocl.main import main
from my_driver import MyDriver

# from __future__ import print_function

import os
import pickle

# import cart_pole
import time
import neat
# import visualize
#! /usr/bin/env python3

from pytocl.main import main
from my_driver import MyDriver
import subprocess
import neat



if __name__ == '__main__':

	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, 'config-ctrnn')
	config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
	                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
	                     config_path)

	with open('winner-feedforward', 'rb') as f:
		c = pickle.load(f)

	print('Loaded genome:')
	net=neat.ctrnn.CTRNN.create(c, config, 0.1)
	

	# subprocess.call('./start.sh',shell=True)
	

	main(MyDriver(net=net))
	

	with open("mydata.txt",'r') as f:
		fitt=f.read()
	

	# subprocess.call('./autostop.sh',shell=True)
	
	print("fitness *******************   ",fitt)

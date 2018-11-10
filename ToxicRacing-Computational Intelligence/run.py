#! /usr/bin/env python3

from pytocl.main import main
from pytocl.driver import Driver

# from __future__ import print_function
from neat.checkpoint import Checkpointer
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
def eval_genome(genome, config):
	# net = neat.nn.FeedForwardNetwork.create(genome, config)
	net=neat.nn.FeedForwardNetwork.create(genome, config)
	# print("meh")
	# os.system('pkill torcs')
	# time.sleep(5)
	# subprocess.call('torcs',shell=True)
	# os.system('torcs')
	# print("a")
	# time.sleep(1)
	# cwd=os.getcwd()
	subprocess.call('./autostart.sh',shell=True)
	# print("b")
	# time.sleep(1)
	# print("c")
	main(MyDriver(net=net))
	# print("d")
	with open("mydata.txt",'r') as f:
		fitt=f.read()
	# os.system('pkill torcs')
	subprocess.call('./autostop.sh',shell=True)
	print("fitness *******************   ",fitt)
	return float(fitt)

def eval_genomes(genomes, config):
	for genome_id, genome in genomes:
		genome.fitness = eval_genome(genome, config)


def run():
    # Load the config file, which is assumed to live in
    # the same directory as this script.



	pop = Checkpointer().restore_checkpoint("neat-checkpoint-27")
	# local_dir = os.path.dirname(__file__)
	# config_path = os.path.join(local_dir, 'config-ctrnn')
	# config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
	#                      neat.DefaultSpeciesSet, neat.DefaultStagnation,
	#                      config_path)
	# pop = neat.Population(config)
	stats = neat.StatisticsReporter()
	check=Checkpointer(2,time_interval_seconds=None)
	pop.add_reporter(stats)
	pop.add_reporter(check)
	pop.add_reporter(neat.StdOutReporter(True))

	pe = neat.ParallelEvaluator(1, eval_genome)
	winner = pop.run(pe.evaluate,500)

	# Save the winner.
	with open('winner-feedforward', 'wb') as f:
	    pickle.dump(winner, f)

	print(winner)

    # visualize.plot_stats(stats, ylog=True, view=True, filename="feedforward-fitness.svg")
    # visualize.plot_species(stats, view=True, filename="feedforward-speciation.svg")

    # node_names = {-1: 'x', -2: 'dx', -3: 'theta', -4: 'dtheta', 0: 'control'}
    # visualize.draw_net(config, winner, True, node_names=node_names)

    # visualize.draw_net(config, winner, view=True, node_names=node_names,
    #                    filename="winner-feedforward.gv")
    # visualize.draw_net(config, winner, view=True, node_names=node_names,
    #                    filename="winner-feedforward-enabled.gv", show_disabled=False)
    # visualize.draw_net(config, winner, view=True, node_names=node_names,
    #                    filename="winner-feedforward-enabled-pruned.gv", show_di
    	# print(x)




if __name__ == '__main__':
    run()
    #main(Driver())

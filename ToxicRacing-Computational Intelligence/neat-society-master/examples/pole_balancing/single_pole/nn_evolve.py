"""
Single-pole balancing experiment using a discrete-time recurrent neural network.
"""

from __future__ import print_function

import os
import pickle

import cart_pole

from neatsociety import nn, parallel, population, visualize
from neatsociety.config import Config
from neatsociety.math_util import mean

runs_per_net = 5
num_steps = 60000 # equivalent to 1 minute of simulation time


# Use the NN network phenotype and the discrete actuator force function.
def evaluate_genome(g):
    net = nn.create_feed_forward_phenotype(g)

    fitnesses = []

    for runs in range(runs_per_net):
        sim = cart_pole.CartPole()

        # Run the given simulation for up to num_steps time steps.
        fitness = 0.0
        for s in range(num_steps):
            inputs = sim.get_scaled_state()
            action = net.serial_activate(inputs)

            # Apply action to the simulated cart-pole
            force = cart_pole.discrete_actuator_force(action)
            sim.step(force)

            # Stop if the network fails to keep the cart within the position or angle limits.
            # The per-run fitness is the number of time steps the network can balance the pole
            # without exceeding these limits.
            if abs(sim.x) >= sim.position_limit or abs(sim.theta) >= sim.angle_limit_radians:
                break

            fitness += 1.0

        fitnesses.append(fitness)

    # The genome's fitness is its worst performance across all runs.
    return min(fitnesses)


# Load the config file, which is assumed to live in
# the same directory as this script.
local_dir = os.path.dirname(__file__)
config = Config(os.path.join(local_dir, 'nn_config'))

pop = population.Population(config)
pe = parallel.ParallelEvaluator(evaluate_genome)
pop.run(pe.evaluate, 2000)

# Save the winner.
print('Number of evaluations: {0:d}'.format(pop.total_evaluations))
winner = pop.statistics.best_genome()
with open('nn_winner_genome', 'wb') as f:
    pickle.dump(winner, f)

print(winner)

# Plot the evolution of the best/average fitness.
visualize.plot_stats(pop.statistics, ylog=True, filename="nn_fitness.svg")
# Visualizes speciation
visualize.plot_species(pop.statistics, filename="nn_speciation.svg")
# Visualize the best network.
visualize.draw_net(winner, view=True, filename="nn_winner.gv")
visualize.draw_net(winner, view=True, filename="nn_winner-enabled.gv", show_disabled=False)
visualize.draw_net(winner, view=True, filename="nn_winner-enabled-pruned.gv", show_disabled=False, prune_unused=True)

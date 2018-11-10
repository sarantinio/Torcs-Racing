#!/usr/bin/python3
import os
import sys
sys.path.insert(0, '/home/peter/code/projects/MultiNEAT') # duh

import time
import random as rnd
import subprocess as comm
import cv2
import numpy as np
import pickle as pickle
import MultiNEAT as NEAT
from MultiNEAT import GetGenomeList, ZipFitness
from MultiNEAT import EvaluateGenomeList_Serial

from concurrent.futures import ProcessPoolExecutor, as_completed
import subprocess

from pytocl.main import main
from my_driver import MyDriver
params = NEAT.Parameters()
params.PopulationSize = 100

params.DynamicCompatibility = True
params.CompatTreshold = 2.0
params.YoungAgeTreshold = 5
params.SpeciesMaxStagnation = 3
params.OldAgeTreshold = 35
params.MinSpecies = 5
params.MaxSpecies = 15
params.RouletteWheelSelection = False

params.MutateRemLinkProb = 0.2
params.RecurrentProb = 0.5
params.OverallMutationRate = 0.9
params.MutateAddLinkProb = 0.9
params.MutateAddNeuronProb = 0.7
params.MutateWeightsProb = 0.90
params.MaxWeight = 15.0
params.WeightMutationMaxPower = 0.7
params.WeightReplacementMaxPower = 1.0

params.MutateActivationAProb = 0.0
params.ActivationAMutationMaxPower = 0.5
params.MinActivationA = 0.05
params.MaxActivationA = 6.0

params.MutateNeuronActivationTypeProb = 0.09

params.ActivationFunction_SignedSigmoid_Prob = 0.0
params.ActivationFunction_UnsignedSigmoid_Prob = 0.0
params.ActivationFunction_Tanh_Prob = 1.0
params.ActivationFunction_TanhCubic_Prob = 0.0
params.ActivationFunction_SignedStep_Prob = 1.0
params.ActivationFunction_UnsignedStep_Prob = 0.0
params.ActivationFunction_SignedGauss_Prob = 1.0
params.ActivationFunction_UnsignedGauss_Prob = 0.0
params.ActivationFunction_Abs_Prob = 0.0
params.ActivationFunction_SignedSine_Prob = 1.0
params.ActivationFunction_UnsignedSine_Prob = 0.0
params.ActivationFunction_Linear_Prob = 1.0


params.AllowLoops = True
params.DivisionThreshold = 0.5
params.VarianceThreshold = 0.3
params.BandThreshold = 0.3
params.InitialDepth = 1
params.MaxDepth = 3
params.IterationLevel = 2
params.Leo = True
params.GeometrySeed = True
params.LeoSeed = True
params.LeoThreshold = 0.3
params.CPPN_Bias = -1.0
params.Qtree_X = 1.0
params.Qtree_Y = 1.0
params.Width = 2.
params.Height = 1.
params.Elitism = 0.1

rng = NEAT.RNG()
rng.TimeSeed()
meh=[]

for i in range(9):
    meh.append((-2,-i/9,1))

# for i in range(9):
#     meh.append((2,-i/9,1))



# for i in range(41):
#     if i >2 and i<12:
         
#         meh.append((-(i-2)/9,-1.,-1.))
#     elif i>11 and i<22:
#         meh.append(((i-11)/9,-1.,1.))
meh.append((0,0.5,-1))
meh.append((-0.5,0.5,-1))
meh.append((0.5,0.5,-1))
meh.append((0,-1,-1))
	# else:
	# 	meh.append((i/11.,-1.,1.))
	# 	meh.append(((i-0)/41,-1,0))
	# elif i >10 and i<14:
	# 	meh.append(((i-0)/41,-1,0))
	# else:
	# 	meh.append((i/41,-1.,0.))
print(meh)			
substrate = NEAT.Substrate(meh,#(1., -1, 1.),(0., -1, 1.)],
                           [(0., 0, 1.),(-1.,0,1.0),(1.,0,1.0)],
                           [(-1.9, 1., 1.),(1.9, 1., 1.)])#(-1.9, 1., 1.),(-1.3, 1., 1.),(-0.7, 1., 1.),(0, 1., 1.),(0.7, 1., 1.),(1.3, 1., 1.),(1.9, 1., 1.),])

substrate.m_allow_input_hidden_links = True
substrate.m_allow_input_output_links = True
substrate.m_allow_hidden_hidden_links = True
substrate.m_allow_hidden_output_links = True
substrate.m_allow_output_hidden_links = True
substrate.m_allow_output_output_links = True
substrate.m_allow_looped_hidden_links = True
substrate.m_allow_looped_output_links = True

substrate.m_allow_input_hidden_links = True
substrate.m_allow_input_output_links = True
substrate.m_allow_hidden_output_links = True
substrate.m_allow_hidden_hidden_links = True

substrate.m_hidden_nodes_activation = NEAT.ActivationFunction.SIGNED_SIGMOID
substrate.m_output_nodes_activation = NEAT.ActivationFunction.UNSIGNED_SIGMOID

substrate.m_with_distance = True

substrate.m_max_weight_and_bias = 8.0


def evaluate_xor(genome):
    net = NEAT.NeuralNetwork()
    genome.BuildHyperNEATPhenotype(net, substrate)
    # nn=genome.BuildHyperNEATPhenotype(net, substrate)
    # error = 0
    # depth = 5

    # do stuff and return the fitness
    # net.Flush()
    net = NEAT.NeuralNetwork()
    genome.BuildPhenotype(net)
    img = np.zeros((400, 400, 3), dtype=np.uint8)
    img += 10
    NEAT.DrawPhenotype(img, (0, 0, 400, 400), net)
    cv2.imshow("CPPN", img)
    # Visualize best network's Pheotype
    net = NEAT.NeuralNetwork()
    genome.BuildESHyperNEATPhenotype(net, substrate, params)
    img = np.zeros((800, 800, 3), dtype=np.uint8)
    img += 10

    NEAT.DrawPhenotype(img, (0, 0, 800, 800), net, substrate=True)
    cv2.imshow("NN", img)
    cv2.waitKey(33)

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
    # print("fitness *******************   ",fitt)
    return float(fitt)

    # except Exception as ex:
    #     print('Exception meheh:', ex)
    #     return 0.0


def getbest(run):
    g = NEAT.Genome(0,
                     substrate.GetMinCPPNInputs(),
                    3,
                    substrate.GetMinCPPNOutputs(),
                    False,
                    NEAT.ActivationFunction.TANH,
                    NEAT.ActivationFunction.TANH,
                    0,
                    params)

    pop = NEAT.Population(g, params, True, 1.0, run)
    maxf_ever = 0
    hof = []
    for generation in range(300):
        # Evaluate genomes
        genome_list = NEAT.GetGenomeList(pop)

        fitnesses = EvaluateGenomeList_Serial(genome_list, evaluate_xor, display=True)
        [genome.SetFitness(fitness) for genome, fitness in zip(genome_list, fitnesses)]

        print('Gen: %d Best: %3.5f' % (generation, max(fitnesses)))

        # Print best fitness
        # print("---------------------------")
        # print("Generation: ", generation)
        # print("max ", max([x.GetLeader().GetFitness() for x in pop.Species]))
        # maxf = max([x.GetFitness() for x in NEAT.GetGenomeList(pop)])
        # print('Generation: {}, max fitness: {}'.format(generation, maxf))

        # if maxf > maxf_ever:
        # 	with open("lastGenWinner",'w') as f:

        #     	f.write(pickle.dumps(net)
        #     maxf_ever = maxf


        # Visualize best network's Genome

        net = NEAT.NeuralNetwork()
        pop.Species[0].GetLeader().BuildPhenotype(net)
        # img = np.zeros((400, 400, 3), dtype=np.uint8)
        # img += 10
        # NEAT.DrawPhenotype(img, (0, 0, 400, 400), net)
        # cv2.imshow("CPPN", img)
        # # Visualize best network's Pheotype
        # net = NEAT.NeuralNetwork()
        pop.Species[0].GetLeader().BuildESHyperNEATPhenotype(net, substrate, params)
        # img = np.zeros((400, 400, 3), dtype=np.uint8)
        # img += 10

        # NEAT.DrawPhenotype(img, (0, 0, 400, 400), net, substrate=True)
        # cv2.imshow("NN", img)
        # cv2.waitKey(33)
        # time.sleep(2)



        with open('winnerGenome', 'wb') as f:
            pickle.dump(str(pop.GetBestGenome()),f)
        with open('winnerNet', 'wb') as f:
            pickle.dump(str(net), f)
        with open('winnerSub', 'wb') as f:
            pickle.dump(str(substrate), f)
        with open('winnerParams', 'wb') as f:
            pickle.dump(str(params), f)

        if max(fitnesses) > 20000.0:
            break

        # Epoch
        generations = generation
        pop.Epoch()

    return generations


gens = []
for run in range(1):
    gen = getbest(run)

    gens += [gen]
    print('Run:', run, 'Generations to solve XOR:', gen)
avg_gens = sum(gens) / len(gens)

print('All:', gens)
print('Average:', avg_gens)

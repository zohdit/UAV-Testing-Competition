import json
from timer import Timer
import numpy as np
from os.path import join
import random
import copy

import shutil
from testcase import TestCase
from aerialist.px4.drone_test import DroneTest
from aerialist.px4.obstacle import Obstacle

from evaluator import Evaluator
from config import CASE_STUDY, RUN, FEATURES
from obstacle_mutator import ObstacleMutator
from folder import Folder



class Individual(object):
    # Global counter of all the individuals (it is increased each time an individual is created or mutated).
    COUNT = 0
    SEEDS = set()
    COUNT_MISS = 0

    def __init__(self, member1:Obstacle, member2:Obstacle, seed):
        self.id = Individual.COUNT
        self.seed = seed
        self.ff = None
        self.obstacle1 = member1
        self.obstacle2 = member2
        self.features = tuple()
        self.run = RUN
        self.seed = seed
        self.features = FEATURES
        self.tool = "DeepHyperion"
        self.rank = np.inf
        self.selected_counter = 0
        self.placed_mutant = 0
        self.timestamp, self.elapsed_time = Timer.get_timestamps()
        self.test = None

    def reset(self):
        self.ff = None
        self.rank = np.inf
        self.selected_counter = 0
        self.placed_mutant = 0


    def evaluate(self, test_case):
        case_study = DroneTest.from_yaml(test_case)
        self.test = TestCase(case_study, [self.obstacle1, self.obstacle2])
        if self.ff is None:          
            distances = Evaluator.evaluate(self)
            self.ff = distances
        return self.ff

    def mutate(self):
        mutant_obstacle1 = self.obstacle1
        mutant_obstacle2 = self.obstacle2
        rand = random.randint(0, 1)
        if rand == 0: 
            mutant_obstacle1 = ObstacleMutator(self.obstacle1).mutate()
        else:
            mutant_obstacle2 = ObstacleMutator(self.obstacle2).mutate()

        while(mutant_obstacle1.intersects(mutant_obstacle2)):
            if rand == 0: 
                mutant_obstacle1 = ObstacleMutator(self.obstacle1).mutate()
            else:
                mutant_obstacle2 = ObstacleMutator(self.obstacle2).mutate()

        self.obstacle1 = mutant_obstacle1
        self.obstacle2 = mutant_obstacle2
        self.reset()

    def to_dict(self):
        return {'id': str(self.id),
                'seed': str(self.seed),
                'misbehaviour': self.is_misbehavior(),
                'performance': str(self.ff),
                'timestamp': str(self.timestamp),
                'elapsed': str(self.elapsed_time),
                'tool' : str(self.tool),
                'run' : str(self.run),
                'features': self.features,
                'rank': str(self.rank),
                'selected': str(self.selected_counter),
                'placed_mutant': str(self.placed_mutant), 
                'obstacle1': self.obstacle1.to_dict(),
                'obstacle2': self.obstacle2.to_dict()
        }


    def dump(self, filename):
        self.test.save_yaml(filename+".yaml")
        data = self.to_dict()
        filedest = filename+".json"
        with open(filedest, 'w') as f:
            (json.dump(data, f, sort_keys=True, indent=4))
        if self.ff != 10000:
            shutil.copy2(self.test.log_file, f"{filename}.ulg")
            shutil.copy2(self.test.plot_file, f"{filename}.png")

    def is_misbehavior(self):
        if self.ff >= 1.5:
            return False
        else:
            return True

    def export(self, all=False):
        if self.is_misbehavior():
            dst = join(Folder.DST_MIS, "mbr"+str(self.id))
            self.dump(dst)
        if all:
            dst = join(Folder.DST_ALL, "mbr"+str(self.id))
        else:
            dst = join(Folder.DST_ARC, "mbr"+str(self.id))
        self.dump(dst)

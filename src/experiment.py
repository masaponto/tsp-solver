#!/usr/bin/env python

import argparse
import os
import sys
import time
import numpy as np

from tabulate import tabulate

from utils import read_graph, get_cost
from simulated_annealing import simulated_anealing
from tabu_search import tabu_search


def time_mesure(solver, graph, n=10):
    runnig_time_list = []
    result_list = []

    for i in range(n):
        start = time.time()
        s = solver(graph)
        runing_time = time.time() - start

        runnig_time_list.append(runing_time)
        result_list.append(s)

    return result_list, runnig_time_list


def experiment(solver, graph):
    results, times = time_mesure(solver, graph)

    costs = [get_cost(r, graph) for r in results]

    # tabu list result
    c_max = max(costs)
    c_min = min(costs)
    c_ave = np.average(costs)

    t_max = max(times)
    t_min = min(times)
    t_ave = np.average(times)

    table = [["Cost"] + [c_max] + [c_min] + [c_ave],
             ["Time [s]"] + [t_max] + [t_min] + [t_ave]]

    header = [" ", "MAX", "MIN", "AVE"]

    return tabulate(table, header, tablefmt="pipe")


def main():

    p = argparse.ArgumentParser(
        description='This script is for experiment of solving TSP with TS and SA')
    p.add_argument('-g', '--graph', type=str,
                   help='path to graph csv file', required=True)

    option_args = p.parse_known_args()[0]
    path = option_args.graph

    if not os.path.exists(path):
        print("File not found")
        sys.exit(1)

    graph = read_graph(path)

    tabu_table = experiment(tabu_search, graph)
    sa_table = experiment(simulated_anealing, graph)

    print("## Tabu Search Result")
    print(tabu_table)
    print()

    print("## Simulated Anealing Result")
    print(sa_table)
    print()


if __name__ == "__main__":
    main()

from state_encoding import JobShopProblem
from state_encoding import Schedule
import matplotlib.pyplot as plt
import math
import time
import random
import copy



def calc_probability(delta: float, t: float):
    prob = (1 / (1 + math.exp((-1) * delta) / t))
    return prob


def just_valid_neighbours(neighbourhood):
    non_valid_neighbours = set()
    for neighbour in neighbourhood:
        if not neighbour.is_valid():
            non_valid_neighbours.add(neighbour)
    return list(set(neighbourhood) - non_valid_neighbours)


def simulated_annealing_one(problem: JobShopProblem, max_time = 900, r = 0.1, t_max = 100000000, t_min = 1):
    start_time = time.time()
    initial_solution = Schedule.create_from_problem(problem)
    best_solution = initial_solution.copy()
    j = 0
    t = t_max
    while t >= t_min or time.time() - start_time <= 900:
        local_opt_count = 0
        sol = initial_solution.copy()
        if sol.get_length() < best_solution.get_length():
            best_solution = sol.copy()       
        neighbours = just_valid_neighbours(sol.get_neighbourhood())
        t = t * math.exp((-1) * j * r)
        if(t <= 0):
            break
        local_opt = sol.copy()
        while neighbours and local_opt_count <= 10:
                neighbour = neighbours.pop(0)
                delta = sol.get_length() - neighbour.get_length()
                if delta >= 0:
                    sol = neighbour.copy()
                    neighbours = just_valid_neighbours(sol.get_neighbourhood())                    
                    if neighbour.get_length() < local_opt.get_length():
                        local_opt = neighbour.copy()
                        if local_opt.get_length() < best_solution.get_length():
                            best_solution = local_opt.copy()
                            local_opt_count = 0
                            
                    else:
                        local_opt_count += 1
                elif random.random() < calc_probability(delta, t):
                        sol = neighbour.copy()
                        neighbours = just_valid_neighbours(sol.get_neighbourhood())
                        local_opt_count += 1
        j += 1
    return best_solution


def main():


    problem = JobShopProblem.load_from_file("data/abz5")   

    #solution
    solution = simulated_annealing_one(problem)
    print("\nsol: ", solution.get_length())
    fig = plt.figure()
    fig.add_subplot(1, 1, 1)
    solution.visualize()
    plt.show()


if __name__ == "__main__":
    main()
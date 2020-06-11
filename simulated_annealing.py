from state_encoding import JobShopProblem
from state_encoding import Schedule
import matplotlib.pyplot as plt
import math
import time
import random



def calc_probability(delta: float, t: float):
    prob = (1 / (1 + math.exp((-1) * delta) / t))
    return prob


def just_valid_neighbours(neighbourhood):
    non_valid_neighbours = set()
    for n in neighbourhood:
        if not n.is_valid():
            non_valid_neighbours.add(n)
    return list(set(neighbourhood) - non_valid_neighbours)


def simulated_annealing_one(problem: JobShopProblem, max_time = 800, r = 0.005, t_max = 100000000, t_min = 1):
    start_time = time.time()
    initial_solution = Schedule.create_from_problem(problem)
    best_solution = initial_solution.copy()
    j = 0
    #temperature t
    t = t_max
    while t >= t_min and time.time() - start_time <= max_time:
        opt_count = 0
        sol = initial_solution.copy()    
        neighbours = just_valid_neighbours(sol.get_neighbourhood())
        t = t * math.exp((-1) * j * r)
        if(t <= 0):
            break
        local_opt = sol.copy()
        while neighbours and opt_count <= 70:
                neighbour = neighbours.pop(0)
                delta = sol.get_length() - neighbour.get_length()
                if delta >= 0:
                    sol = neighbour.copy()
                    neighbours = just_valid_neighbours(sol.get_neighbourhood())                    
                    if neighbour.get_length() < local_opt.get_length():
                        local_opt = neighbour.copy()
                        if local_opt.get_length() < best_solution.get_length():
                            best_solution = local_opt.copy()
                            opt_count = 0                      
                    else:
                        opt_count += 1
                elif random.random() < calc_probability(delta, t):
                        sol = neighbour.copy()
                        neighbours = just_valid_neighbours(sol.get_neighbourhood())
                        
                else:
                    opt_count += 1
        j += 1
    return best_solution, time.time() - start_time


def simulated_annealing_two(problem: JobShopProblem, max_time = 800, r = 0.001, t_max = 100000000, t_min = 1):
    start_time = time.time()
    initial_solution = Schedule.create_from_problem(problem)
    best_solution = initial_solution.copy()
    j = 0
    t = t_max
    while t >= t_min and time.time() - start_time <= max_time:
        opt_count = 0
        sol = initial_solution.copy()
        t = t * math.exp((-1) * j * r)
        if(t <= 0):
            break
        local_opt = sol.copy()
        neighbours = sol._random_neighbour_generator()
        neighbour = neighbours.__next__()
        while opt_count <= 100:
            delta = sol.get_length() - neighbour.get_length()
            if delta >= 0:
                sol = neighbour.copy()
                neighbours = sol._random_neighbour_generator()                  
                if sol.get_length() < local_opt.get_length():
                    local_opt = sol.copy()
                    if local_opt.get_length() < best_solution.get_length():
                        best_solution = sol.copy()
                        opt_count = 0                         
                else:
                    opt_count += 1
            elif random.random() < calc_probability(delta, t):
                sol = neighbour.copy()
                neighbours = sol._random_neighbour_generator()              
            else:
                opt_count += 1 
            neighbour = neighbours.__next__()
            if neighbour == None:
                print("NONENclear")
                break
        j += 1
    best_solution.print_schedule()
    return best_solution, time.time() - start_time


def simulated_annealing_three(problem: JobShopProblem, max_time = 800, r = 0.001, t_max = 100000000, t_min = 1):
    start_time = time.time()
    initial_solution = Schedule.create_from_problem(problem)
    best_solution = initial_solution.copy()
    j = 0
    t = t_max
    while t >= t_min and time.time() - start_time <= max_time:
        opt_count = 0
        sol = initial_solution.copy()
        t = t * math.exp((-1) * j * r)
        if(t <= 0):
            break
        local_opt = sol.copy()
        neighbours = sol._random_neighbour_generator_two()
        neighbour = neighbours.__next__()
        while opt_count <= 100:
            delta = sol.get_length() - neighbour.get_length()
            if delta >= 0:
                sol = neighbour.copy()
                neighbours = sol._random_neighbour_generator_two()                  
                if sol.get_length() < local_opt.get_length():
                    local_opt = sol.copy()
                    if local_opt.get_length() < best_solution.get_length():
                        best_solution = sol.copy()
                        opt_count = 0                         
                else:
                    opt_count += 1
            elif random.random() < calc_probability(delta, t):
                sol = neighbour.copy()
                neighbours = sol._random_neighbour_generator_two()              
            else:
                opt_count += 1 
            neighbour = neighbours.__next__()
            if neighbour == None:
                print("NONENclear")
                break
        j += 1
    best_solution.print_schedule()
    return best_solution, time.time() - start_time


    

def main():

     
    """
    #solution
    problem = JobShopProblem.load_from_file("data/4x4")
    solution, run_time = simulated_annealing_one(problem)
    print("\nsol1: ", solution.get_length())
    print("run_time: ", run_time)
    fig = plt.figure()
    fig.add_subplot(1, 1, 1)
    solution.visualize()
    plt.show()
    """

    #solution with neighbourhood generator  
    problem = JobShopProblem.load_from_file("data/3x3")
    solution, run_time = simulated_annealing_three(problem)
    print("\nsol2: ", solution.get_length())
    print("run_time: ", run_time)
    fig = plt.figure()
    fig.add_subplot(1, 1, 1)
    solution.visualize()
    plt.savefig("images/" + str(run_time) + ".png")

    problem = JobShopProblem.load_from_file("data/4x4")
    solution, run_time = simulated_annealing_three(problem)
    print("\nsol2: ", solution.get_length())
    print("run_time: ", run_time)
    fig = plt.figure()
    fig.add_subplot(1, 1, 1)
    solution.visualize()
    plt.show()
    


if __name__ == "__main__":
    main()
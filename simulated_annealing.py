from state_encoding import JobShopProblem
from state_encoding import Schedule
import matplotlib.pyplot as plt
import math
import time
import random
import os



def calc_probability_three(delta: float, t: float):
    if delta < -700.0:
        delta = -700.0
    elif delta > 700.0:
        delta = 700.0
    prob = (1 / (1 + (math.exp((-1) * delta) / t)))
    return prob

def calc_probability_two(delta: float, t: float):
    prob = (1 / (1 + math.exp(delta / t)))
    return prob


def calc_probability(delta: float, t: float):
    prob = math.exp(-1*(delta / t))
    return prob



def simulated_annealing(problem: JobShopProblem, max_time = 4000, r = 0.0008, t_max = 5000, t_min = 1):
    start_time = time.time()
    initial_solution = Schedule.create_from_problem(problem)
    best_solution = initial_solution.copy()
    sol = initial_solution.copy()
    j = 0
    t = t_max
    num_pro = 0
    num_wh = 0
    while t >= t_min and time.time() - start_time <= max_time:
        opt_count = 0
        t = t * math.exp((-1) * j * r)
        if(t <= 0):
            break
        sol = initial_solution.copy()
        local_opt = sol.copy()
        neighbours = sol._random_neighbour_generator()
        neighbour = neighbours.__next__()
        while opt_count <= 900:
            num_wh += 1
            delta = neighbour.get_length() - sol.get_length()
            if delta <= 0:
                sol = neighbour.copy()
                neighbours = sol._random_neighbour_generator()                  
                if sol.get_length() < local_opt.get_length():
                    local_opt = sol.copy()
                    if local_opt.get_length() < best_solution.get_length():
                        best_solution = sol.copy()
                        opt_count = 0                         
                else:
                    opt_count += 1
            elif random.random() <= calc_probability(delta, t):
                opt_count += 1 
                sol = neighbour.copy()
                neighbours = sol._random_neighbour_generator() 
                num_pro += 1             
            else:
                opt_count += 1 
            neighbour = neighbours.__next__()
            if neighbour == None:
                print("NONENclear")
                break
        j += 1
    print("wh : ", num_wh)
    print("prob_c: ", num_pro)
    return best_solution, time.time() - start_time


"""
def simulated_annealing_two(problem: JobShopProblem, max_time = 4000, r = 0.001, t_max = 100000000, t_min = 1):
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
        while opt_count <= 120:
            delta = neighbour.get_length() - sol.get_length()
            if delta <= 0:
                sol = neighbour.copy()
                neighbours = sol._random_neighbour_generator()                  
                if sol.get_length() < local_opt.get_length():
                    local_opt = sol.copy()
                    if local_opt.get_length() < best_solution.get_length():
                        best_solution = sol.copy()
                        opt_count = 0                         
                else:
                    opt_count += 1
            elif random.random() < calc_probability_two(delta, t):
                sol = neighbour.copy()
                neighbours = sol._random_neighbour_generator()              
            else:
                opt_count += 1 
            neighbour = neighbours.__next__()
            if neighbour == None:
                print("NONENclear")
                break
        j += 1
    return best_solution, time.time() - start_time
"""



def simulated_annealing_three(problem: JobShopProblem, max_time = 4000, r = 0.0008, t_max = 10000, t_min = 1):
    start_time = time.time()
    initial_solution = Schedule.create_from_problem(problem)
    best_solution = initial_solution.copy()
    j = 0
    t = t_max
    num_pro = 0
    num_wh = 0
    while t >= t_min and time.time() - start_time <= max_time:
        opt_count = 0
        sol = initial_solution.copy()
        t = t * math.exp((-1) * j * r)
        if(t <= 0):
            break
        local_opt = sol.copy()
        neighbours = sol._random_neighbour_generator()
        neighbour = neighbours.__next__()
        while opt_count <= 900:
            num_wh += 1
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
            elif random.random() < calc_probability_three(delta, t):
                sol = neighbour.copy()
                neighbours = sol._random_neighbour_generator()
                num_pro += 1              
            else:
                opt_count += 1 
            neighbour = neighbours.__next__()
            if neighbour == None:
                print("NONENclear")
                break
        j += 1
    return best_solution, time.time() - start_time


def simulated_annealing_four(problem: JobShopProblem, max_time = 4000, r = 0.0008, t_max = 10000, t_min = 1):
    start_time = time.time()
    initial_solution = Schedule.create_from_problem(problem)
    best_solution = initial_solution.copy()
    j = 0
    t = t_max
    while t >= t_min and time.time() - start_time <= max_time:
        opt_count = 0
        t = t * math.exp((-1) * j * r)
        if(t <= 0):
            break
        sol = initial_solution.copy()
        local_opt = sol.copy()
        neighbours = sol._random_neighbour_generator()
        neighbour = neighbours.__next__()
        while opt_count <= 900:
            delta = neighbour.get_length() - sol.get_length()
            if delta <= 0:
                if  random.random() <= calc_probability(delta, t):
                    sol = neighbour.copy()
                    neighbours = sol._random_neighbour_generator()                  
                    if sol.get_length() < local_opt.get_length():
                        local_opt = sol.copy()
                        if local_opt.get_length() < best_solution.get_length():
                            best_solution = sol.copy()
                            opt_count = 0                         
                    else:
                        opt_count += 1
            elif random.random() <= calc_probability(delta, t):
                sol = neighbour.copy()
                neighbours = sol._random_neighbour_generator()              
            else:
                opt_count += 1 
            neighbour = neighbours.__next__()
            if neighbour == None:
                print("NONENclear")
                break
        j += 1
    return best_solution, time.time() - start_time




def simulated_annealing_five(problem: JobShopProblem, max_time = 4000, r = 0.0008, t_max = 10000, t_min = 1):
    start_time = time.time()
    initial_solution = Schedule.create_from_problem(problem)
    best_solution = initial_solution.copy()
    j = 0
    t = t_max
    num_pro = 0
    num_wh = 0
    while t >= t_min and time.time() - start_time <= max_time:
        opt_count = 0
        sol = initial_solution.copy()
        t = t * math.exp((-1) * j * r)
        if(t <= 0):
            break
        local_opt = sol.copy()
        neighbours = sol._random_neighbour_generator_two()
        neighbour = neighbours.__next__()
        while opt_count <= 900:
            num_wh += 1
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
            elif random.random() < calc_probability_three(delta, t):
                sol = neighbour.copy()
                neighbours = sol._random_neighbour_generator_two()
                num_pro += 1              
            else:
                opt_count += 1 
            neighbour = neighbours.__next__()
            if neighbour == None:
                print("NONENclear")
                break
        j += 1
    return best_solution, time.time() - start_time

    

def main():

    
    #solution with neighbourhood generator 
    table = "5x5" 
    problem = JobShopProblem.load_from_file("data/" + table)
    solution, run_time = simulated_annealing(problem)
    solution.print_schedule()
    length = solution.get_length()
    print("\nsol1: ", length)
    print("run_time: ", run_time)
    fig = plt.figure()
    fig.add_subplot(1, 1, 1)
    solution.visualize()
    path_1 = "images/sa1/" + table
    if not os.path.exists(path_1):
        os.mkdir(path_1)
    plt.savefig(path_1 +"/" + str(length) + str(run_time) + ".png")

    print("\n--------------------------\n")
    problem = JobShopProblem.load_from_file("data/" + table)
    solution, run_time = simulated_annealing_three(problem)
    length = solution.get_length()
    print("\nsol3c: ", length)
    print("run_time: ", run_time)
    fig = plt.figure()
    fig.add_subplot(1, 1, 1)
    solution.visualize()
    path_1 = "images/sa2/" + table
    if not os.path.exists(path_1):
        os.mkdir(path_1)
    plt.savefig(path_1 + "/" + str(length) + str(run_time) + ".png")
    
    """
    problem = JobShopProblem.load_from_file("data/" + table)
    solution, run_time = simulated_annealing_two(problem)
    length = solution.get_length()
    print("\nsol2: ", length)
    print("run_time: ", run_time)
    fig = plt.figure()
    fig.add_subplot(1, 1, 1)
    solution.visualize()
    path_1 = "images/sa2/" + table
    if not os.path.exists(path_1):
        os.mkdir(path_1)
    plt.savefig(path_1 +"/" + str(length) + str(run_time) + ".png")
    """
    """
    problem = JobShopProblem.load_from_file("data/" + table)
    solution, run_time = simulated_annealing_three(problem)
    length = solution.get_length()
    print("\nsol3: ", length)
    print("run_time: ", run_time)
    fig = plt.figure()
    fig.add_subplot(1, 1, 1)
    solution.visualize()
    path_1 = "images/sa3/" + table
    if not os.path.exists(path_1):
        os.mkdir(path_1)
    plt.savefig(path_1 +"/" + str(length) + str(run_time) + ".png")
    """
    print("\n--------------------------\n")
    problem = JobShopProblem.load_from_file("data/" + table)
    solution, run_time = simulated_annealing_four(problem)
    length = solution.get_length()
    print("\nsol4: ", length)
    print("run_time: ", run_time)
    fig = plt.figure()
    fig.add_subplot(1, 1, 1)
    solution.visualize()
    path_1 = "images/sa3/" + table
    if not os.path.exists(path_1):
        os.mkdir(path_1)
    plt.savefig(path_1 +"/" + str(length) + str(run_time) + ".png")


    print("\n--------------------------\n")
    problem = JobShopProblem.load_from_file("data/" + table)
    solution, run_time = simulated_annealing_five(problem)
    length = solution.get_length()
    print("\nsol4: ", length)
    print("run_time: ", run_time)
    fig = plt.figure()
    fig.add_subplot(1, 1, 1)
    solution.visualize()
    path_1 = "images/sa4/" + table
    if not os.path.exists(path_1):
        os.mkdir(path_1)
    plt.savefig(path_1 +"/" + str(length) + str(run_time) + ".png")
    

    


if __name__ == "__main__":
    main()
from sa.state_encoding import JobShopProblem
from sa.state_encoding import Schedule
import matplotlib.pyplot as plt
import math
import time
import random
import os
from .controller import TableController, ResultController




def calc_probability(delta: float, t: float):
    prob = math.exp(-1*(delta / t))
    return prob



def simulated_annealing(problem: JobShopProblem, max_time = 4000, r = 0.00005, t_max = 100000, t_min = 1):
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
        while opt_count <= 250:
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
    return best_solution, time.time() - start_time

    

def run_simmulated_annealing(table_text: str, table_id, table_name, r_c : ResultController, temp=10000.0, reduction_rate=0.0001):

    print(temp, reduction_rate)
    #solution with neighbourhood generator  
    problem = JobShopProblem.load(table_text)
    solution, run_time = simulated_annealing(problem, t_max=temp, r=reduction_rate)
    length = solution.get_length()
    print("\nsol2: ", length)
    print("run_time: ", run_time)
    fig = plt.figure()
    fig.add_subplot(1, 1, 1)
    solution.visualize()

    if len(r_c.get_all_results(table_id)) < 10:
        print("path: ", os.getcwd())
        if not os.path.exists("sa/static/images/" + table_id):
           os.mkdir("sa/static/images/" + table_id)
        path_1 ="sa/static/"
        path_2 = "images/" + table_id + "/" + str(length) + str(run_time) + ".png"
        plt.savefig(path_1 + path_2)
        result_id = r_c.add_result(table_id, run_time, length, path_2)
        return result_id
    elif length < r_c.get_worst_solution(table_id).result_length:
        os.remove(path_1 + r_c.get_worst_solution(table_id).result_image)
        r_c.get_worst_solution(table_id).delete()
        if not os.path.exists("sa/static/images/" + table_id):
            os.mkdir("sa/static/images/" + table_id)
        path_1 ="sa/static/"
        path_2 = "images/" + table_id + "/" + str(length) + str(run_time) + ".png"
        plt.savefig(path_1 + path_2)
        result_id = r_c.add_result(table_id, run_time, length, path_2)
        return result_id
    return None

    
        





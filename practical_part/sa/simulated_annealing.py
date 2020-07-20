from sa.state_encoding import JobShopProblem
from sa.state_encoding import Schedule
import matplotlib.pyplot as plt
import math
import time
import random
import os
from .controller import TableController, ResultController



def get_parameters(problem: JobShopProblem):
    temp = 300
    t_decrease = 1.1 - (1/problem.num_jobs)
    count = 4 * problem.num_jobs
    count_increase = 1.1 + (1/(problem.num_jobs))
    return (temp, t_decrease, count, count_increase)


def calc_probability(delta: float, t: float):
    prob = math.exp(-1*(delta / t))
    return prob


def simulated_annealing(problem: JobShopProblem, max_time = 50000, r = 0.01, t_max = 1000, 
t_min = 5, count=50, count_increase=1.2):
    start_time = time.time()
    sol = Schedule.create_from_problem(problem)
    best_solution = sol.copy()
    count_max = 1000
    t = t_max
    while t >= t_min and time.time() - start_time <= max_time:
        h_count = 0
        if t <= 50:
            r = 0.8
        neighbours = sol.random_neighbour_generator()
        neighbour = neighbours.__next__()
        while h_count <= int(count):
            delta = neighbour.get_length() - sol.get_length()
            if delta <= 0:
                sol = neighbour.copy()
                neighbours = sol.random_neighbour_generator()                  
                if sol.get_length() <  best_solution.get_length():
                    best_solution = sol.copy()             
            elif random.random() <= calc_probability(delta, t):
                sol = neighbour.copy()
                neighbours = sol.random_neighbour_generator()
            neighbour = neighbours.__next__()
            if neighbour == None:
                break
            h_count += 1
        t = t * r
        if count < count_max:
            count = count * count_increase
        print("temp: ", t)
    print("c: ", count)
    return best_solution, time.time() - start_time



def simulated_annealing_two(problem: JobShopProblem, max_time = 50000, r = 0.01, t_max = 1000, 
t_min = 5, count=50, count_increase=1.0):
    print("enter")
    start_time = time.time()
    sol = Schedule.create_from_problem(problem)
    best_solution = sol.copy()
    max_count = 1000
    t = t_max
    while t >= t_min and time.time() - start_time <= max_time:
        h_count = 0
        if t <= 50:
            r = 0.8
        neighbours = sol.random_neighbour_generator_three()
        neighbour = neighbours.__next__()
        while h_count <= count:
            delta = neighbour.get_length() - sol.get_length()
            if delta <= 0:
                sol = neighbour.copy()
                neighbours = sol.random_neighbour_generator_three()                  
                if sol.get_length() <  best_solution.get_length():
                    best_solution = sol.copy() 
                    print(best_solution.get_length())            
            elif random.random() <= calc_probability(delta, t):
                sol = neighbour.copy()
                neighbours = sol.random_neighbour_generator_three()
            neighbour = neighbours.__next__()
            if neighbour == None:
                break
            h_count += 1
        if count < max_count:
            count = count * count_increase
        t = t * r
        print("temp: ", t)
        
    return best_solution, time.time() - start_time


    

def run_simmulated_annealing(table_text: str, table_id, table_name, r_c : ResultController, temp=10000.0, reduction_rate=0.0001, count=50, count_increase=1.2, sa_num=0, test=False):
    print(sa_num)
    if sa_num == 0:
            sa = simulated_annealing
    elif sa_num == 1:
            sa = simulated_annealing_two
    


    if test:
    
        #solution with neighbourhood generator  
        problem = JobShopProblem.load(table_text)
        solution, run_time = sa(problem, t_max=temp, r=reduction_rate, count=count, count_increase=count_increase)
        length = solution.get_length()
        print("\nsol2: ", length)
        print("run_time: ", run_time)
        fig = plt.figure()
        fig.add_subplot(1, 1, 1)
        solution.visualize()


    else:
        problem = problem = JobShopProblem.load(table_text)
        param = get_parameters(problem = problem)
        temp = param[0]
        reduction_rate = param[1]
        count = param[2]
        count_increase = param[3]
        solution, run_time = sa(problem, t_max=temp, r=reduction_rate, count=count, count_increase=count_increase)
        length = solution.get_length()
        print("\nsol2: ", length)
        print("run_time: ", run_time)
        fig = plt.figure()
        fig.add_subplot(1, 1, 1)
        solution.visualize()
    

    if len(r_c.get_all_results(table_id)) < 40:
        if not os.path.exists("sa/static/images/" + table_id):
            os.mkdir("sa/static/images/" + table_id)
        path_1 ="sa/static/"
        result_id = r_c.add_result(table_id, run_time, length, count, temp, reduction_rate, count_increase, sa_num)
        path_2 = "images/" + table_id + "/" + "result_"  + str(result_id) + ".png"
        plt.savefig(path_1 + path_2)
        r_c.update_path(result_id, path_2)
        return result_id
    elif length < r_c.get_worst_solution(table_id).result_length:
        os.remove(path_1 + r_c.get_worst_solution(table_id).result_image)
        r_c.get_worst_solution(table_id).delete()
        if not os.path.exists("sa/static/images/" + table_id):
            os.mkdir("sa/static/images/" + table_id)
        path_1 ="sa/static/"
        result_id = r_c.add_result(table_id, run_time, length, count, temp, reduction_rate)
        path_2 = "images/" + table_id + "/" + "result_"  + str(result_id) + ".png"
        plt.savefig(path_1 + path_2)
        r_c.update_path(result_id, path_2)
        return result_id
    return None




    
        





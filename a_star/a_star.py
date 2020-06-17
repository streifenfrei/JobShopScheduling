import time
import copy

class JobPart:

    def __init__(self, j, i, m, t, a=False):

        self.job_number = int(j)
        self.instance = int(i)
        self.machine_number = int(m)
        self.time = int(t)
        self.active = a

    def equal(self, ob):
        if (self.instance == ob.instance) and (self.job_number == ob.job_number):
            if (self.machine_number == ob.machine_number) and (self.time == ob.time) and (self.active == ob.active):               
                return True
            else:               
                return False                
        else:         
            return False


    def to_string(self):
        return str([self.job_number, self.instance, self.machine_number, self.time, self.active])



def get_active_state_duration(state):
    d = 0
    for jp in state:
        if jp.active:
            d += jp.time
    return d




def heuristic(current_state, table, num_machines):
    val = 0
    val = val + get_active_state_duration(current_state)
    for i in range(len(table)):
        for j in range(num_machines):
            for job_part in current_state:
                if i == job_part.job_number and j >= job_part.instance and job_part.machine_number != -1:
                    if not(job_part.active and j == job_part.instance):
                        p = table[i][j]
                        val =  val + int(p[1])
    return (val / (len(table)))


def get_active_parts(current_state):
    actives = set()
    times = list()
    time = 0
    for c in current_state:
        if c.active:
            actives.add(JobPart(c.job_number, c.instance, c.machine_number, c.time, c.active))
            times.append(c.time)
    if len(times) > 0:
        time = min(times)
    return time, actives


def is_machine_free(machine_number, active_instances):
    for a in active_instances:
        if a.machine_number == machine_number:
            return False
    
    return True


def update_job_part(job_part, time, table, num_machines):
    number = job_part.job_number
    if  job_part.time - time <= 0:
        active = False
        inst = job_part.instance + 1
        if  job_part.instance == num_machines - 1:
            mn = - 1
            time = 0
        else:
            entry = table[job_part.job_number][job_part.instance + 1]
            time = int(entry[1])
            mn = int(entry[0])   
        return JobPart(number, inst, mn, time, active)
    else:
        time = job_part.time - time
        mn = job_part.machine_number
        active = True
        inst = job_part.instance
        return JobPart(number, inst, mn, time, active)

    return JobPart(number, inst, entry[0], time, active)

                    
def power_set(ps):
    result = [[]]
    for val in ps:
        new_subset = [subset + [val] for subset in result]
        result.extend(new_subset)
    result.remove([])
    return result


def is_valid(pos, m_numbers):   
    machine_numbers = []
    times = list()
    for elem in pos:
        if elem.instance >= m_numbers and elem.active == False:
            return False, None
        machine_numbers.append(elem.machine_number)
        times.append(elem.time)
    if len(machine_numbers) == len(set(machine_numbers)):
        if len(times) > 0:
            return True, min(times)
        else:
            return True, None
    else: 
        return False, None


def get_neighbours(current_state, table, m_numbers):
    neighbours = list()
    temp = {JobPart(c_s.job_number, c_s.instance, c_s.machine_number, c_s.time, c_s.active) for c_s in current_state}
    time_a, active_instances = get_active_parts(temp)
    temp = temp - active_instances
    all_possibilities = power_set(temp)
    
    for pos in all_possibilities:
        new_state = set()
        if len(active_instances) > 0:
            pos.extend(active_instances)
        validated_pos = is_valid(pos, m_numbers)
        if validated_pos[0]:
            time = validated_pos[1]
            updated_jobs = set()
            for next_p in pos:
                n = update_job_part(next_p, time, table, m_numbers)
                new_state.add(n)
                updated_jobs.add(next_p.job_number)
            for cs in current_state:
                if cs.job_number not in updated_jobs:
                    new_state.add(cs) 
            neighbours.append(new_state)
    
    if len(active_instances) > 0:
        just_active_jobs = set()
        n_s = set()
        for ac in active_instances:
            a = update_job_part(ac, time_a, table, m_numbers)
            n_s.add(a)  
            just_active_jobs.add(ac.job_number)
        for cs in current_state:
            if cs.job_number not in just_active_jobs:
                n_s.add(cs)
        neighbours.append(n_s)

    return neighbours


def state_to_string(state):
        l = [None] * len(state)
        for s in state:
            l[s.job_number] = [s.job_number, s.instance, s.machine_number, s.time, s.active]
        return str(l)



def path_to_string(p):
    path = []
    for state in p:
        l = [None] * len(state)
        for s in state:
            l[s.job_number] = [s.job_number, s.instance, s.machine_number, s.time, s.active]
        path.append(str(l))  
    
    return "-".join(path)


def calc_time(cs, n_state):

    for c in cs:
        for ns in n_state:
            if c.job_number == ns.job_number:
                if c.instance + 1 == ns.instance:
                    return c.time
                elif c.instance == ns.instance and c.time > ns.time:
                    return c.time - ns.time
    
    return 0


def compare_s(first, second):

    val = True
    if len(second) == 0:
        return False
    for f in first:
        for s in second:
            if (f.job_number == s.job_number):
                if not f.equal(s):
                    val =  False
    return val


def a_star_fast(table, start_pos, goal_pos, num_machines):
    print("\n-----NEW----\n")
    
    start_time = time.time()
    visited = set()
    in_queue = set()
    path_queue = dict()

    g = {}
    f = {}

    visited.add(state_to_string(start_pos))
    in_queue.add(state_to_string(start_pos))
    g[path_to_string([start_pos])] = 0.0  
    f[path_to_string([start_pos])] = g[path_to_string([start_pos])] + heuristic(start_pos, table, num_machines)
    best_path_length = f[path_to_string([start_pos])]
    path_queue[best_path_length] = [[start_pos]]
    while path_queue:
        if time.time() - start_time >= 100 * 60:
            return "Error: Time out", None, time.time() - start_time
        best_path_length = min(path_queue.keys())
        path = path_queue[best_path_length].pop(0)
        if len(path_queue[best_path_length]) == 0:
            del path_queue[best_path_length]
        last_state = path[-1]
        if compare_s(goal_pos, last_state) and last_state != [] and g[path_to_string(path)] <= 33:
            return path, g[path_to_string(path)], time.time() - start_time
        visited.add(state_to_string(last_state))
        in_queue.remove(state_to_string(last_state))
        neighbours = get_neighbours(last_state, table, num_machines)
        for neighbour in neighbours:
            if state_to_string(neighbour) not in visited and state_to_string(neighbour) not in in_queue:
                new_path = list(path)
                new_path.append(neighbour)
                g[path_to_string(new_path)] = g[path_to_string(path)] + calc_time(last_state, neighbour)
                valuation = g[path_to_string(new_path)] + heuristic(neighbour, table, num_machines)
                f[path_to_string(new_path)] = g[path_to_string(new_path)] + heuristic(neighbour, table, num_machines)
                if valuation in path_queue.keys():
                    path_queue[valuation].append(new_path)
                else:
                    path_queue[valuation] = []
                    path_queue[valuation].append(new_path)
                in_queue.add(state_to_string(neighbour))
        if best_path_length < 0:
            best_path_length = min(path_queue.keys())
    return "error", None, None


def a_star(table, start_pos, goal_pos, num_machines):
    print("\n-----NEW----\n")
    
    start_time = time.time()
    visited = set()
    in_queue = set()
    path_queue = [[start_pos]]

    g = {}
    f = {}

    visited.add(state_to_string(start_pos))
    in_queue.add(state_to_string(start_pos))
    g[path_to_string([start_pos])] = 0.0  
    f[path_to_string([start_pos])] = g[path_to_string([start_pos])] + heuristic(start_pos, table, num_machines)
    
    while path_queue:
        if time.time() - start_time >= 100 * 60:
            return "Error: Time out", None, time.time() - start_time
        path = path_queue.pop(0)
        last_state = path[-1]
        if compare_s(goal_pos, last_state) and last_state != []:
            return path, g[path_to_string(path)], time.time() - start_time
        visited.add(state_to_string(last_state))
        in_queue.remove(state_to_string(last_state))
        neighbours = get_neighbours(last_state, table, num_machines)
        for neighbour in neighbours:
            if state_to_string(neighbour) not in visited and state_to_string(neighbour) not in in_queue:
                new_path = list(path)
                new_path.append(neighbour)
                g[path_to_string(new_path)] = g[path_to_string(path)] + calc_time(last_state, neighbour)
                f[path_to_string(new_path)] = g[path_to_string(new_path)] + heuristic(neighbour, table, num_machines)
                i = 0
                while i < len(path_queue) and f[path_to_string(path_queue[i])] < f[path_to_string(new_path)]:
                    i += 1
                path_queue.insert(i, new_path)
                in_queue.add(state_to_string(neighbour))
    return "error", None, None


def a_star_main(table, num_machines, num_jobs):
    start_pos = set()
    goal_pos = set()
    for job in range(num_jobs):
        val_s = table[job][0]
        start_pos.add(JobPart(job, 0, val_s[0], val_s[1]))
        goal_pos.add(JobPart(job, num_machines,  -1, 0, False))
        job += 1


    result_path, result_time, execution_time = a_star_fast(table, start_pos, goal_pos, num_machines)

    if type(result_path) != str:
        print("Result:  ")
        print(path_to_string(result_path), result_time)
        print("runn_time: ", execution_time)
    else:
        print(result_path)

    



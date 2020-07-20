import copy
import random
import sys
from itertools import groupby
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time


class JobShopProblem:

    def __init__(self, jobs: list):
        # list of jobs (which are lists of operations):
        # [
        #     [(0,0,2,4),(0,1,2,1),(0,2,0,5),(0,3,1,4)...],
        #     [(1,0,3,5),(1,1,0,3),(1,2,0,7)...],
        #     [(2,0,1,2),(2,1,3,5),(2,2,3,7),(2,3,1,5)...],
        # ]
        # an operation is a 4 tuple (job, operation, machine, time_steps)
        self.jobs = jobs
        self.num_jobs = len(jobs)
        self.num_ops = len(jobs[0])

    @staticmethod
    def load(table: str):
        jobs = []
        job = 0
        lines = table.split("\n")
        for line in lines:
            jobs.append([])
            split_line = line.strip().split(" ")
            operation = 0
            for index in range(0, len(split_line), 2):
                machine = int(split_line[index])
                time_steps = int(split_line[index + 1])
                jobs[job].append((job, operation, machine, time_steps))
                operation += 1
            job += 1
        return JobShopProblem(jobs)


class Schedule:

    def __init__(self, schedule: list):
        # nested list similar to the JobShopProblem jobs list
        # but: list of lists (machines) of operations
        self.schedule = schedule
        self.jobs = {}
        self._update_jobs()

    def _update_jobs(self):
        self.jobs = {}
        for machine in self.schedule:
            for operation_tuple in machine:
                job = operation_tuple[0]
                if job is not None:
                    if job not in self.jobs.keys():
                        self.jobs[job] = []
                    self.jobs[job].append(operation_tuple)
        for job in self.jobs:
            job_list = self.jobs[job]
            job_list.sort(key=lambda x: x[1])

    @staticmethod
    def create_from_problem(problem: JobShopProblem):
        jobs = copy.copy(problem.jobs)
        machine_amount = max(max(machine for (_, _, machine, _) in job) for job in jobs)
        instance = Schedule([[] for x in range(machine_amount+1)])
        while jobs:
            for job in jobs:
                operation_tuple = job.pop(0)
                job, operation, machine, time_steps = operation_tuple
                if operation == 0:
                    if instance.schedule[machine] is None:
                        instance.schedule[machine] = []
                    instance.schedule[machine].append(operation_tuple)
                else:
                    instance._update_jobs()
                    last_operation_end = instance._get_operation_end(job, operation - 1)
                    machine_end = instance._get_machine_duration(machine)
                    offset = last_operation_end - machine_end
                    if offset > 0:
                        instance.schedule[machine].append([None, None, machine, offset])
                    instance.schedule[machine].append(operation_tuple)
            jobs = [job for job in jobs if job != []]
        instance._update_jobs()
        return instance


    def _get_operations_at_timestamp(self, timestamp: int):
        operations = []
        for machine in self.schedule:
            current_operation = None
            time = 0
            for operation in machine:
                time += operation[3]
                if time >= timestamp:
                    current_operation = operation
                    break
            if current_operation is not None:
                operations.append(current_operation)
        return operations

    def _get_operation_end(self, target_job: int, target_operation: int):
        machine_index = self.jobs[target_job][target_operation][2]
        machine = self.schedule[machine_index]
        time = 0
        for operation in machine:
            job, operation, _, time_steps = operation
            time += time_steps
            if job == target_job and operation == target_operation:
                return time
        print(target_job, target_operation)
        return None
    

    def _get_machine_duration(self, machine):
        if isinstance(machine, int):
            machine = self.schedule[machine]
        time = 0
        for operation in machine:
            time_steps = operation[3]
            time += time_steps
        return time

    def get_length(self):
        length = 0
        for machine in self.schedule:
            machine_duration = self._get_machine_duration(machine)
            if machine_duration > length:
                length = machine_duration
        return length

    def is_valid(self):
        current_operations = {}
        for time_stamp in range(self.get_length()):
            operations = self._get_operations_at_timestamp(time_stamp)
            seen_jobs = []
            for operation_tuple in operations:
                job, operation, machine, time_steps = operation_tuple
                if job is None:
                    continue
                if job in seen_jobs:
                    return False
                seen_jobs.append(job)
                if job not in current_operations.keys():
                    current_operations[job] = 0
                if current_operations[job] == operation:
                    continue
                elif current_operations[job] + 1 == operation:
                    current_operations[job] += 1
                else:
                    return False
        return True

    # add space in front of operation
    def _offset_operation(self, operation_tuple, offset):
        job, operation, machine, time_steps = operation_tuple
        machine_list = self.schedule[machine]
        operation_index = machine_list.index(operation_tuple)
        previous_op_of_machine_index = operation_index - 1
        previous_op_of_machine = None
        if previous_op_of_machine_index >= 0:
            previous_op_of_machine = machine_list[previous_op_of_machine_index]
        # add space in front
        if previous_op_of_machine is None:
            # (operation is the first in the machine (no previous operation))
            machine_list.insert(0, [None, None, machine, offset])
        else:
            if previous_op_of_machine[0] is None:
                # if previous operation is also a space, just increase it by the offset
                previous_op_of_machine[3] += offset
            else:
                # insert new space
                machine_list.insert(operation_index, [None, None, machine, offset])
        # reduce succeeding spaces by offset
        index = machine_list.index(operation_tuple) + 1
        while index < len(machine_list) and offset > 0:
            operation = machine_list[index]
            if operation[0] is None:
                old_space_size = operation[3]
                operation[3] -= offset
                if operation[3] <= 0:
                    machine_list.remove(operation)
                    index -= 1
                offset -= old_space_size
            index += 1


    # semi deep copy (references to jobs are kept) and remove idle spaces
    def _copy_schedule_and_compress(self):
        new_schedule = []
        for machine in self.schedule:
            new_machine = []
            for operation in machine:
                if operation[0] is not None:
                    new_machine.append(operation)
            new_schedule.append(new_machine)
        return new_schedule

    
    def _combine_empty_spaces(self, machine_num):
            machine = self.schedule[machine_num]
            for op_index, op in enumerate(machine):
                if op_index < len(machine) - 1:
                    next_op = machine[op_index + 1]
                    if op[0] == None and next_op[0] == None:
                        j, o, m, t = op
                        n_j, n_o, n_m, n_t = next_op
                        op = (None, None, machine_num, n_t + t)
                        machine[op_index] = op
                        machine.pop(op_index + 1)
                        self.schedule[machine_num] = machine
    

    def m_minimize_empty_spaces(self, machine_num):
         machine = self.schedule[machine_num]
         for op_index, op in enumerate(machine):
             if op_index < len(machine) and op_index > 0:
                 prev_op = machine[op_index - 1]
                 if op[0] != None and prev_op[0] == None:
                     j, o, m, t = op
                     p_j, p_o, p_m, p_t =  prev_op
                     if o > 0: 
                        op_begin = self._get_operation_begin(machine_num, j, o)
                        p_op_end = self._get_operation_end(j, o - 1)
                        delta = op_begin - p_op_end
                        if delta > 0:
                            if delta >= p_t:
                                 machine.pop(op_index - 1)
                            else:       
                                machine[op_index - 1] = (p_j, p_o, p_m, p_t - delta)


    def _get_operation_begin(self, machine_num, target_job, target_op):
        result = 0
        for op in self.schedule[machine_num]:
            if op[0] == target_job and op[1] == target_op:
                return result
            else:
                result += op[3]
        return "Error: target_op not in schedule"   


    def print_schedule(self):
        for machine in self.schedule:
           print(machine)          


    def _manuel_schedule(self, schedule):
        self.schedule = schedule


    def decompress(self):
        while not self.is_valid():         
            for machine_num, machine_schedule in enumerate(self.schedule):
                for op_index, operation in enumerate(machine_schedule):
                    job, op, machine_num, time = operation
                    if op != 0 and op is not None:
                        pre_job_end = self._get_operation_end(job, op - 1)                        
                        if pre_job_end == None:
                            print("Error")
                        op_begin = self._get_operation_begin(machine_num, job, op)                                          
                        offset = pre_job_end - op_begin
                        if offset > 0:
                            if op_index < len(machine_schedule)  - 1:
                                next_op = machine_schedule[op_index + 1]
                                n_job, n_op, n_m, n_t = next_op
                                if n_job == None:
                                    if n_t - offset <= 0:
                                        self.schedule[machine_num].pop(op_index + 1)
                                    else:
                                        machine_schedule[op_index + 1] = (None, None, machine_num, n_t - offset)
                            blank_op = (None, None, machine_num, offset)        
                            self.schedule[machine_num].insert(op_index, blank_op)                         
                            self._combine_empty_spaces(machine_num)
                            self.m_minimize_empty_spaces(machine_num)
                              

    def get_sequenze(self, sched: list, num_op: int, num_machines: int):
        sequenze = []
        
        for op in range(num_op):
            for machine in range(num_machines):
                sequenze.append(sched[machine][op][0])
        return sequenze

    
    def sequenze_to_schedule(self, sequenz: list, machine_num: int):
        sched = [[] for m in range(machine_num)]
        job_operation = [0 for i in range(len(self.jobs))]

        for op in sequenz:
            job_op = (op, job_operation[op])
            job_operation[op] += 1
            operation_tuble  = self.jobs[job_op[0]][job_op[1]]
            sched[operation_tuble[2]].append(operation_tuble)

        return sched
    

    def sequenz_to_string(self, sequenz):
        return str(sequenz)
    

    def random_neighbour_generator(self):
        compressd_schedule = self._copy_schedule_and_compress()
        num_op = len(compressd_schedule[0])
        num_m = len(compressd_schedule)
        visited_neighbours_sequenzes = set()
        visited_neighbours = set()
        visited_neighbours.add(Schedule(compressd_schedule).to_string())
        sequenz = self.get_sequenze(compressd_schedule, num_op, num_m)
        sequenz_index = [x for x in range(len(sequenz))]
        while sequenz_index:
            rand_index  =  random.randrange(len(sequenz_index))
            op_index_one = sequenz_index.pop(rand_index)
            possible_partners = [i for i in sequenz_index if sequenz[i] != sequenz[op_index_one]]
            while possible_partners:
                neighbour_sequenz = copy.deepcopy(sequenz)
                rand_index = random.randrange(len(possible_partners))
                op_index_two = possible_partners.pop(rand_index)
                neighbour_sequenz[op_index_one], neighbour_sequenz[op_index_two] = neighbour_sequenz[op_index_two], neighbour_sequenz[op_index_one]
                if self.sequenz_to_string(neighbour_sequenz) not in visited_neighbours_sequenzes:
                    visited_neighbours_sequenzes.add(self.sequenz_to_string(neighbour_sequenz))
                    neighbour_schedule = self.sequenze_to_schedule(neighbour_sequenz, num_m)
                    neighbour = Schedule(neighbour_schedule)
                    if neighbour.to_string() not in visited_neighbours:
                        visited_neighbours.add(neighbour.to_string())
                        neighbour.decompress()
                        yield neighbour
        yield None
    
    

    def random_neighbour_generator_three(self):
        compressd_schedule = self._copy_schedule_and_compress()
        num_op = len(compressd_schedule)
        num_m = len(compressd_schedule)
        
        sequenz = self.get_sequenze(compressd_schedule, num_op, num_m)
        for i in range(len(sequenz)):
            neighbour = copy.deepcopy(sequenz)
            swap_idx = random.randrange(len(sequenz))
            neighbour[i], neighbour[swap_idx] = neighbour[swap_idx], neighbour[i]
            neighbour_schedule = self.sequenze_to_schedule(neighbour, num_m)
            schedule = Schedule(neighbour_schedule)
            schedule.decompress()
            yield schedule
        yield None



    def visualize(self, with_labels=True):
        ax = plt.gca()
        ax.yaxis.grid()
        ax.set_xlim(0, self.get_length())
        ax.set_xlabel('time')
        ax.set_ylim(0, len(self.schedule))
        ax.set_ylabel('machines')
        cmap = plt.cm.get_cmap(name='tab20')
        for y in range(len(self.schedule)):
            x = 0
            for operation_tuple in self.schedule[y]:
                job, operation, machine, time_steps = operation_tuple
                if job is None:
                    color = 'white'
                else:
                    color = cmap(job)
                rectangle = patches.Rectangle((x, y), time_steps, 1, color=color)
                if with_labels and operation is not None:
                    plt.text(x+(time_steps / 2), y + 0.5, str(job) + ":" + str(operation), ha='center', va='center')
                ax.add_patch(rectangle)
                x += time_steps


    def copy(self):
        return Schedule(self.schedule)
    

    def to_string(self):
        return "-".join([str(x) for x in self.schedule])



import copy
import random
import sys
from itertools import groupby
import matplotlib.pyplot as plt
import matplotlib.patches as patches


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

    @staticmethod
    def load_from_file(file_path: str):
        jobs = []
        with open(file_path, 'r') as file:
            job = 0
            for line in file:
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

    def _is_cyclic(self):
        checked_operations = []
        for machine in self.schedule:
            for operation_tuple in machine:
                if operation_tuple not in checked_operations and operation_tuple[0] is not None:
                    is_cyclic, seen_operations = self._is_cyclic_recursion(operation_tuple, [])
                    if is_cyclic:
                        return True
                    checked_operations += seen_operations
        return False

    def _is_cyclic_recursion(self, operation_tuple, seen_operations):
        seen_operations = set(copy.copy(seen_operations))
        seen_operations.add(operation_tuple)
        job, operation, machine, time_steps = operation_tuple
        dependencies = []
        # previous operation in machine
        machine_list = self.schedule[machine]
        machine_index = machine_list.index(operation_tuple)
        for index in reversed(range(machine_index)):
            current_operation = machine_list[index]
            if current_operation[0] is not None:
                dependencies.append(current_operation)
                break
        # previous operation in job
        if operation != 0:
            dependencies.append(self.jobs[job][operation-1])

        for dependency in dependencies:
            if dependency in seen_operations:
                return True, seen_operations
            else:
                is_cyclic, seen_operations_new = self._is_cyclic_recursion(dependency, seen_operations)
                seen_operations.union(seen_operations_new)
                if is_cyclic:
                    return True, seen_operations
        return False, seen_operations

    def _add_idle_spaces(self):
        time_stamp = 0
        # operations (list) contains all operations at the current time stamp
        operations = self._get_operations_at_timestamp(time_stamp)
        # increment time stamp continuously
        while operations:
            # group operations by jobs (each group contains all operations belonging to one job)
            groups = groupby(operations, lambda x: x[0])
            for key, group in groups:
                group = list(group)
                # if group is not group of spaces
                if group[0][0] is not None:
                    group.sort(key=lambda x: x[1])
                    # do for earliest operation in that group
                    earliest_operation = group.pop(0)
                    job, operation, machine, time_steps = earliest_operation
                    jobs_previous_op_end = 0
                    # add offset to previous operation in job if necessary
                    if operation != 0:
                        jobs_previous_op_end = self._get_operation_end(job, operation-1)
                        operation_start = self._get_operation_end(job, operation) - time_steps
                        offset = jobs_previous_op_end - operation_start
                        if offset > 0:
                            self._offset_operation(earliest_operation, offset)
                    last_operation_end = jobs_previous_op_end + time_steps
                    # add offset for next operations in job if required
                    for current_operation in range(operation + 1, len(self.jobs[job])):
                        current_operation_tuple = self.jobs[job][current_operation]
                        time_steps = current_operation_tuple[3]
                        current_operation_start = self._get_operation_end(job, current_operation) - time_steps
                        offset = last_operation_end - current_operation_start
                        if offset > 0:
                            self._offset_operation(current_operation_tuple, offset)
            time_stamp += 1
            operations = self._get_operations_at_timestamp(time_stamp)

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

    # calculates whole neighbourhood (would not recommend using it as it takes forever)
    def get_neighbourhood(self):
        neighbourhood = []
        schedule_compressed = self._copy_schedule_and_compress()
        # generate neighbourhood by switching every valid pair of operations
        for machine_index in range(len(schedule_compressed)):
            machine = schedule_compressed[machine_index]
            for operation1_index in range(len(machine)):
                operation1 = machine[operation1_index]
                if operation1[0] is not None:
                    for operation2_index in range(operation1_index+1, len(machine)):
                        operation2 = machine[operation2_index]
                        # if valid pair of operations (no idle spaces and do not belong to the same job) is found
                        if operation2[0] is not None and operation1[0] != operation2[0]:
                            new_schedule = self._copy_schedule_and_compress()
                            # switch operations in new schedule
                            new_machine = new_schedule[machine_index]
                            new_machine[operation1_index] = operation2
                            new_machine[operation2_index] = operation1
                            new_schedule = Schedule(new_schedule)
                            # add spaces and make schedule valid if schedule is not cyclic
                            if not new_schedule._is_cyclic():
                                new_schedule._add_idle_spaces()
                                neighbourhood.append(new_schedule)
                                sys.stdout.write('\rGenerated {0} neighbours'.format(len(neighbourhood)))
                                sys.stdout.flush()
        return neighbourhood

    
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


    def _decompress_two(self):
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
                              

    def _random_neighbour_generator_two(self):
        compressed_schedule = self._copy_schedule_and_compress()
        schedule_index = [x for x in range(len(compressed_schedule))]
        while schedule_index:
            machine_number = random.randint(0, len(schedule_index) - 1)
            machine_schedule_index = schedule_index.pop(machine_number)
            machine_schedule = compressed_schedule[machine_schedule_index]
            operations = [x for x in range(len(machine_schedule))]
            while operations:
                rand_op = random.randint(0, len(operations) - 1)               
                operation_index  = operations.pop(rand_op)
                operation_one = machine_schedule[operation_index]
                for operation_two_index in operations:
                    operation_two = machine_schedule[operation_two_index]
                    if operation_one[0] != operation_two[0]:
                        new_schedule = Schedule(self.schedule)._copy_schedule_and_compress()
                        new_machine = new_schedule[machine_schedule_index]
                        if new_machine != machine_schedule:
                            print("Error", new_machine)
                            exit()
                        new_machine[operation_index] = operation_two
                        new_machine[operation_two_index] = operation_one
                        neighbour = Schedule(new_schedule)
                        if not neighbour._is_cyclic():
                            neighbour._add_idle_spaces()
                            if neighbour.is_valid():
                                yield neighbour
        yield None
        

    def _random_neighbour_generator(self):
        compressed_schedule = self._copy_schedule_and_compress()
        schedule_index = [x for x in range(len(compressed_schedule))]
        while schedule_index:
            machine_number = random.randint(0, len(schedule_index) - 1)
            print(machine_number)
            machine_schedule_index = schedule_index.pop(machine_number)
            machine_schedule = compressed_schedule[machine_schedule_index]
            operations = [x for x in range(len(machine_schedule))]
            while operations:
                rand_op = random.randint(0, len(operations) - 1)
                print("r. ", rand_op)
                operation_index  = operations.pop(rand_op)
                operation_one = machine_schedule[operation_index]
                for operation_two_index in operations:
                    operation_two = machine_schedule[operation_two_index]
                    if operation_one[0] != operation_two[0]:
                        new_schedule = Schedule(self.schedule)._copy_schedule_and_compress()
                        new_machine = new_schedule[machine_schedule_index]
                        if new_machine != machine_schedule:
                            print("Error", new_machine)                           
                            exit()
                        new_machine[operation_index] = operation_two
                        new_machine[operation_two_index] = operation_one
                        neighbour = Schedule(new_schedule)
                        if not neighbour._is_cyclic():
                            neighbour._decompress_two()
                            yield neighbour
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
                    plt.text(x+(time_steps / 2), y + 0.5, str(operation), ha='center', va='center')
                ax.add_patch(rectangle)
                x += time_steps


    def copy(self):
        return Schedule(self.schedule)


if __name__ == '__main__':
    problem = JobShopProblem.load_from_file("data/4x4")
    initial_schedule = Schedule.create_from_problem(problem)
    """
    neighbourhood = initial_schedule.get_neighbourhood()
    non_valid_neighbours = []
    for neighbour in neighbourhood:
        if not neighbour.is_valid():
            non_valid_neighbours.append(neighbour)
    # visualization
    # initial schedule
    fig = plt.figure()
    fig.add_subplot(1, 1, 1)
    initial_schedule.visualize()
    plt.show()
    # some random neighbours
    fig = plt.figure(figsize=(10, 8))
    neighbourhood_sample = random.sample(neighbourhood, 9)
    for neighbour_index in range(len(neighbourhood_sample)):
        neighbour = neighbourhood_sample[neighbour_index]
        fig.add_subplot(3, 3, neighbour_index+1)
        neighbour.visualize(with_labels=True)
    plt.show()
    """
    """
    # some non valid neighbours
    fig = plt.figure(figsize=(10, 8))
    neighbourhood_sample = random.sample(non_valid_neighbours, 9)
    for neighbour_index in range(len(neighbourhood_sample)):
        neighbour = non_valid_neighbours[neighbour_index]
        fig.add_subplot(3, 3, neighbour_index+1)
        neighbour.visualize(with_labels=True)
    plt.show()
    """


    sch = []
    sch.append([(2, 0, 0, 6), (0, 0, 0, 4), (1, 2, 0, 4), (3, 2, 0, 4)])
    sch.append([(2, 2, 1, 3), (0, 1, 1, 3), (1, 3, 1, 6), (3, 3, 1, 5)])
    sch.append([(1, 0, 2, 4), (2, 1, 2, 3), (3, 1, 2, 3), (0, 2, 2, 5)])
    sch.append([(3, 0, 3, 6), (1, 1, 3, 5), (2, 3, 3, 6), (0, 3, 3, 6)])
    initial_schedule._manuel_schedule(sch)
    fig = plt.figure()
    fig.add_subplot(1, 1, 1)   
    initial_schedule.visualize()
    plt.show()
    print(initial_schedule.get_length())
    fig = plt.figure()
    fig.add_subplot(1, 1, 1)
    test_s = Schedule(initial_schedule._copy_schedule_and_compress())
    test_s.visualize()
    plt.show()
    print("here")
    fig = plt.figure()
    fig.add_subplot(1, 1, 1)
    test_s._decompress_two()
    test_s.print_schedule()
    test_s.visualize()
    plt.show()
    print(test_s.get_length())
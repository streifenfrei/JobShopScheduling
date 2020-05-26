import copy
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
                    last_operation_end = instance._get_operation_end(job, operation - 1)
                    machine_end = instance._get_machine_duration(machine)
                    offset = last_operation_end - machine_end
                    if offset > 0:
                        instance.schedule[machine].append([None, None, machine, offset])
                    instance.schedule[machine].append(operation_tuple)
            jobs = [job for job in jobs if job != []]
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
        for machine in self.schedule:
            time = 0
            for operation in machine:
                job, operation, _, time_steps = operation
                time += time_steps
                if job == target_job and operation == target_operation:
                    return time
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

    def _add_idle_spaces(self):
        if self.is_valid():
            return
        time_stamp = 0
        # operations (list) contains all operations at the current time stamp
        last_operations = []
        operations = self._get_operations_at_timestamp(time_stamp)
        while operations:
            # group operations by jobs
            groups = groupby(operations, lambda x: x[0])
            for key, group in groups:
                group = list(group)
                # if there are multiple operations belonging to the same job: add space accordingly
                if (len(group)) != 1 and group[0][0] is not None:
                    # sort operations by operation_id
                    group.sort(key=lambda x: x[1])
                    group.pop(0)
                    # add space to every operation, so they are not parallel
                    for operation_tuple in group:
                        job, operation, machine, time_steps = operation_tuple
                        previous_op_of_job_end = self._get_operation_end(job, operation-1)
                        # offset to last operation of that job
                        offset = previous_op_of_job_end - time_stamp
                        previous_op_of_machine = next((x for x in last_operations if x[2] == machine), None)
                        machine_list = self.schedule[machine]
                        # add space in front
                        if previous_op_of_machine is None:
                            # (operation is the first in the machine (no previous operation))
                            machine_list.insert(0, (None, None, machine, offset))
                        else:
                            if previous_op_of_machine[0] is None:
                                # if previous operation is also a space, just increase it by the offset
                                previous_op_of_machine[3] += offset
                            else:
                                # insert new space
                                index = machine_list.index(operation_tuple)
                                machine_list.insert(index, [None, None, machine, offset])
            last_operations = operations
            operations = self._get_operations_at_timestamp(time_stamp)
            time_stamp += 1

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
                            # add spaces and make schedule valid
                            new_schedule._add_idle_spaces()
                            neighbourhood.append(new_schedule)
        return neighbourhood

    def visualize(self):
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
                ax.add_patch(rectangle)
                x += time_steps


if __name__ == '__main__':
    problem = JobShopProblem.load_from_file("data/abz5")
    initial_schedule = Schedule.create_from_problem(problem)
    neighbourhood = initial_schedule.get_neighbourhood()

    # visualization
    # initial schedule
    fig = plt.figure()
    fig.add_subplot(1, 1, 1)
    initial_schedule.visualize()
    plt.show()
    # first 4 neighbours
    fig = plt.figure()
    for neighbour_index in range(len(neighbourhood[:4])):
        neighbour = neighbourhood[neighbour_index]
        fig.add_subplot(2, 2, neighbour_index+1)
        neighbour.visualize()
    plt.show()


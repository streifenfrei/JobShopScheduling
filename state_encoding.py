import copy


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
                    last_operation_end = instance.get_operation_end(job, operation - 1)
                    machine_end = instance.get_machine_duration(machine)
                    offset = last_operation_end - machine_end
                    if offset > 0:
                        instance.schedule[machine].append((None, None, machine, offset))
                    instance.schedule[machine].append(operation_tuple)
            jobs = [job for job in jobs if job != []]
        return instance

    def get_jobs_at_timestamp(self, timestamp: int):
        jobs = []
        for machine in self.schedule:
            current_job = None
            time = 0
            for operation in machine:
                job, _, _, time_steps = operation
                time += time_steps
                if time >= timestamp:
                    current_job = job
                    break
            jobs.append(current_job)

    def get_operation_end(self, target_job, target_operation):
        for machine in self.schedule:
            time = 0
            for operation in machine:
                job, operation, _, time_steps = operation
                time += time_steps
                if job == target_job and operation == target_operation:
                    return time
        return None

    def get_machine_duration(self, machine):
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
            machine_duration = self.get_machine_duration(machine)
            if machine_duration > length:
                length = machine_duration
        return length

    def get_neighbourhood(self):
        # TODO neighbourhood
        return


if __name__ == '__main__':
    problem = JobShopProblem.load_from_file("data/abz5")
    initial_schedule = Schedule.create_from_problem(problem)
    print(initial_schedule.get_length())

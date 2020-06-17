class Machine:

    def __init__(self, machine_num: int, job: int, job_instance: int, time: int, active: False):
        self.machine_num = machine_num
        self.job = job
        self.job_instance = job_instance
        self.time = time
        self.active = active


class State:

    def __init__(self, machines: set, done_job_instaces: dict):
        self.machines = dict()
        self.done_job_instaces = done_job_instaces
        for machine in machines:
            self.machines[machine.machine_num] = machine
    

    def is_job_instance_done(self, job_num, num_intance):
        if self.done_job_instaces[job_num] == num_intance:
            return True
        else:
            return False


def power_set(ps):
    result = [[]]
    for val in ps:
        new_subset = [subset + [val] for subset in result]
        result.extend(new_subset)
    result.remove([])
    return result


def get_neighbours(current_state)
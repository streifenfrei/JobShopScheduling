class JobPart:

    def __init__(self, job, instance, machine, time, active=False):
        self.job = job
        self.instance = instance
        self.machine = machine
        self.time = time
        self.active = active
    

    def compare_to(self, state):
        if (self.instance == state.instance) and (self.job == state.job):
            if (self.machine == state.machine) and (self.time == state.time) and (self.active == state.active):               
                return True
            else:               
                return False                
        else:         
            return False


class State:

    def __init__(self, job_parts: list):
        self.job_parts = job_parts
    



def power_set(ps):
    result = [[]]
    for val in ps:
        new_subset = [subset + [val] for subset in result]
        result.extend(new_subset)
    result.remove([])
    return result


def is_valid(state: State):


def get_neighbours(current_state)
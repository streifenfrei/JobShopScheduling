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



import a_star as a


def read_table(path):
    with open(path, "r") as table:
        time_table = list()
        
        for line in table:
            job = line.strip().split(" ")
            job_plan = list()
            for instance in range(0, len(job), 2):
                job_plan.append((int(job[instance]), int(job[instance + 1])))
            time_table.append(job_plan)
    return time_table, len(time_table), len(time_table[0])


def main():
    table, num_jobs, num_machines = read_table("data/5x4")
    print(table)
    print("\n\n")
    a.a_star_main(table, num_machines, num_jobs)
    



if __name__ == "__main__":
    main()
    exit()
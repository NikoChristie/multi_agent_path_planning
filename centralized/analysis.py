import yaml
import os
import subprocess
import time

output_file = "output.csv"

KEYS = [
    'Map Name',
    'Density %',
    'Agent #',
    'CBS Sum Of Cost',
    'SIPP Sum Of Cost',
    'CBS Makespan',
    'SIPP Makespan',
    'CBS Time',
    'SIPP Time',
]

path = ".\\benchmark\\8x8_obst12\\"

def get_agents(solution):
    return list(solution['schedule'].keys())

def get_agents_count(solution):
    return len(get_agents(solution))

def get_sum_of_cost(solution):
    agents = get_agents(solution)

    costs = list(map(lambda agent : len(solution['schedule'][agent]), agents))
    return sum(costs)

def get_makespan(solution):
    agents = get_agents(solution)

    costs = list(map(lambda agent : len(solution['schedule'][agent]), agents))
    return max(costs)

def get_time(solution):
    return solution['time']

def get_map_size(problem):
    dimensions = problem['map']['dimensions']
    size = dimensions[0] * dimensions[1]
    return size

def get_map_obstacles_count(problem):
    obstacles = problem['map']['obstacles']
    return len(obstacles)

def get_map_density_percent(problem):
    density = (get_map_obstacles_count(problem) / get_map_size(problem)) * 100
    return round(density, 2)

def analyze_solution(output):

    analysis = {
        'Agent #': 0,
        'Sum Of Cost': 0,
        'Makespan': 0,
        'Time': 0,
    }

    # Output File
    with open(output, 'r') as file:
        solution = yaml.safe_load(file)
        analysis['Agent #'] = get_agents_count(solution)
        analysis['Sum Of Cost'] = get_sum_of_cost(solution)
        analysis['Makespan'] = get_makespan(solution)
        analysis['Time'] = get_time(solution)

    return analysis

def run_cbs(input):
    print("running cbs", flush=True)
    subprocess.call(f"python ./cbs/cbs.py {input} cbs_output.yaml", timeout=15)
    return analyze_solution("cbs_output.yaml")

def run_sipp(input):
    print("running sipp", flush=True)
    subprocess.call(f"python ./sipp/multi_sipp.py {input} sipp_output.yaml", timeout=15)
    return analyze_solution("sipp_output.yaml")

def combine_solutions(input, x, y):
    
    if x['Agent #'] != y['Agent #']:
        return None

    analysis = {
        'Map Name': None,
        'Density %': 0,
        'Agent #': 0,
        'CBS Sum Of Cost': 0,
        'CBS Makespan': 0,
        'CBS Time': 0,
        'SIPP Sum Of Cost': 0,
        'SIPP Makespan': 0,
        'SIPP Time': 0,
    }


    with open(input, 'r') as f:
        problem = yaml.load(f, Loader=yaml.FullLoader)
        analysis['Density %'] = get_map_density_percent(problem)
        analysis['Map Name'] = input
        analysis['Agent #'] = x['Agent #']

    analysis['CBS Sum Of Cost'] = x['Sum Of Cost']
    analysis['CBS Makespan'] = x['Makespan']
    analysis['CBS Time'] = x['Time']

    analysis['SIPP Sum Of Cost'] = y['Sum Of Cost']
    analysis['SIPP Makespan'] = y['Makespan']
    analysis['SIPP Time'] = y['Time']

    return analysis

# Start Analysis

with open(output_file, 'w') as f:
    f.write(','.join(KEYS) + '\n')

for map_file in os.listdir(path):

    input_file = path + map_file
    '''
    f = open(input_file, "r")
    problem = yaml.load(f, Loader=yaml.FullLoader)
    f.close()

    if len(problem['agents']) == 4:
    '''
    print(input_file)

    try:
        cbs  = run_cbs(input_file)
        sipp = run_sipp(input_file)
    except subprocess.TimeoutExpired:
        continue

    solution = combine_solutions(input_file, cbs, sipp)

    if solution != None:
        with open(output_file, 'a') as f:
            output = map(lambda x: str(solution[x]), KEYS)

            f.write(','.join(output) + '\n')
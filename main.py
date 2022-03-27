from datetime import datetime
import multiprocessing as mp
from re import sub
import subprocess
import cpuinfo


def get_cpu_data():
    cores = mp.cpu_count()
    return cores


def math_single_core_test(vals):

    if len(vals) != 2:
        raise ValueError("Wrong number of arguments.")

    if 0 in vals:
        raise ValueError("Argument is equal 0.")

    for i in range(2):
        typeof = type(vals[i])
        if typeof is not int:
            raise AttributeError('Argument is not int type.')

    ## 1 - get control value
    control_value = vals[0] ** vals[1]

    #  2 - Get starting time
    t0 = datetime.now()
    
    #  3 - Iterate through calculation and check is result correct
    for _ in range(small_iteration):
        value = vals[0] ** vals[1]
        if value != control_value:
            raise ValueError("Single Core - CPU returned incorrect score.")

    #  4 - Get finish time
    t1 = datetime.now()

    #  5 - Calc difference in seconds 
    delta = t1 - t0
    delta = delta.total_seconds()

    #  6 - Return score
    print(f"Single Core - Calculation done in: {delta}s.")
    return delta


def math_big_number_test(vals):
    if len(vals) != 2:
        raise ValueError("Wrong number of arguments.")

    if 0 in vals:
        raise ValueError("Argument is equal 0.")

    for i in range(2):
        typeof = type(vals[i])
        if typeof is not int:
            raise AttributeError('Argument is not int type.')

    ## 1 - get control value
    control_value = vals[0] ** vals[1]

    #  2 - Get starting time
    t0 = datetime.now()
    
    #  3 - Iterate through calculation and check is result correct
    for _ in range(big_iteration):
        value = vals[0] ** vals[1]
        if value != control_value:
            raise ValueError("Single Core BIG value - CPU returned incorrect score.")

    #  4 - Get finish time
    t1 = datetime.now()

    #  5 - Calc difference in seconds 
    delta = t1 - t0
    delta = delta.total_seconds()

    #  6 - Return score
    print(f"Single Core BIG value - Calculation done in: {delta}s.")
    return delta


def math_all_core_test(vals, cores):

    ## Control value
    global control_value
    control_value = vals[0] ** vals[1]

    ## Func need to be global, cuz pickle will raise Atrribute Exception
    global calc
    def calc(x):
        value = x[0] ** x[1]
        if value != control_value:
            raise ValueError("All Core - CPU returned incorrect score.")

    ## Values from this list will be processed 
    input_list = []
    for _ in range(small_iteration):
        input_list.append(vals)

    ## Create pool for all cores
    pool = mp.Pool(cores)
    t0 = datetime.now()
    result = pool.map(func=calc, iterable=input_list)
    pool.close()
    pool.join()
    t1 = datetime.now()

    ## Score time
    delta = (t1 - t0).total_seconds()

    print(f"All Core - Calculation done in: {delta}s.")
    return delta


if __name__ == "__main__":
    small_iteration = 600
    big_iteration = 1
    standard_values = (2938475, 7221)
    big_values = (2938475, 721121)
    score_board = {
        'single_core': 0,
        'all_core': 0,
        'big_number_single_core': 0,
        'small_iteration': small_iteration,
        'big_iteration': big_iteration,
        'standard_values': standard_values,
        'big_values': big_values,
    }

    ## Device details
    device_info = cpuinfo.get_cpu_info()
    score_board['python_version'] = device_info['python_version']
    score_board['arch'] = device_info['arch']
    score_board['bits'] = device_info['bits']

    ## Get Raspberry version
    bashCommand = "cat /proc/device-tree/model"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    score_board['device'] = output.decode().rstrip('\x00')

    ## Not found on X86
    try:
        score_board['hardware_raw'] = device_info['hardware_raw']
    except Exception as e:
        pass

    score_board['brand_raw'] = device_info['brand_raw']
    score_board['hz_advertised_friendly'] = device_info['hz_advertised_friendly']
    score_board['hz_actual'] = round(device_info['hz_actual'][0] / 1000000000, 2)

    cores = get_cpu_data()
    print(f'Found {cores} logical CPU cores.')
    print('=' * 80)
    print('Starting math test.')

    single_core = round(math_single_core_test(standard_values), 2)
    big_number_single_core = round(math_big_number_test(big_values), 2)
    all_core = round(math_all_core_test(standard_values, cores), 2)

    score_board['single_core'] = single_core
    score_board['big_number_single_core'] = big_number_single_core
    score_board['all_core'] = all_core

    print('=' * 80)
    print ("{:<40} {:<40}".format('NAME', 'VALUE'))

    for item in score_board:
        print ("{:<40} {:<40}".format(item.upper(), str(score_board[item])))

    prompt = input('Save results? [Y/N]: ')
    if prompt.lower() == "y":
        with open('results.txt', 'w') as fp:
            for item in score_board:
                fp.write("{:<40} {:<40}\n".format(item.upper(), str(score_board[item])))
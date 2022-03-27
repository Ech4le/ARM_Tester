from datetime import datetime
import multiprocessing as mp


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
    for _ in range(1):
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
    cores = get_cpu_data()
    print(f'Found {cores} logical CPU cores.')
    print('Starting math test.')
    standard_values = (2938475, 32521)
    math_single_core_test(standard_values)
    # big_values = (2938475, 3251121)
    # math_big_number_test(big_values)
    math_all_core_test(standard_values, cores)
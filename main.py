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
    for _ in range(450):
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


if __name__ == "__main__":
    cores = get_cpu_data()
    print(f'Found {cores} logical CPU cores.')
    print('Starting math test.')
    standard_values = (2938475, 32521)
    math_single_core_test(standard_values)
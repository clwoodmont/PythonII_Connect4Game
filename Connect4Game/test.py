import time
import func_timeout


def my_function(n):
    """Sleep for n seconds and return n squared."""
    print(f'Processing {n}')
    time.sleep(n)
    return n**2


def main_controller(max_wait_time, all_data):
    """
    Feed my_function with a list of items to process (all_data).

    However, if max_wait_time is exceeded, return the item and a fail info.
    """
    res = []
    for data in all_data:
        try:
            my_square = func_timeout.func_timeout(
                max_wait_time, my_function, args=[data]
                )
            res.append((my_square, 'processed'))
        except func_timeout.FunctionTimedOut:
            print('error')
            res.append((data, 'fail'))
            continue

    return res


timeout_time = 2.1  # my time limit
all_data = range(1, 10)  # the data to be processed

res = main_controller(timeout_time, all_data)
print(res)
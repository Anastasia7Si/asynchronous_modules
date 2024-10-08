import multiprocessing


def do_calculation(data):
    return data * 2


def start_process():
    print('Starting', multiprocessing.current_process().name)


if __name__ == '__main__':
    inputs = list(range(10))
    print('Input    :', inputs)
    builtin_outputs = list(map(do_calculation, inputs))
    print('Buit-in  :', builtin_outputs)

    pool_size = multiprocessing.cpu_count() * 2
    pool = multiprocessing.Pool(
        processes=pool_size,
        initializer=start_process
        # maxtasksperchild=2 - ограничение кол-ва задач для процесса
    )
    pool_outputs = pool.map(do_calculation, inputs)
    pool.close()
    pool.join()
    print('Pool     :', pool_outputs)

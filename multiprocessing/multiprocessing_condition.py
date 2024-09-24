import multiprocessing
import time


def stage_1(condition):
    """Выполнить первый этап работы, а затем
    уведомить stage_2 для продолжения."""

    name = multiprocessing.current_process().name
    print('Starting: ', name)
    with condition:
        print(f'{name} done and ready for stage 2')
        condition.notify_all()


def stage_2(condition):
    """Дождаться услови, сообщающего, что stage_1 завершён."""

    name = multiprocessing.current_process().name
    print('Starting: ', name)
    with condition:
        condition.wait()
        print(f'{name} running')


if __name__ == '__main__':
    condition = multiprocessing.Condition()
    stg_1 = multiprocessing.Process(name='s1',
                                    target=stage_1,
                                    args=(condition,))
    stg_2_clients = [
        multiprocessing.Process(
            name='stage_2[{}]'.format(i),
            target=stage_2,
            args=(condition,)
            )
            for i in range(1, 3)
    ]

    for client in stg_2_clients:
        client.start()
        time.sleep(1)
    stg_1.start()

    stg_1.join()
    for client in stg_2_clients:
        client.join()

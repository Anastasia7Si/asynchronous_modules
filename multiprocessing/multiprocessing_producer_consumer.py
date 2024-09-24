import multiprocessing
import time


class Consumer(multiprocessing.Process):

    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
    
    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Прекращение выполнения с помощью "отравленной таблетки"
                print(f'{proc_name}: Exiting')
                self.task_queue.task_done()
                break
            print(f'{proc_name}: {next_task}')
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)


class Task:

    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def __call__(self):
        time.sleep(0.1)
        return '{self.a} * {self.b} = {product}'.format(
            self=self, product=self.a * self.b
        )
    
    def __str__(self):
        return '{self.a} * {self.b}'.format(self=self)


if __name__ == '__main__':
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    number_consumers = multiprocessing.cpu_count() * 2
    print(f'Creating {number_consumers} consumers')
    consumers = [
        Consumer(tasks, results)
        for i in range(number_consumers)
    ]
    for worker in consumers:
        worker.start()
    
    number_jobs = 10
    for i in range(number_jobs):
        tasks.put(Task(i, i))
    for i in range(number_consumers):
        tasks.put(None)
    tasks.join()
    while number_jobs:
        result = results.get()
        print('Result:', result)
        number_jobs -= 1

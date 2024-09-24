import multiprocessing


class Worker(multiprocessing.Process):

    def run(self):
        print(f'In {self.name}.')
        return


if __name__ == '__main__':
    jobs = []
    for i in range(5):
        process = Worker()
        jobs.append(process)
        process.start()
    for job in jobs:
        job.join()

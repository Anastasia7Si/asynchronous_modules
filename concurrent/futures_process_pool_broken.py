from concurrent import futures
import os
import signal


with futures.ProcessPoolExecutor(max_workers=2) as executor:
    print('getting the pid for one worker')
    func1 = executor.submit(os.getpid)
    pid1 = func1.result()

    print(f'killing process {pid1}')
    os.kill(pid1, signal.SIGHUP)

    print('submiting another task')
    func2 = executor.submit(os.getpid)
    try:
        pid2 = func2.result()
    except futures.process.BrokenProcessPool as e:
        print(f'could not start new tasks: {e}')

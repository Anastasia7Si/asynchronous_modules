import asyncio


async def phase(i):
    print(f'in phase {i}')
    try:
        await asyncio.sleep(0.1 * i)
    except asyncio.CancelledError:
        print(f'phase {i} canceled')
        raise
    else:
        print(f'done with phase {i}')
        return f'phase {i} result'


async def main(number_phases):
    print('starting main')
    phases = [
        asyncio.create_task(phase(i))
        for i in range(number_phases)
    ]
    print('waiting 0.1 for phases to complate')
    completed, pending = await asyncio.wait(phases, timeout=0.1)
    print(f'{len(completed)} and {len(pending)} pending')
    if pending:
        print('canceled tasks')
        for task in pending:
            task.cancel()
    print('exiting main')


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(3))
finally:
    event_loop.close()

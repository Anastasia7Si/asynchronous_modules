import asyncio


async def phase(i):
    print(f'in phase {i}')
    await asyncio.sleep(0.1 * i)
    print(f'done with phase {i}')
    return f'phase {i} result'


async def main(number_phases):
    print('starting main')
    phases = [
        asyncio.create_task(phase(i))
        for i in range(number_phases)
    ]
    print('waiting for phases to complete')
    completed, pending = await asyncio.wait(phases)
    results = [time.result() for time in completed]
    print('results: {!r}'.format(results))


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(3))
finally:
    event_loop.close()

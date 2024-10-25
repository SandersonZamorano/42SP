import time

def ft_progress(list):
    total = len(list)
    start_time = time.time()
    for i, elem in enumerate(list):
        percent = (i + 1) / total * 100
        elapsed_time = time.time() - start_time
        eta = elapsed_time / (i + 1) * (total - (i + 1))
        print(f'\r ETA: {eta:.2f}s [{percent:.0f}%][{("=" * int(percent // 2)).ljust(50)}] elapsed time: {elapsed_time:.2f}s', end='')
        yield elem  

a_list = range(1000)
ret = 0

for elem in ft_progress(a_list):
    ret += (elem + 3) % 5
    time.sleep(0.01)

print()
print(ret)
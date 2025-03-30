import multiprocessing
import threading
import time


def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

def run_fibonacci(n, results, idx=None):
    result = fibonacci(n)
    if idx is not None:
        results[idx] = result
    return result

def sync_execution(n, times):
    start_time = time.time()
    results = [0] * times
    
    for i in range(times):
        results[i] = run_fibonacci(n, None)
    
    end_time = time.time()
    return end_time - start_time

def threaded_execution(n, times):
    start_time = time.time()
    threads = []
    results = [0] * times
    
    for i in range(times):
        thread = threading.Thread(target=run_fibonacci, args=(n, results, i))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    return end_time - start_time

def process_execution(n, times):
    start_time = time.time()
    processes = []
    manager = multiprocessing.Manager()
    results = manager.list([0] * times)
    
    for i in range(times):
        process = multiprocessing.Process(target=run_fibonacci, args=(n, results, i))
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()
    
    end_time = time.time()
    return end_time - start_time

def main():
    n = 35  
    times = 10  
    
    print(f"Вычисление чисел Фибоначчи для n={n}, {times} раз")
    
    sync_time = sync_execution(n, times)
    print(f"Синхронное выполнение: {sync_time:.4f} секунд")
    
    threaded_time = threaded_execution(n, times)
    print(f"Многопоточное выполнение: {threaded_time:.4f} секунд")
    
    process_time = process_execution(n, times)
    print(f"Многопроцессное выполнение: {process_time:.4f} секунд")
    
    with open("artifacts/fibonacci_results.txt", "w") as f:
        f.write(f"Вычисление чисел Фибоначчи для n={n}, {times} раз\n")
        f.write(f"Синхронное выполнение: {sync_time:.4f} секунд\n")
        f.write(f"Многопоточное выполнение: {threaded_time:.4f} секунд\n")
        f.write(f"Многопроцессное выполнение: {process_time:.4f} секунд\n")

if __name__ == "__main__":
    main()

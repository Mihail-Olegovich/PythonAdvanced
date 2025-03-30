import concurrent.futures
import math
import multiprocessing
import time


def integrate(f, a, b, *, n_jobs=1, n_iter=10000000):
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


def partial_integrate(f, a, b, n_iter):
    """Вычисляет часть интеграла на отрезке [a, b] с n_iter итерациями."""
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


def parallel_integrate_threads(f, a, b, *, n_jobs=1, n_iter=10000000):
    """Интегрирование с использованием потоков (ThreadPoolExecutor)."""
    if n_jobs <= 1:
        return integrate(f, a, b, n_jobs=1, n_iter=n_iter)
    
    chunk_size = n_iter // n_jobs
    step = (b - a) / n_jobs
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=n_jobs) as executor:
        futures = []
        for i in range(n_jobs):
            start = a + i * step
            end = a + (i + 1) * step
            
            iter_count = chunk_size
            if i == n_jobs - 1:
                iter_count = n_iter - chunk_size * (n_jobs - 1)
                end = b 
            
            futures.append(executor.submit(partial_integrate, f, start, end, iter_count))
        
        results = [future.result() for future in futures]
        return sum(results)


def parallel_integrate_processes(f, a, b, *, n_jobs=1, n_iter=10000000):
    """Интегрирование с использованием процессов (ProcessPoolExecutor)."""
    if n_jobs <= 1:
        return integrate(f, a, b, n_jobs=1, n_iter=n_iter)
    
    chunk_size = n_iter // n_jobs
    step = (b - a) / n_jobs
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=n_jobs) as executor:
        futures = []
        for i in range(n_jobs):
            start = a + i * step
            end = a + (i + 1) * step
            
            iter_count = chunk_size
            if i == n_jobs - 1:
                iter_count = n_iter - chunk_size * (n_jobs - 1)
                end = b
            
            futures.append(executor.submit(partial_integrate, f, start, end, iter_count))
        
        results = [future.result() for future in futures]
        return sum(results)


def benchmark():
    """Сравнение производительности для разного количества потоков/процессов."""
    cpu_count = multiprocessing.cpu_count() 
    max_jobs = cpu_count * 2
    n_iter = 100000000  
    
    jobs_list = list(range(1, max_jobs + 1))
    thread_times = []
    process_times = []
    
    print(f"Сравнение времени интегрирования функции math.cos на отрезке [0, π/2]")
    print(f"Используется {n_iter} итераций и {cpu_count} ядер CPU")
    print("-" * 60)
    print("| n_jobs | ThreadPoolExecutor (с) | ProcessPoolExecutor (с) |")
    print("|--------|------------------------|--------------------------|")
    
    for n_jobs in jobs_list:
        start_time = time.time()
        result_thread = parallel_integrate_threads(math.cos, 0, math.pi / 2, n_jobs=n_jobs, n_iter=n_iter)
        thread_time = time.time() - start_time
        thread_times.append(thread_time)
        
        start_time = time.time()
        result_process = parallel_integrate_processes(math.cos, 0, math.pi / 2, n_jobs=n_jobs, n_iter=n_iter)
        process_time = time.time() - start_time
        process_times.append(process_time)
        
        print(f"| {n_jobs:6d} | {thread_time:22.4f} | {process_time:24.4f} |")
    
    exact_result = 1.0 
    
    print("-" * 60)
    print(f"Точное значение интеграла: {exact_result}")
    print(f"Рассчитанное значение (потоки): {result_thread:.10f}")
    print(f"Рассчитанное значение (процессы): {result_process:.10f}")
    
    with open("artifacts/integration_benchmark_results.txt", "w") as f:
        f.write(f"Сравнение времени интегрирования функции math.cos на отрезке [0, π/2]\n")
        f.write(f"Используется {n_iter} итераций и {cpu_count} ядер CPU\n\n")
        f.write("| n_jobs | ThreadPoolExecutor (с) | ProcessPoolExecutor (с) |\n")
        f.write("|--------|------------------------|------------------------|\n")
        
        for i, n_jobs in enumerate(jobs_list):
            f.write(f"| {n_jobs:6d} | {thread_times[i]:22.4f} | {process_times[i]:24.4f} |\n")
        
        f.write("\nТочное значение интеграла: 1.0\n")
        f.write(f"Рассчитанное значение (потоки): {result_thread:.10f}\n")
        f.write(f"Рассчитанное значение (процессы): {result_process:.10f}\n\n") 

if __name__ == "__main__":
    benchmark()

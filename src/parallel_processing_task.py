"""Задача - Параллельная обработка числовых данных"""

import csv
import multiprocessing
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor

sys.setrecursionlimit(1500)


def generate_data(n: int) -> list[int]:
    """
    Генерирует список случайных чисел от 1 до 1000.
    Переданный аргумент определяет размер списка
    """
    return [random.randint(1, 1000) for _ in range(n)]


def process_number(n: int) -> int:
    """Вычисляет факториал числа рекурсивным способом"""
    if n == 1:
        return n
    return n * process_number(n - 1)


def write_results(method: str, list_length: int, time: float):
    """Записывает время выполнения в CSV-файл"""
    data = {"method": method, "list_length": list_length, "time": time}

    with open("results.csv", "a", newline="") as file:
        writer = csv.DictWriter(
            file, fieldnames=["method", "list_length", "time"]
        )
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(data)


def thread_pool(list_length: int) -> None:
    """Замер времени выполнения для ThreadPoolExecutor"""
    numbers = generate_data(list_length)

    start = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_number, num) for num in numbers]
        for future in futures:
            future.result()
    end = time.time()

    write_results(
        method="ThreadPool",
        list_length=list_length,
        time=round((end - start), 3),
    )


def multiprocessing_pool(list_length: int) -> None:
    """Замер времени выполнения для multiprocessing.Pool"""
    numbers = generate_data(list_length)

    start = time.time()
    with multiprocessing.Pool(processes=8) as pool:
        results = pool.map(process_number, numbers)  # noqa
    end = time.time()

    write_results(
        method="MultiprocessingPool",
        list_length=list_length,
        time=round((end - start), 3),
    )


def worker(task_queue: multiprocessing.Queue):
    """Воркер для замера multiprocessing_process_queue()"""
    while True:
        task = task_queue.get()
        if task is None:
            break
        result = process_number(task) # noqa


def multiprocessing_process_queue(list_length: int) -> None:
    """
    Замер времени выполнения с использованием
    multiprocessing.Process и multiprocessing.Queue
    """
    numbers = generate_data(list_length)
    task_queue = multiprocessing.Queue()

    num_processes = 8
    processes = []

    for _ in range(num_processes):
        p = multiprocessing.Process(target=worker, args=(task_queue,))
        p.start()
        processes.append(p)

    start_time = time.time()

    for number in numbers:
        task_queue.put(number)

    for _ in range(num_processes):
        task_queue.put(None)

    for p in processes:
        p.join()

    end_time = time.time()

    write_results(
        method="ProcessQueue",
        list_length=list_length,
        time=round(end_time - start_time, 3),
    )


def single_thread(list_length: int) -> None:
    """Замер времени выполнения для однопоточного варианта"""
    numbers = generate_data(list_length)

    start_time = time.time()
    for num in numbers:
        process_number(num)
    end_time = time.time()

    write_results(
        method="SingleThread",
        list_length=list_length,
        time=round(end_time - start_time, 3),
    )


if __name__ == "__main__":
    thread_pool(list_length=10**5)
    multiprocessing_pool(list_length=10**5)
    multiprocessing_process_queue(list_length=10**5)
    single_thread(list_length=10**5)

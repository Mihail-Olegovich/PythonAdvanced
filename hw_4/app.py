import codecs
import datetime
import multiprocessing
import threading
import time


def process_a(input_queue, pipe_conn, exit_event):
    """
    Процесс A.
    Получает сообщения из input_queue, применяет .lower() и отправляет в процесс B.
    Отправляет сообщение не чаще, чем 1 раз в 5 секунд.
    """
    print(f"[{datetime.datetime.now()}] Процесс A запущен")
    
    while not exit_event.is_set():
        try:
            if not input_queue.empty():
                message = input_queue.get()
                
                if message == "EXIT":
                    print(f"[{datetime.datetime.now()}] Процесс A: получена команда выхода")
                    pipe_conn.send("EXIT")
                    break
                
                
                processed_message = message.lower()
                time_now = datetime.datetime.now()
                print(f"[{time_now}] Процесс A: получено '{message}', обработано -> '{processed_message}'")
                
                
                pipe_conn.send(processed_message)
                
                
                time.sleep(5)
            else:
                
                time.sleep(0.1)
        except Exception as e:
            print(f"[{datetime.datetime.now()}] Процесс A: ошибка - {e}")
    
    print(f"[{datetime.datetime.now()}] Процесс A завершен")


def process_b(pipe_conn, output_queue, exit_event):
    """
    Процесс B.
    Получает сообщения из pipe_conn, применяет rot13 и отправляет в output_queue.
    """
    print(f"[{datetime.datetime.now()}] Процесс B запущен")
    
    while not exit_event.is_set():
        try:
            if pipe_conn.poll():  
                message = pipe_conn.recv()
                
                if message == "EXIT":
                    print(f"[{datetime.datetime.now()}] Процесс B: получена команда выхода")
                    output_queue.put("EXIT")
                    break
                
                
                encoded_message = codecs.encode(message, 'rot_13')
                time_now = datetime.datetime.now()
                print(f"[{time_now}] Процесс B: получено '{message}', закодировано -> '{encoded_message}'")
                
                
                output_queue.put(encoded_message)
            else:
                
                time.sleep(0.1)
        except Exception as e:
            print(f"[{datetime.datetime.now()}] Процесс B: ошибка - {e}")
    
    print(f"[{datetime.datetime.now()}] Процесс B завершен")


def input_reader(input_queue, exit_event):
    """
    Поток для чтения ввода пользователя.
    """
    print(f"[{datetime.datetime.now()}] Начало чтения пользовательского ввода. Введите 'exit' для завершения.")
    
    while not exit_event.is_set():
        try:
            
            message = input()
            time_now = datetime.datetime.now()
            
            if message.lower() == 'exit':
                print(f"[{time_now}] Получена команда выхода")
                input_queue.put("EXIT")
                exit_event.set()
                break
            
            print(f"[{time_now}] Отправлено в процесс A: '{message}'")
            input_queue.put(message)
        except EOFError:
            
            break
        except Exception as e:
            print(f"[{datetime.datetime.now()}] Ошибка при чтении ввода: {e}")
    
    print(f"[{datetime.datetime.now()}] Чтение пользовательского ввода завершено")


def output_reader(output_queue, exit_event):
    """
    Поток для чтения из выходной очереди.
    """
    print(f"[{datetime.datetime.now()}] Начало чтения выходной очереди")
    
    while not exit_event.is_set():
        try:
            
            if not output_queue.empty():
                message = output_queue.get()
                
                if message == "EXIT":
                    print(f"[{datetime.datetime.now()}] Получена команда выхода из процесса B")
                    break
                
                time_now = datetime.datetime.now()
                print(f"[{time_now}] Получено от процесса B: '{message}'")
            else:
                
                time.sleep(0.1)
        except Exception as e:
            print(f"[{datetime.datetime.now()}] Ошибка при чтении из выходной очереди: {e}")
    
    print(f"[{datetime.datetime.now()}] Чтение выходной очереди завершено")


def main():
    """
    Главный процесс.
    Создает процессы A и B, а также очереди для взаимодействия.
    """
    
    exit_event = multiprocessing.Event()
    
    
    input_queue = multiprocessing.Queue()    
    output_queue = multiprocessing.Queue()   
    
    
    a_conn, b_conn = multiprocessing.Pipe()
    
    
    process_a_instance = multiprocessing.Process(
        target=process_a, 
        args=(input_queue, a_conn, exit_event)
    )
    
    process_b_instance = multiprocessing.Process(
        target=process_b, 
        args=(b_conn, output_queue, exit_event)
    )
    
    
    input_thread = threading.Thread(target=input_reader, args=(input_queue, exit_event))
    output_thread = threading.Thread(target=output_reader, args=(output_queue, exit_event))
    
    try:
        print(f"[{datetime.datetime.now()}] Запуск приложения")
        
        
        process_a_instance.start()
        process_b_instance.start()
        
        
        input_thread.start()
        output_thread.start()
        
        
        input_thread.join()
        output_thread.join()
        
        
        process_a_instance.join()
        process_b_instance.join()
        
    except KeyboardInterrupt:
        print(f"[{datetime.datetime.now()}] Получен сигнал прерывания, завершаем работу")
        exit_event.set()
    except Exception as e:
        print(f"[{datetime.datetime.now()}] Ошибка: {e}")
    finally:
        
        if process_a_instance.is_alive():
            process_a_instance.terminate()
        if process_b_instance.is_alive():
            process_b_instance.terminate()
        
        print(f"[{datetime.datetime.now()}] Приложение завершено")


if __name__ == "__main__":
    main()

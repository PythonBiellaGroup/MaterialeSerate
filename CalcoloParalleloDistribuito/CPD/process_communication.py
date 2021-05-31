import multiprocessing
import time

# FONTE: https://pymotw.com/2/multiprocessing/communication.html


class Consumer(multiprocessing.Process):
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        """
        Estendo la classe multiprocessing.Process, e implemento il codice in run
        :return:
        """
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill, termino il processo
                print('%s: Exiting' % proc_name)
                self.task_queue.task_done()
                break
            print('%s: %s' % (proc_name, next_task))
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return


class Task(object):
    '''
    Definisco un task generico, implemento l'algoritmo in __call__(self)
    '''
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self):
        time.sleep(.5)  # pretend to take some time to do the work
        return '%s * %s = %s' % (self.a, self.b, self.a * self.b)

    def __str__(self):
        return '%s * %s' % (self.a, self.b)


if __name__ == '__main__':
    # Definisco le le code per salvare i task e i risultati

    # JoinableQueue e una coda con informatione sullo stato dei task
    # all'interno (JoinableQueue().task_done()) permette di attendere finche tutti i task nella que sono
    # completati (JoinableQueue().join())
    tasks = multiprocessing.JoinableQueue()

    results = multiprocessing.Queue()

    # Start consumers
    num_consumers = multiprocessing.cpu_count() * 2
    print('Creating %d consumers' % num_consumers)
    consumers = [Consumer(tasks, results)
                 for i in range(num_consumers)]
    for w in consumers:
        w.start()

    # Enqueue jobs
    num_jobs = 50

    for i in range(num_jobs):
        tasks.put(Task(i, i))

    # Aggiungi una 'Poison pill' per ogni consumer
    # La poison pill e un oggetto specifico per dire ai processi di terminare in quanto il loro lavoro non e piu
    # richiesto
    for i in range(num_consumers):
        tasks.put(None)

    # Wait for all of the tasks to finish
    tasks.join()

    # Stampa i risultati dalla coda
    while num_jobs:
        result = results.get()
        print('Result:', result)
        num_jobs -= 1

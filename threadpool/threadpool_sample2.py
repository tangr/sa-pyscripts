import queue
import threading
# import urllib2
import urllib.request
import time
# from beautifulsoup4 import BeautifulSoup
from bs4 import BeautifulSoup

# https://developer.ibm.com/articles/au-threadingpython/#using-queues-with-threads

hosts = ["http://yahoo.com", "http://google.com",
        "http://ibm.com", "http://apple.com"]
in_queue = queue.Queue()
out_queue = queue.Queue()

class ThreadUrl(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue, outqueue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.outqueue = outqueue

    def run(self):
        while True:
            #grabs host from queue
            host = self.queue.get()

            #grabs urls of hosts and then grabs chunk of webpage
            # url = urllib2.urlopen(host)
            url = urllib.request.urlopen(host)
            chunk = url.read()

            #place chunk into out queue
            self.outqueue.put(chunk)

            #signals to queue job is done
            self.queue.task_done()

class DatamineThread(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, out_queue):
        threading.Thread.__init__(self)
        self.out_queue = out_queue

    def run(self):
        while True:
            #grabs host from queue
            chunk = self.out_queue.get()

            #parse the chunk
            soup = BeautifulSoup(chunk, features="html.parser")
            print(soup.findAll(['title']))

            #signals to queue job is done
            self.out_queue.task_done()

start = time.time()
def main():
    #populate queue with data
    for host in hosts:
        in_queue.put(host)

    #spawn a pool of threads, and pass them queue instance
    for i in range(5):
        t = ThreadUrl(in_queue, out_queue)
        t.setDaemon(True)
        t.start()

    for i in range(5):
        dt = DatamineThread(out_queue)
        dt.setDaemon(True)
        dt.start()

    #wait on the queue until everything has been processed
    in_queue.join()
    out_queue.join()

if __name__ == '__main__':
    main()
    print("Elapsed Time: %s" % (time.time() - start))

#!/usr/bin/python
# -*- coding: utf-8 -*-

#Python的线程池实现
# https://blog.51cto.com/1238306/1742627

import queue
import threading
import sys
import time
import urllib
import subprocess
import os

#替我们工作的线程池中的线程
class MyThread(threading.Thread):
    def __init__(self, workQueue, resultQueue, timeout=5, **kwargs):
        threading.Thread.__init__(self, kwargs=kwargs)
        #线程在结束前等待任务队列多长时间
        self.timeout = timeout
        self.setDaemon(True)
        self.workQueue = workQueue
        self.resultQueue = resultQueue
        self.start()

    def run(self):
        while True:
            try:
                #从工作队列中获取一个任务
                callable, args, kwargs = self.workQueue.get(timeout=self.timeout)
                #我们要执行的任务
                arg1 = self.workQueue.qsize()
                res = callable(arg1, kwargs)
                #报任务返回的结果放在结果队列中
                self.resultQueue.put(self.getName() + " | " + str(self.ident) + " | " + str(res))
                arg2 = self.resultQueue.qsize()
            except queue.Empty: #任务队列空的时候结束此线程
                break
            except :
                print(sys.exc_info())
                raise

class ThreadPool:
    def __init__(self, num_of_threads=10):
        self.workQueue = queue.Queue()
        self.resultQueue = queue.Queue()
        self.threads = []
        self.__createThreadPool(num_of_threads)

    def __createThreadPool(self, num_of_threads):
        for i in range( num_of_threads ):
            thread = MyThread(self.workQueue, self.resultQueue)
            print('*****************')
            print(thread.workQueue)
            print(thread.workQueue.qsize())
            print('*****************')
            self.threads.append(thread)
            print(self.threads)

    def wait_for_complete(self):
        #等待所有线程完成。
        while len(self.threads):
            thread = self.threads.pop()
            # print(threading.active_count())
            # print(threading.enumerate())
            #等待线程结束
            if thread.isAlive():#判断线程是否还存活来决定是否调用join
                thread.join()

    def add_job(self, callable, *args, **kwargs):
        self.workQueue.put((callable, args, kwargs))

def workerfun(arg1, arg2):
    html = ""
    try:
        time.sleep(1)
        # conn = urllib.urlopen('http://www.baidu.com/')
        # html = conn.read(20)
        html = arg1
        processes = subprocess.Popen(
                    'echo ${PPID} "|" $$',
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    stdin=subprocess.PIPE,
                    universal_newlines=True,
                    cwd='/tmp'
        )
        line = processes.stdout.readline()
        line = line.rstrip()
    except:
        print(sys.exc_info())
    return line


def main():
    print('start testing')
    tp = ThreadPool(5)
    for i in range(20):
        time.sleep(0.2)
        tp.add_job(workerfun, i)
        print(tp)
    tp.wait_for_complete()

    #处理结果
    print('result Queue\'s length == %d '% tp.resultQueue.qsize())
    while tp.resultQueue.qsize():
        print(tp.resultQueue.get())
    print('end testing')

if __name__ == '__main__':
    main()

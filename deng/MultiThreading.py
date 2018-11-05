#!/usr/bin/env python
# coding=utf-8
import sys 
import queue 
import threading
from time import time
from requests import ConnectionError


class MultiThreading(object):
    def __init__(self, func_list=None):
        # 所有线程函数的返回值汇总，如果最后为0，说明全部成功
        self.ret_flag = 0
        self.func_list = func_list
        self.threads = []
         
    def set_thread_func_list(self, func_list):
        """
        @note: func_list是一个list，每个元素是一个dict，
        有func和args两个参数，func为函数引用，args为元组
        """
        self.func_list = func_list
        
    def trace_func(self, func, *args, **kwargs):
        """
        @note:替代profile_func，新的跟踪线程返回值的函数，
        对真正执行的线程函数包一次函数，以获取返回值
        """
        ret = func(*args, **kwargs)
        self.ret_flag += ret
        
    def start(self, count=None):
        """
        @note: 启动多线程执行，并阻塞到结束
        """
        self.threads = []
        self.ret_flag = 0

        for func_dict in self.func_list:
            if count is None:
                if func_dict["args"]:
                    t = threading.Thread(target=func_dict["func"],
                                         args=func_dict["args"])
                else:
                    t = threading.Thread(target=func_dict["func"])
            else:
                if func_dict["args"]:
                    new_arg_list = []
                    new_arg_list.append(func_dict["func"])
                    for arg in func_dict["args"]:
                        new_arg_list.append(arg)
                    new_arg_tuple = tuple(new_arg_list)
                    t = threading.Thread(target=self.trace_func,
                                         args=new_arg_tuple)
                else:
                    t = threading.Thread(target=self.trace_func,
                                         args=(func_dict["func"],))
            self.threads.append(t)
     
        for thread_obj in self.threads:
            thread_obj.start()
     
        for thread_obj in self.threads:
            thread_obj.join()
 
    def get_value(self):
        """
        @note: 所有线程函数的返回值之和，如果为0那么表示所有函数执行成功
        """
        return self.get_flag


class MyThread(threading.Thread):
    def __init__(self, work_queue, result_queue, timeout, save_resule=True, *args, **kwargs):
        threading.Thread.__init__(self, *args, kwargs=kwargs)
        # 线程从工作队列中取任务超时时间
        self.timeout = timeout 
        self.daemon = True
        self.work_queue = work_queue 
        self.result_queue = result_queue
        self.save_resule = save_resule
        self.start()
        
    def run(self):
        while True:
            try:
                # 从工作队列中获取任务
                func, args, kwargs = self.work_queue.get(timeout=self.timeout)
                # 执行任务
                # 执行结果变量
                res = 1
                # 启动时间
                starttime = int(time())
                if self.save_resule:
                    # 保存执行结果
                    res = func(*args, **kwargs)
                else:
                    # 不保执行存结果
                    func(*args, **kwargs)
                # 执行结束时间
                endtime = int(time())
                # 把任务执行结果放入结果队列中
                self.result_queue.put((self.getName(), endtime - starttime, res))
            except queue.Empty:
                print('线程【{}】任务已完成（从queue队列中获取任务超时【{}秒】），退出！'.format(self.ident, self.timeout))
                break


class ThreadPool(object):
    def __init__(self):
        self.work_queue = queue.Queue() 
        self.result_queue = queue.Queue() 
        self.threads = []
        self.request_count = 0
        self.starttime = 0
        self.endtime = 0
        
    def create_threadpool(self, num_of_threads, timeout, save_resule):
        """
        @note:创建线程池
        """
        print("本次启动【{}】个线程，"
              "线程超时时间为【{}】秒，"
              "保存每次执行结果：【{}】".format(num_of_threads, timeout, save_resule))
        request_count = self.work_queue.qsize()
        starttime = int(time()) 
        for i in range(num_of_threads):
            thread = MyThread(self.work_queue, self.result_queue, timeout, save_resule)
            self.threads.append(thread)
        # 设置等待所有子线程完成
        self._wait_for_complete()
        endtime = int(time())
        print("=========================")
        print("总计请求数：", request_count)
        print("starttime:", starttime)
        print("endtime  :", endtime)
        print("运行总耗时：", endtime - starttime)
        print("成功处理了", self.result_queue.qsize(), "次请求！")
        print("=========================")
        return self.result_queue

    def _wait_for_complete(self):
        """
        @note:等待所有线程完成
        """
        while len(self.threads):
            thread = self.threads.pop()
            # 等待线程结束
            if thread.isAlive():
                # 判断线程是否存在来决定是否调用join
                thread.join()

    def create_threadpool_nowait(self, num_of_threads, timeout, save_resule):
        """
        @note:创建线程池
        """
        self.starttime = int(time())
        print("本次启动【{}】个线程，"
              "线程超时时间为【{}】秒，"
              "保存每次执行结果：【{}】".format(num_of_threads, timeout, save_resule))
        for i in range(num_of_threads):
            thread = MyThread(self.work_queue, self.result_queue, timeout, save_resule)
            self.threads.append(thread)

    def wait_for_complete(self):
        """
        @note:等待所有线程完成
        """
        while len(self.threads):
            thread = self.threads.pop()
            # 等待线程结束
            if thread.isAlive():
                # 判断线程是否存在来决定是否调用join
                thread.join()
        self.request_count = self.result_queue.qsize()
        self.endtime = int(time())
        print("=========================")
        print("总计请求数：", self.request_count)
        print("starttime:", self.starttime)
        print("endtime  :", self.endtime)
        print("运行总耗时：", self.endtime - self.starttime)
        print("成功处理了", self.request_count, "次请求！")
        print("=========================")

    def add_job(self, func, *args, **kwargs):
        """
        @note:往工作队列中添加任务
        """
        self.work_queue.put((func, args, kwargs))

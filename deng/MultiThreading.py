#!/usr/bin/env python
# coding=utf-8
import sys 
import Queue 
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
    def __init__(self, work_queue, result_queue, timeout, **kwargs):
        threading.Thread.__init__(self, kwargs=kwargs)
        # 线程从工作队列中取任务超时时间
        self.timeout = timeout 
        self.setDaemon(True) 
        self.work_queue = work_queue 
        self.result_queue = result_queue 
        self.start()
        
    def run(self):
        while True:
            try:
                # 从工作队列中获取任务
                func, args, kwargs = self.work_queue.get(timeout=self.timeout)
                # 执行任务
                res = func(*args, **kwargs)
                # 把任务执行结果放入结果队列中
                self.result_queue.put((self.getName(), int(time()), res))
            except Queue.Empty:
                break
            except ConnectionError:
                print "连接被拒绝，重试……"
            except Exception as e:
                print sys.exc_info()
                print e


class ThreadPool(object):
    def __init__(self):
        self.work_queue = Queue.Queue() 
        self.result_queue = Queue.Queue() 
        self.threads = []
        
    def create_threadpool(self, num_of_threads, timeout):
        """
        @note:创建线程池
        """
        request_count = self.work_queue.qsize()
        starttime = int(time()) 
        for i in range(num_of_threads):
            thread = MyThread(self.work_queue, self.result_queue, timeout)
            self.threads.append(thread)
        # 设置等待所有子线程完成
        self._wait_for_complete()
        endtime = int(time())
        print "========================="
        print "总计请求数：", request_count
        print "starttime:", starttime
        print "endtime  :", endtime 
        print "运行总耗时：", endtime - starttime
        print "成功处理了", self.result_queue.qsize(), "次请求！"
        print "========================="
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
     
    def add_job(self, func, *args, **kwargs):
        """
        @note:往工作队列中添加任务
        """
        self.work_queue.put((func, args, kwargs))

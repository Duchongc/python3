# encoding: utf-8
import threading
import time
def ChiHuoGuo(people):
    print("%s 吃火锅的小伙伴-羊肉: %s" %(time.ctime(),people))
    time.sleep(1)
    print("%s 吃火锅的小伙伴-鱼丸:%s" %(time.ctime(),people))
class myThread(threading.Thread):
    def __init__(self,people,name):
        threading.Thread.__init__(self)
        self.threadName = name
        self.people = people
    def run(self):
        print(" 开始线程:"+self.threadName)
        ChiHuoGuo(self.people)
        print("结束线程:"+self.name)
print(u"崇崇请小伙伴吃火锅")
threads = []
thread1 = myThread("yoyo","Thread-1")
thread2 = myThread("laji","Thread-2")

threads.append(thread1)
threads.append(thread2)
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()



time.sleep(1)
print("退出主线程")
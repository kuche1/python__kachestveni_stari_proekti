from ctypes import *
import time

dll = CDLL('testDLL.dll')


c_int_3 = c_int(3)
c_int_5 = c_int(5)
dll_add = dll.add

s=time.time()
for x in range(5000000):
    a = 5+3
print(time.time()-s)

s=time.time()
for x in range(5000000):
    a = dll_add(c_int_3,c_int_5)
print(time.time()-s)

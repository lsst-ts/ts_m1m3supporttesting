import time
import datetime
import os
import os.path
import math

def Equal(topic, actual, expected):
    message = "Check %s (%s) = %s" % (topic, GetFormat(actual), GetFormat(expected))
    return Result(message, actual == expected)
    
def NotEqual(topic, actual, expected):
    message = "Check %s (%s) != %s" % (topic, GetFormat(actual), GetFormat(expected))
    return Result(message, actual != expected)
    
def LessThan(topic, actual, expected):
    message = "Check %s (%s) < %s" % (topic, GetFormat(actual), GetFormat(expected))
    return Result(message, actual < expected)

def LessThanEqual(topic, actual, expected):
    message = "Check %s (%s) <= %s" % (topic, GetFormat(actual), GetFormat(expected))
    return Result(message, actual <= expected)

def GreaterThan(topic, actual, expected):
    message = "Check %s (%s) > %s" % (topic, GetFormat(actual), GetFormat(expected))
    return Result(message, actual > expected)

def GreaterThanEqual(topic, actual, expected):
    message = "Check %s (%s) >= %s" % (topic, GetFormat(actual), GetFormat(expected))
    return Result(message, actual >= expected)

def InRange(topic, actual, min, max):
    message = "Check %s (%s) in [%s, %s]" % (topic, GetFormat(actual), GetFormat(min), GetFormat(max))
    return Result(message, actual >= min and actual <= max)
    
def WaitUntil(topic, timeout, eval):
    start = time.time()
    timedout = False
    while not eval():
        time.sleep(0.1)
        if time.time() - start >= timeout:
           timedout = True
           break
    message = "WaitUntil %s or %0.3fs" % (topic, timeout)
    return Result(message, not timedout)

def InTolerance(topic, actual, expected, tolerance):
    message = "Check %s (%s) = %s (+/-)%s" % (topic, GetFormat(actual), GetFormat(expected), GetFormat(tolerance))
    return Result(message, actual >= (expected - tolerance) and actual <= (expected + tolerance))        
    
def Header(message):
    print("*********************************************")
    print("***** %s" % message)
    print("*********************************************")
    
def SubHeader(message):
    print("***** %s" % message)
    
def Log(message):
    _Log("     - %s" % message)

def _Log(message):
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%S')
    print("%s: %s" % (timestamp, message))
    
def Result(message, result):
    text = "ANOM"
    if result:
        text = "PASS"
    _Log("%s - %s" % (text, message))
    return result
    
def GetFormat(value):
    if isinstance(value, int):
        return "%d" % value
    if isinstance(value, float):
        return "%f" % value
    return "%s" % value
    
def GetFilePath(file):
    return os.path.join(os.path.expanduser("~"), file)
    
def Average(data, accessor):
    sum = 0.0
    count = 0
    for item in data:
        count += 1
        sum += accessor(item)
    return sum / count
    
def ActuatorToCylinderSpace(o, x, y, z):
    if o == '+Y':
        return z - y, y * math.sqrt(2)
    if o == '-Y':
        return z + y, -y * math.sqrt(2)
    if o == '+X':
        return z - x, x * math.sqrt(2)
    if o == '-X':
        return z + x, -x * math.sqrt(2)
    return z, 0
    

#Equal("A", 1, 2)
#Equal("A", 2, 2)
#NotEqual("B", 1, 2)
#NotEqual("B", 2, 2)
#LessThan("C", 1, 2)
#LessThan("C", 2, 2)
#LessThan("C", 3, 2)
#LessThanEqual("D", 1, 2)
#LessThanEqual("D", 2, 2)
#LessThanEqual("D", 3, 2)
#GreaterThan("E", 1, 2)
#GreaterThan("E", 2, 2)
#GreaterThan("E", 3, 2)
#GreaterThanEqual("F", 1, 2)
#GreaterThanEqual("F", 2, 2)
#GreaterThanEqual("F", 3, 2)
#InRange("G", 1, 2, 3)
#InRange("G", 2, 2, 3)
#InRange("G", 3, 2, 3)
#InRange("G", 4, 2, 3)
#InTolerance("H", 1, 3, 1)
#InTolerance("H", 2, 3, 1)
#InTolerance("H", 3, 3, 1)
#InTolerance("H", 4, 3, 1)
#InTolerance("H", 5, 3, 1)
#WaitUntil("I", 1.0, lambda: False)
#WaitUntil("I", 1.0, lambda: True)
#Log("Hello World")

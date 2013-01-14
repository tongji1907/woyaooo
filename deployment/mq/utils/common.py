import time
import hashlib
import random

NOW = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

def MD5(str):
    return hashlib.md5(str).hexdigest().upper()

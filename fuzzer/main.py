import generator
from ctypes import CDLL
import numpy as np

# Initializes the harness and sets it up for work
harness = CDLL("harness/harness.so")

while True:
    t = generator.generate()
    harness.register_testcase(bytes(t, 'ascii'))
    try:
        exec(t, {'np':np})
    except:
        # If the exec fails, then we should not store
        continue
    generator.register(t)

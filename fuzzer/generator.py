import random

def generate():
    # TODO: Write a proper generator here
    return random.choice(["print('a')", 'print "A"'])

def register(t):
    # TODO: Use the generated valid code to seed the fuzzer more
    pass

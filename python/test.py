import time
import threading
from visualization import start, stop

def background():
    while True:
        # number = int(len(oilrigs)) * 49
        # number += money
        # time.sleep(1)
        print('starting visuals')
        start()

def foreground():
    print('started')
    # What you want to run in the foreground
    time.sleep(5)
    print('stopping visuals')
    stop()

b = threading.Thread(name='background', target=background)
f = threading.Thread(name='foreground', target=foreground)

b.start()
f.start()
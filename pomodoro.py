import time, sys, subprocess
from tqdm import tqdm

def send_notification(text):
    subprocess.run(['notify-send', text])

def timer(minutes=0, seconds=0):
    seconds += 60 * minutes
    for _ in tqdm(range(seconds)):
        time.sleep(1.0)
    send_notification("Timer has run out")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Using default value of 25 minutes")
        timer(minutes=25)
    else:
        timer(minutes=int(sys.argv[1]))

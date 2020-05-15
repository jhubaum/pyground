import time, sys, subprocess
from tqdm import tqdm

def send_notification(text):
    subprocess.run(['notify-send', text])


def set_terminal_title(title):
    print(f'\033]2;{title}\a')

def format_remaining_str(remaining, prefix="Pomodoro timer. Time remaining: "):
    seconds = remaining % 60
    minutes = remaining // 60
    hours = minutes // 60
    minutes %= 60

    l = [minutes, seconds]
    if hours > 0:
        l.insert(0, hours)

    return prefix + ':'.join(map(lambda x: str(x).zfill(2), l))


def timer(minutes=0, seconds=0):
    seconds += 60 * minutes
    set_terminal_title(format_remaining_str(seconds))
    for r in tqdm(range(seconds-1, -1, -1),
            desc="Progress: ",
            bar_format='{desc} |{bar}| ({remaining} remaining)'):
        time.sleep(1.0)
        set_terminal_title(format_remaining_str(r))
    send_notification("Timer has run out")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Using default value of 25 minutes")
        timer(minutes=25)
    else:
        timer(minutes=int(sys.argv[1]))

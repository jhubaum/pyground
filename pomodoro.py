import time, subprocess
from tqdm import tqdm
import argparse

def setup_argparser():
    parser = argparse.ArgumentParser(description='A simple pomodoro timer')
    parser.add_argument('time', default=25, type=int,
            help='the length of the timer in minutes')
    return parser


def send_notification(summary, body=''):
    subprocess.run(['notify-send', summary, body])


def set_terminal_title(title):
    print(f'\033]2;{title}\a', end='', flush=True)


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
    timer_range = range(1, seconds+1)
    with tqdm(total=seconds, position=0, leave=True) as pbar:
        for i in tqdm(timer_range, position=0, leave=True,
                      desc="Progress: ",
                      bar_format='{desc} |{bar}| ({remaining} remaining)'):
            time.sleep(1.0)
            pbar.update()
            set_terminal_title(format_remaining_str(seconds-i))

    send_notification("Take a break", "The timer has run out")

if __name__ == '__main__':
    args = setup_argparser().parse_args()
    timer(minutes=args.time)

import time, subprocess
from tqdm import tqdm
import argparse

def setup_argparser():
    parser = argparse.ArgumentParser(description='A simple pomodoro timer')
    parser.add_argument('time', type=int, default=25,
            help='the length of the timer in minutes')
    parser.add_argument('--output-method', choices=['tqdm', 'window-title'], 
            default='window-title',
            help="""How is the remaining time shown? \n
                    \n\ttqdm: using a progress bar\
                    \n\twindow-title: the title of terminal is updated (default)""")

    return parser


def send_notification(text):
    subprocess.run(['notify-send', text])


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


def timer(minutes=0, seconds=0, output='tqdm'):
    seconds += 60 * minutes
    if output == 'window-title':
        set_terminal_title(format_remaining_str(seconds))

    timer_range = range(seconds-1, -1, -1)
    if output == 'tqdm':
        timer_range = tqdm(timer_range,
                desc="Progress: ",
                bar_format='{desc} |{bar}| ({remaining} remaining)')

    for r in timer_range:
        time.sleep(1.0)
        if output == 'window-title':
            set_terminal_title(format_remaining_str(r))
    send_notification("Timer has run out")

if __name__ == '__main__':
    args = setup_argparser().parse_args()
    timer(minutes=args.time, output=args.output_method)

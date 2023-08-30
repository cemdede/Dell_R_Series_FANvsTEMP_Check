#!/usr/bin/env python3
import curses
import subprocess
import time
import re

# Define spinner states
spinner_states = ['|', '/', '-', '\\']

def get_fan_info():
    result = subprocess.run(["sudo", "ipmitool", "sdr", "type", "fan"], capture_output=True, text=True)
    return result.stdout.strip()

def get_temp_info():
    result = subprocess.run(["sudo", "ipmitool", "sdr", "type", "temperature"], capture_output=True, text=True)
    return result.stdout.strip()

def get_color_for_value(value, scale_type):
    if scale_type == 'temperature':
        if 34 <= value <= 38:
            return 1  # Green
        elif 38 < value <= 50:
            return 2  # Yellow
        elif 50 < value <= 70:
            return 4  # Orange
        else:
            return 3  # Red
    elif scale_type == 'fan_speed':
        if 2000 <= value <= 5000:
            return 1  # Green
        elif 5000 < value <= 9000:
            return 2  # Yellow
        elif 9000 < value <= 13000:
            return 4  # Orange
        else:
            return 3  # Red

def extract_numeric_value(s, pattern):
    match = re.search(pattern, s)
    return float(match.group(1)) if match else None

def main(stdscr):
    # Initialize spinner index
    spinner_idx = 0

    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Orange color
    stdscr.nodelay(True)  # Make getch non-blocking
    stdscr.timeout(1000)  # Refresh every 1 second

    while True:
        stdscr.clear()

        fan_info = get_fan_info().split('\n')
        temp_info = get_temp_info().split('\n')

        highest_temp = max([extract_numeric_value(s, r"\b(\d+\.?\d*) degrees C\b") for s in temp_info if extract_numeric_value(s, r"\b(\d+\.?\d*) degrees C\b") is not None])
        fan_speeds = [extract_numeric_value(s, r"\b(\d+\.?\d*) RPM\b") for s in fan_info if extract_numeric_value(s, r"\b(\d+\.?\d*) RPM\b") is not None]
        mean_fan_speed = int(sum(fan_speeds) / len(fan_speeds)) if fan_speeds else 0

        temp_color = get_color_for_value(highest_temp, 'temperature')
        fan_speed_color = get_color_for_value(mean_fan_speed, 'fan_speed')

        stdscr.addstr(0, 0, f"Heat of Highest Temp Sensor: {highest_temp}C ", curses.color_pair(temp_color))
        stdscr.addstr(0, 60, f"Mean Fan Speed: {mean_fan_speed} RPM ", curses.color_pair(fan_speed_color))

        stdscr.addstr(1, 0, '-' * 120)

        for i in range(max(len(fan_info), len(temp_info))):
            stdscr.addstr(i + 2, 55, "|", curses.color_pair(1))

        for idx, temp_line in enumerate(temp_info):
            stdscr.addstr(idx + 2, 0, temp_line.ljust(55))

        for idx, fan_line in enumerate(fan_info):
            stdscr.addstr(idx + 2, 56, " " + fan_line.ljust(54))

        # Update the spinner index and draw it with a 2-line gap after Temp info
        spinner_idx = (spinner_idx + 1) % len(spinner_states)
        stdscr.addstr(len(temp_info) + 4, 0, f"Running {spinner_states[spinner_idx]}", curses.color_pair(5))

        stdscr.refresh()

        c = stdscr.getch()  # Capture the keypress
        if c != -1:  # If a key was pressed
            if c == ord('q'):
                break  # Exit the loop when 'q' is pressed

if __name__ == "__main__":
    curses.wrapper(main)


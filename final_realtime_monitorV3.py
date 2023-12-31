#!/usr/bin/env python3

import curses
import subprocess
import time
import re
import math
import logging

logging.basicConfig(filename='/tmp/cron.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Spinner states
spinner_states = ['|', '/', '-', '\\']

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

def get_fan_info():
    result = subprocess.run(["sudo", "ipmitool", "sdr", "type", "fan"], capture_output=True, >
    return result.stdout.strip()

def get_temp_info():
    result = subprocess.run(["sudo", "ipmitool", "sdr", "type", "temperature"], capture_outpu>
    return result.stdout.strip()

def get_gpu_temp_info():
    result = subprocess.run(["nvidia-smi", "-q", "-d", "TEMPERATURE"], capture_output=True, t>
    temp_info = result.stdout
    match = re.search(r"GPU Current Temp\s+:\s+(\d+) C", temp_info)
    return int(match.group(1)) if match else None

    def extract_numeric_value(s, pattern):
        match = re.search(pattern, s)
        return float(match.group(1)) if match else None

def main(stdscr):
    spinner_idx = 0
    cpu_count = 0  # To track the number of CPUs

    subprocess.run(["sudo", "ipmitool", "raw", "0x30", "0x30", "0x01", "0x00"])
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_RED)

    stdscr.timeout(1000)

    while True:
        stdscr.clear()

        fan_info = get_fan_info().split('\n')
        temp_info = get_temp_info().split('\n')

        corrected_temp_info = []
        for line in temp_info:
            if "Inlet Temp" in line:
                line = line.replace("Inlet Temp", "Board Inlet Temp")
            elif "Exhaust Temp" in line:
                line = line.replace("Exhaust Temp", "Board Exhaust Temp")
            elif "Temp" in line:
                cpu_count += 1
                line = line.replace("Temp", f"CPU_{cpu_count} Temp")

            corrected_temp_info.append(line)

        # Reset the CPU count for the next iteration
        cpu_count = 0

        highest_temp = max([extract_numeric_value(s, r"\b(\d+\.?\d*) degrees C\b") for s in t>
        fan_speeds = [extract_numeric_value(s, r"\b(\d+\.?\d*) RPM\b") for s in fan_info if e>
        mean_fan_speed = int(sum(fan_speeds) / len(fan_speeds)) if fan_speeds else 0
        gpu_temp = get_gpu_temp_info()

        logging.info(f"Heat of Highest Temp Sensor: {highest_temp}C")
        logging.info(f"Mean Fan Speed: {mean_fan_speed} RPM")
        logging.info(f"GPU Temperature: {gpu_temp}C")

        temp_color = get_color_for_value(highest_temp, 'temperature')
        fan_speed_color = get_color_for_value(mean_fan_speed, 'fan_speed')
        gpu_temp_color = get_color_for_value(gpu_temp, 'temperature')

        stdscr.addstr(0, 0, f"Highest Tempreture for Board or CPUs: {highest_temp}C ", curses>
        stdscr.addstr(0, 60, f"Mean Fan Speed: {mean_fan_speed} RPM ", curses.color_pair(fan_>
        stdscr.addstr(0, 90, f"GPU Temperature: {gpu_temp}C ", curses.color_pair(gpu_temp_col>
        stdscr.addstr(1, 0, '-' * 114)

        for i in range(max(len(corrected_temp_info), len(fan_info))):
            stdscr.addstr(i + 2, 58, "|", curses.color_pair(1))

        for idx, temp_line in enumerate(corrected_temp_info):
            stdscr.addstr(idx + 2, 0, f"{temp_line:<54}")

        spinner_idx = (spinner_idx + 1) % len(spinner_states)
        stdscr.addstr(len(corrected_temp_info) + 4, 0, f"Running {spinner_states[spinner_idx]>

        for idx, fan_line in enumerate(fan_info):
            stdscr.addstr(idx + 2, 60, f"{fan_line:<54}")

        stdscr.refresh()

        c = stdscr.getch()
        if c == ord('q'):
            break

if __name__ == "__main__":
    curses.wrapper(main)

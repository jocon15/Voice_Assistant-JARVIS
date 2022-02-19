"""This script is the peripheral for notes. The stored notes will be printed to a terminal."""
import time
import MasterConfig


with open(f'{MasterConfig.cwd}\\stored_notes\\notes.txt', 'r') as file:
    lines = file.readlines()

for line in lines:
    print(line)

time.sleep(10000)

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 15:46:27 2020

@author: Brendan Non-Admin
"""


import sys
import time

class SameLinePrinter:
    
    def __init__(self, previous_line_length=0):
        self.previous_line_length = previous_line_length
        
    def print_line(self, line):
        print('\r' + ' ' * self.previous_line_length + '\r', end='')
        print(line, end='')
        sys.stdout.flush()
        self.previous_line_length = len(line)
        
printer = SameLinePrinter()
for i in range(1, 11):
    time.sleep(0.5)
    printer.print_line("Test: {:>3} / 10".format(i))
    
from tqdm import tqdm

for i in tqdm(range(1, 11)):
    time.sleep(0.5)
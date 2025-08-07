"""
This module contains useful functions.
"""
from tqdm import tqdm

class ProgressBar:
    def __init__(self, total, desc="Processing"):
        self.progress_bar = tqdm(total=total, desc=desc, unit='scenario')

    def update(self, n=1):
        self.progress_bar.update(n)

    def close(self):
        self.progress_bar.close()
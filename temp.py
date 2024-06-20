# delete all jon file in the current directory

import os
import glob

files = glob.glob('*.json')

for f in files:
    os.remove(f)


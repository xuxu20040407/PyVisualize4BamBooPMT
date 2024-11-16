import os

import pyvisualize_PMT as pv
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--dirtime', type=int, default=1000, help='Time in ps')
parser.add_argument('--dirindex', type=int, default=0, help='Index of the directory')
args = parser.parse_args()

dirtime = args.dirtime
dirindex = args.dirindex


folder_path = f'../Trace_pattern_time/{dirtime}ps/{dirindex}'
new_folder=f'./TopPMT/{dirtime}ps/{dirindex}'
os.makedirs(new_folder, exist_ok=True)
heatmapper = pv.TopPMTHeatmapper(71,folder_path,new_folder)
heatmapper.process_all_files()
from fileReader import get_data
from dataHandler import *
import os
from tkinter import filedialog


def get_data_from_txt():
    pre_result_dir = filedialog.askdirectory()
    pre_result_file_list = os.listdir(pre_result_dir)

    dataset_from_dwg = get_data(pre_result_file_list[0], pre_result_dir)
    pages = detect_pages(dataset_from_dwg)
    print(len(pages))

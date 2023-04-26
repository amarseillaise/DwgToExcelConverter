from fileReader import get_data
from dataHandler import *
import os
from tkinter import filedialog
from Objects.ProcessFlow import ProcessFlow
import logging

logging.basicConfig(level=logging.DEBUG, filename="log.log", format="%(asctime)s %(levelname)s %(message)s")


def get_data_from_txt():
    pre_result_dir = filedialog.askdirectory(title="Выберите папку с выгрузкой техпроцессов .txt")
    pre_result_file_list = os.listdir(pre_result_dir)

    dataset_from_dwg_list = [get_data(x, pre_result_dir) for x in pre_result_file_list]
    pages_list = [detect_pages(x) for x in dataset_from_dwg_list]
    return pages_list


def get_process_flow(pages_list):
    pf_list = []
    for pages in pages_list:
        pf = None
        for page in pages:
            if page.kind.lower() == "мк" and page.form == "2":
                pf = ProcessFlow(marker=page.name_tech,
                                 file_name=page.file_name,
                                 name=page.name,
                                 description=page.description,
                                 developer=page.developer,
                                 checker=page.checker,
                                 approver=page.approver,
                                 normalizator=page.normalizator,
                                 liter=page.liter)
        if pf is None:
            raise Exception(f"MK page is not defined in file {pages[0].file_name}")
        detect_operations(pf, pages)
        detect_shifts(pf, pages)
        pf_list.append(pf)
    return pf_list

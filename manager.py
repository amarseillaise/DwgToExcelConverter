import os
import logging
from tkinter import filedialog
from dataIO import get_data
from Objects.Page import detect_pages
from Objects.ProcessFlow import ProcessFlow


logging.basicConfig(level=logging.DEBUG, filename="log.log", format="%(asctime)s %(levelname)s %(message)s")
logging.debug("######################START######################")


def get_data_from_txt():
    while True:
        pre_result_dir: str = filedialog.askdirectory(title="Выберите папку с выгрузкой техпроцессов .txt")
        pre_result_file_list: list = os.listdir(pre_result_dir)
        if pre_result_file_list:
            break

    dataset_from_dwg_list: list = [get_data(x, pre_result_dir) for x in pre_result_file_list]
    pages_list: list = [detect_pages(x) for x in dataset_from_dwg_list]
    if len(pages_list) < 1:
        raise Exception("Failed resolve pages")
    return pages_list


def get_process_flow(pages_list: list):
    pf_list = []
    for pages in pages_list:
        pf = None
        for page in pages:
            if page.kind.lower() == "мк" and page.form == "2":
                pf = ProcessFlow(marker=page.name_tech,
                                 file_name=page.__file_name,
                                 name=page.name,
                                 description=page.description,
                                 developer=page.developer,
                                 checker=page.checker,
                                 approver=page.approver,
                                 normalizator=page.normalizator,
                                 liter=page.liter)
        if not pf:
            raise Exception(f"MK page is not defined in file {pages[0].__file_name}")
        pf.detect_operations(pages)
        pf.detect_shifts(pages)
        pf_list.append(pf)
    return pf_list

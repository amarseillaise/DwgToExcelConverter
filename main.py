import manager
import writerToExcel


def main():
    pages_list = manager.get_data_from_txt()
    pf_list = manager.get_process_flow(pages_list)
    writerToExcel.write_pf_to_excel(pf_list)


if __name__ == "__main__":
    main()

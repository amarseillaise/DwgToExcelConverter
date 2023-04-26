import manager
import writerToExcel


def main():
    pages_list = manager.get_data_from_txt()
    process_flows = manager.get_process_flow(pages_list)
    writerToExcel.write_pf_to_excel(process_flows)


if __name__ == "__main__":
    main()

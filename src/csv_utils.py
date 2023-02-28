import csv


def read_in_data_as_tuples(csv_fpath, has_header=True):
    header = None
    tuples = []

    with open(csv_fpath, "r") as f:
        reader = csv.reader(f, delimiter='\t')

        is_first_row = has_header
        for row in reader:
            if is_first_row:
                header = row
                is_first_row = False
            else:
                tuples.append(row)

    return header, tuples


def write_out_data_helper(dict_list, filename, mode="w", has_header=True):
    if len(dict_list) <= 0:
        return ""

    with open(filename, mode) as csvfile:
        writer = csv.DictWriter(csvfile, delimiter='\t',
                                fieldnames=dict_list[0].keys())

        if mode == "w" and has_header:
            writer.writeheader()

        for datum in dict_list:
            try:
                writer.writerow(datum)
            except BaseException:
                print("failed on {0}".format(datum))
                continue

    return filename


def append_data_to_file(dict_list, filename):
    return write_out_data_helper(dict_list, filename, mode="a")

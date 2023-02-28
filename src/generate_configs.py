import config_io


def generate_configs_from_files_and_add_fields(file):
    cfg = config_io.read_config_from_file(file)
    cfg["config_fpath"] = file

    return cfg

# This is a sample Python script.
import datetime
import os
import sys

import config_io
import config_object as trial
import constants
import csv_utils
import generate_configs
import sqlite_helper_object
import system_utils

CONFIG_OBJ_LIST = [(trial.ConfigObject())]

# location of the entire database run
unique_suffix = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
DB_DIR = os.path.join(
    os.getcwd(),
    "scratch/trial_{0}".format(unique_suffix)
)
homedir = "/root"


def generate_dir_name(db_dir, **kwargs):
    config_name = "_".join(
        ["{1}{0}".format(value, key) for key, value in kwargs.items()]
    )
    dir_name = os.path.join(db_dir, config_name)

    return dir_name


def clone(branch, host):
    cmd = "cd {0} " \
          "&& git clone https://github.com/jl3953/smdbrpc " \
          "&& git stash " \
          "&& git fetch origin {1} " \
          "&& git checkout {1}".format(homedir, branch)

    system_utils.call_remote(host, cmd)


def main():
    db_dir = DB_DIR
    files_to_process = os.path.join(
        db_dir, "configs_to_process.csv"
    )

    # create the database and table
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    # populate configs to process
    for cfg_obj in CONFIG_OBJ_LIST:
        cfg_fpath_list = cfg_obj.generate_all_config_files()
        data = [{
            constants.CONFIG_FPATH_KEY: cfg_fpath,
        } for cfg_fpath in cfg_fpath_list]
        csv_utils.append_data_to_file(data, files_to_process)

    # file of failed configs
    failed_configs_csv = os.path.join(db_dir, "failed_configs.csv")
    f = open(
        failed_configs_csv, "w"
    )  # make sure it's only the failures from this round
    f.close()

    # connect to db
    db = sqlite_helper_object.SQLiteHelperObject(
        os.path.join(db_dir, "trials.db")
    )
    db.connect()
    _, cfg_lt_tuples = csv_utils.read_in_data_as_tuples(
        files_to_process, has_header=False
    )

    for cfg_fpath in cfg_lt_tuples:
        # generate config object
        cfg = generate_configs.generate_configs_from_files_and_add_fields(
            cfg_fpath
        )

        # make directory in which trial will be run
        logs_dir = generate_dir_name(
            db_dir,
            read_percent=cfg["read_percent"],
            client_concurrency=cfg["client_concurrency"],
            server_concurrency=cfg["server_concurrency"],
        )

        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        # copy over config into directory
        for k, v in cfg:
            print(k, v)

        system_utils.call(
            "cp {0} {1}".format(
                cfg[constants.CONFIG_FPATH_KEY], logs_dir
            )
        )

        # clone smdbrpc repo on all hosts
        for n in cfg["clients"]:
            clone(cfg["client_branch"], n.ip)

    return 0


if __name__ == '__main__':
    sys.exit(main())

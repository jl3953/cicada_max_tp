import datetime
import itertools
import os

import config_io
import constants
import node


class ConfigObject:
    """Represents different combinations of configuration parameters."""

    def __init__(self):
        # clients
        self.clients = [
            [node.Node(2), node.Node(3), node.Node(4), node.Node(5)]]
        self.client_branch = ["maxTP"]
        self.client_concurrency = [8, 16]
        self.client_batch_size = [10]  # txns / rpc call
        self.keys_per_txn = [1]
        self.read_percent = [0, 95]  # in percent
        self.duration = [30]  # in seconds

        # servers
        self.servers = [[node.Node(12), node.Node(13), node.Node(14)]]
        self.server_branch = ["postDeadline"]
        self.server_concurrency = [4, 8, 15]
        self.server_batch_size = [5]  # txns / replication call

    def generate_config_combinations(self):
        temp_dict = vars(self)
        all_field_values = list(temp_dict.values())
        values_combinations = list(itertools.product(*all_field_values))

        combinations = []
        for combo in values_combinations:
            config_dict = dict(zip(temp_dict.keys(), combo))
            combinations.append(config_dict)

        return combinations

    def generate_all_config_files(self):
        """Generates all configuration files with different combinations of
        parameters.
    :return:
    """
        ini_fpaths = []
        config_combos = self.generate_config_combinations()
        for config_dict in config_combos:
            ini_fpath = ConfigObject.generate_ini_filename(
                suffix=config_dict["logs_dir"]
            )
            ini_fpaths.append(
                config_io.write_config_to_file(config_dict, ini_fpath)
            )

        return ini_fpaths

    @staticmethod
    def generate_ini_filename(suffix=None, custom_unique_prefix=None):
        """Generates a filename for ini using datetime as unique id.

    :param suffix: (str) suffix for human readability
    :param custom_unique_prefix: use a custom prefix. If none, use datetime.
    :return: (str) full filepath for config file
    """

        unique_prefix = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        if custom_unique_prefix:
            unique_prefix = custom_unique_prefix
        ini = unique_prefix + "_" + suffix + ".ini"
        return os.path.join(constants.TEST_CONFIG_PATH, ini)

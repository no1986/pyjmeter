import argparse

import pandas as pd
import yaml
from box import Box
from pyjmx import createJMX


def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-c",
        "--conf",
        type=str,
        required=True,
        metavar="CONF",
        help="URLなどの設定を記載したconfig.yaml",
    )
    ap.add_argument(
        "-l",
        "--load",
        type=str,
        required=True,
        metavar="LOAD",
        help="負荷変動を記載したload.csv",
    )
    ap.add_argument(
        "-o",
        "--output",
        type=str,
        default="test.jmx",
        metavar="OUTPUT",
        help="出力するアウトプットファイルのファイル名(default:test.jmx)",
    )
    return ap.parse_args()


def read_conf(conf_file):
    config = None
    with open(conf_file, "r") as f:
        config = Box(yaml.safe_load(f))
        pass
    return config


def main():
    args = get_args()
    conf = read_conf(args.conf)
    load = pd.read_csv(args.load)
    createJMX(conf.domain, conf.port, conf.path, conf.threads, load, args.output)
    return


if __name__ == "__main__":
    main()

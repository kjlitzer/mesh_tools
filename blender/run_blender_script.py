import argparse
import os
import subprocess
import sys


sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import Config as config


def main(args):
    cmd = [
        config.blender.path_to_blender,
        "--background",
        "--python",
        f"{args.script}",
        *args.script_args
    ]

    subprocess.run(cmd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start blender headless and execute script.")
    parser.add_argument("script", type=str)
    parser.add_argument("script_args", type=str, nargs="*")

    input_args = parser.parse_args()
    main(input_args)
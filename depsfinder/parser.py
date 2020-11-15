import argparse

parser = argparse.ArgumentParser(description='Calculate start/stop ordering of services')
parser.add_argument(
    'action', choices=['start', 'stop'],
    help="Whether to calculate start/stop ordering"
)
parser.add_argument('--file', '-f', required=True, help="File to use")

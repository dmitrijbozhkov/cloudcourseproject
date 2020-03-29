""" Application configuration """
from os.path import join, abspath, dirname
from yaml import load, Loader

config = None
try:
    with open(join(dirname(abspath(__file__)), "settings.yaml")) as f:
        config = load(f, Loader=Loader)
except FileNotFoundError:
    raise RuntimeError("settings.yaml was not found!")
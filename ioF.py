import os

from aiogram.utils.json import json


async def write_list(a_list, f_name):
    with open(f_name, "w") as fp:
        json.dump(a_list, fp)

    # Read list to memory if is not empty else returns emty list

def read_id(f_name):
    if not os.path.exists(f_name):
        f = open(f_name, "x")
        return 0
    if os.stat(f_name).st_size == 0:
        return 0
    with open(f_name, 'rb') as fp:
        n_list = json.load(fp)
        return n_list

def read_list(f_name):
    if not os.path.exists(f_name):
        f = open(f_name, "x")
        return {}
    if os.stat(f_name).st_size == 0:
        return {}
    with open(f_name, 'rb') as fp:
        n_list = json.load(fp)
        return n_list


def read_arr(f_name):
    if not os.path.exists(f_name):
        f = open(f_name, "x")
        return []
    if os.stat(f_name).st_size == 0:
        return []
    with open(f_name, 'rb') as fp:
        n_list = json.load(fp)
        return n_list
    # Read list to memory if is not empty else returns emty list


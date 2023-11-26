import os
from art import text2art


count_of_lines = 0

def _open_directory(__path: str):
    global count_of_lines

    for filename in os.listdir(__path):
        if os.path.isfile(f"{__path}/{filename}"):
            try:
                count_of_lines += len(open(f"{__path}/{filename}", "r").read().split("\n"))
            except:
                pass
        else:
            _open_directory(f"{__path}/{filename}")

_open_directory("source")
print(count_of_lines)
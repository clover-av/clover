# -*- coding: utf8 -*-
from core.interface.CloverInterface import CloverInterface
from core.settings import settings
import time, sys
import json

VERSION = "1.1"
NAME = "Clover AntiMalware"

def install():
    CloverInterface.clear([settings.pipe_path(2), settings.pipe_path()]) # clear old pipes

def main():
    gui = CloverInterface(NAME, settings.pipe_path(2), settings.setup_path()) # o out deve ser o in do monitor
    pipe_path = settings.pipe_path()

    while True:
        queue = read_blocks(pipe_path)
        processed = []
        for block in queue:
            block = json.loads(block)
            if block['type'] == 1:
                processed.append(block)
                gui.changed_key(block)
        # remove o itens ja processados da fila
        queue = read_blocks(pipe_path)
        pipe_back = open(pipe_path, "w")
        for block in queue:
            block = json.loads(block)
            if block not in processed:
                block = json.dumps(block)
                pipe_back.write(block + "\n")
        pipe_back.close()
        time.sleep(1)

def read_blocks(queue):
    try:
        pipe_back = open(queue, "r")
        queue = pipe_back.readlines()
        pipe_back.close()
        return queue
    except:
        return ''

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--install':
        install()
    else:
        main()
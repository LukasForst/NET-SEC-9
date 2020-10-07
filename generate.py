import logging
import string
import sys
import warnings

from main import sample, verify_passwords

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] - %(levelname)s - %(module)s: %(message)s',
                    stream=sys.stdout)


def run():
    alphabet = string.ascii_letters
    padding = '#'
    selected = []
    for _ in range(0, 1):
        pwd = ''.join(selected)

        possible_pwds = [pwd + letter + padding for letter in alphabet] * 15
        sampled = verify_passwords(possible_pwds, max_workers=10, sample_rounds=2)

        selected_pwd = max(sampled, key=sampled.get)
        selected.append(selected_pwd[-2])

        print(''.join(selected))


def sample_pwd(pwd: str, rounds: int = 20) -> int:
    pwd, mean = sample(pwd, rounds)
    return mean


if __name__ == '__main__':
    warnings.filterwarnings("ignore")

    run()

import logging
import string
import sys
import warnings
from typing import List

from main import sample, verify_passwords

warnings.filterwarnings("ignore")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] - %(levelname)s - %(module)s: %(message)s',
                    stream=sys.stdout)


def run():
    alphabet = string.ascii_lowercase
    padding = '#'
    selected = ['P']
    for _ in range(0, 2):
        pwd = ''.join(selected)

        possible_pwds = [pwd + letter + padding for letter in alphabet]
        print(possible_pwds)
        sampled = verify_passwords(possible_pwds, sample_rounds=7)

        selected_pwd = max(sampled, key=sampled.get)
        selected.append(selected_pwd[-2])

        print(''.join(selected))


def run_bunch():
    alphabet = string.ascii_lowercase
    # alphabet = ['a', 's', 'w']
    combs = ['P' + w + '#' for w in generate_combinations(alphabet, 1)]
    sampled = verify_passwords(combs, sample_rounds=5)
    selected_pwd = max(sampled, key=sampled.get)
    print(selected_pwd)


def generate_combinations(aph: List[str], count: int) -> List[str]:
    if count == 1:
        return aph

    previous_round = generate_combinations(aph, count - 1)
    return [w + a for a in aph for w in previous_round]


def sample_pwd(pwd: str, rounds: int = 20) -> int:
    pwd, mean = sample(pwd, rounds)
    return mean


if __name__ == '__main__':
    run()

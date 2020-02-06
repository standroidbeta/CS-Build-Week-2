import hashlib
import requests
from decouple import config
import json

from uuid import uuid4

from time import sleep

import random


api_key = config('DAKOTA_KEY')

headers = {
    'Authorization': api_key,
    'Content-Type': 'application/json'
}


def get_last_proof():
    response = requests.get('https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/', headers=headers)
    res = json.loads(response.text)
    print("Last Proof", res)
    return res


def proof_of_work(last_proof):
    last = last_proof['proof']
    difficulty = last_proof['difficulty']
    print("Searching for next proof")
    proof = random.randint(-9876543211, 9876543211)
    last_hash = hashlib.sha256(str(last).encode()).hexdigest()
    while valid_proof(last_hash, proof) is False:
        proof += 1

    print("Proof found: ", proof)
    new_proof = {"proof": int(proof)}
    response = requests.post('https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/', headers=headers, data=new_proof)
    print("Coin Mined?", response)
    res = json.loads(response.text)
    print(res)
    sleep(res['cooldown'])
    return res


def valid_proof(last_hash, proof):
    difficulty = last_proof['difficulty']
    guess = hashlib.sha256(str(proof).encode()).hexdigest()
    # guess_hash = hashlib.sha256(guess).hexdigest()
    return guess[:difficulty] == "0" * difficulty


if __name__ == '__main__':
    while True:
        last_proof = get_last_proof()
        sleep(last_proof['cooldown'])
        new_proof = proof_of_work(last_proof)

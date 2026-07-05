import uuid
import os
import random
import string

def generate_random_file():
    filename = str(uuid.uuid4()) + '.txt'
    with open(filename, 'w') as f:
        f.write(''.join(random.choice(string.ascii_lowercase) for _ in range(1024)))
    return filename

def check_file_presence(filename):
    return os.path.isfile(filename)

def census_voice():
    filename = generate_random_file()
    if check_file_presence(filename):
        print(f"File {filename} has been generated and is present.")
    else:
        print(f"File {filename} has not been generated or is not present.")
    os.remove(filename)

census_voice()
from redis import Redis
import yaml
import os

redis = Redis(host='redis', port=6379, db=0)


def upload_file(filename):
    with open(filename) as f:
        data = yaml.safe_load(f.read())
        for row in data.items():
            redis.set(*row)



def upload_translate_to_redis():
    directory = 'IotKernel/translate'
    for file in os.listdir(directory):
        if '.yaml' in file or '.yml' in file:
            print(file)
            upload_file(os.path.join(directory,file))

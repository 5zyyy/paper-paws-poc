import yaml

def write_yaml(path, content):
    with open(path, 'w') as file:
        yaml.dump(content, file)
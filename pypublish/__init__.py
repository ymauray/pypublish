import sys
import os
import yaml
import datetime
import requests

import pypublish.yamlreader
import pypublish.auphonic as auphonic

from pypublish import options, YAML

def name():
    return "PyPublish"

def version():
    return "0.1rc1"

def main():
    print("{} {}".format(name(), version()))

    try:
        opts = options.get_options(sys.argv)
    except Exception as e:
        print(e)
        sys.exit(2)

    if len(opts.args) != 1:
        print("No configuration file given.")
        sys.exit(2)
    
    yaml_file = opts.args[0]

    if not os.path.isfile(yaml_file):
        print("File not found: {}".format(yaml_file))
        sys.exit(2)

    try:
        parser = YAML.Parser()
        config = parser.load(yaml_file)
    except Exception as e:
        print(e)
        sys.exit(2)

    if config["year"] == "auto":
        config["year"] = datetime.datetime.now().strftime("%Y")

    if isinstance(config["image"], dict):
        if config["image"]["type"] == "tegh":
            params = (
                ('episode', config["episode"]),
                ('title', config["title"]),
            )
            requests.get('https://teaearlgreyhot.org/tools/test1.php', params=params)
            config["image"] = f"https://teaearlgreyhot.org/tools/output/tea_earl_grey_hot_{config['episode']}_thumbnail.jpg"

    print(config)

    pipeline = config['pipeline']
    del config['pipeline']
    for module in pipeline:
        if module['module'] == 'auphonic':
            auphonic.create_production(config, module)

if __name__ == '__main__':
    main()

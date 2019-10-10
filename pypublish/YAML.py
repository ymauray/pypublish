import yaml
import sys, os, re

class Parser(object):

    def __init__(self):
        self.__level = 0

    def load(self, yaml_file):
        dirname = os.path.abspath(os.path.dirname(yaml_file))
        with open(yaml_file) as stream:
                config = yaml.safe_load(stream)
                if config is not None:
                    config = self.__process_includes(config, dirname)
                    if self.__level == 0:
                        refconfig = None
                        while refconfig != config:
                            refconfig = config
                            config = self.__replace_tokens(config)
                return config

    def __replace_tokens(self, config):
        config = self.__replace_tokens_internal(config, config)
        return config

    def __replace_tokens_internal(self, value, config):
        if isinstance(value, dict):
            output = {}
            for k in list(value):
                v = value[k]
                output[k] = self.__replace_tokens_internal(v, config)
            return output
        elif isinstance(value, list):
            output = []
            for item in list(value):
                output.append(self.__replace_tokens_internal(item, config))
            return output
        elif isinstance(value, str):
            p = re.compile(r"\${([^}]+)}", re.IGNORECASE)
            m = p.search(value)
            if m:
                if isinstance(config[m.group(1)], str):
                    return value.replace(f"${{{m.group(1)}}}", config[m.group(1)])
                else:
                    return config[m.group(1)]
            else:
                return value
        elif isinstance(value, int):
            return value
        else:
            print(f"Unknown type {type(value)}")
            sys.exit()

    def __process_includes(self, config, dirname):
        output = {}
        for key in list(config):
            if key == 'include':
                for o in list(config[key]):
                    subparser = Parser()
                    subparser.__level = self.__level + 1
                    subconfig = subparser.load(f"{dirname}/{o['file']}")
                    if subconfig is not None:
                        output.update(subconfig)
            else:
                output[key] = config[key]

        return output

import yaml
import sys, os, re

class YAMLUtil(object):

    @staticmethod
    def load(yaml_file, level = 0):
        dirname = os.path.abspath(os.path.dirname(yaml_file))
        with open(yaml_file) as stream:
                config = yaml.safe_load(stream)
                config = YAMLUtil.process_includes(config, dirname, level)
                if level == 0:
                    refconfig = None
                    while refconfig != config:
                        refconfig = config
                        config = YAMLUtil.replace_tokens(config)
                return config

    @staticmethod
    def replace_tokens(config):
        config = YAMLUtil.replace_tokens_internal(config, config)
        return config

    @staticmethod
    def replace_tokens_internal(value, config):
        if isinstance(value, dict):
            output = {}
            for k in list(value):
                v = value[k]
                output[k] = YAMLUtil.replace_tokens_internal(v, config)
            return output
        elif isinstance(value, list):
            output = []
            for item in list(value):
                output.append(YAMLUtil.replace_tokens_internal(item, config))
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

    @staticmethod
    def process_includes(config, dirname, level):
        output = {}
        for key in list(config):
            if key == 'include':
                subconfig = YAMLUtil.load(f"{dirname}/{config[key]}", level + 1)
                output.update(subconfig)
            else:
                output[key] = config[key]

        return output

import yaml
import sys

class YAMLUtil(object):

    @staticmethod
    def load(yaml_file):
        with open(yaml_file) as stream:
                config = yaml.safe_load(stream)
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
            return value.replace("{{episode}}", config["episode"])
        elif isinstance(value, int):
            return value
        else:
            print(f"Unknown type {type(value)}")
            sys.exit()

import yaml

def replace_tokens(source, tokens):
    config = {}
    if isinstance(source, dict):
        for key in list(source):
            value = replace_tokens(source[key], tokens)
            config[replace_tokens(key, tokens)] = value
    elif isinstance(source, str):
        target = source
        for key in list(tokens):
            target = target.replace(f"{{{{{key}}}}}", tokens[key])
        return target
    elif isinstance(source, int):
        return source
    elif isinstance(source, list):
        target = []
        for item in source:
            target.append(replace_tokens(item, tokens))
        return target
    else:
        raise Exception("Unknown type : {}".format(type(source)))

    return config

def parse(yaml_file):
    with open(yaml_file) as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise

    tokens = {}
    tokens["track"] = config["track"]

    config = replace_tokens(config, tokens)
    for key in list(config):
        value = config[key]

    return config

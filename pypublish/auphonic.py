import requests
import json

headers = {
    'Content-Type': 'application/json',
}

def create_production(config, auphonic_config):
    json_data = {}
    json_data['multi_input_files'] = []
    files = {}

    for track in config['tracks']:
        input_file = {}
        input_file['type'] = 'multitrack'
        input_file['algorithms'] = {}
        input_file['id'] = track['file']

        if not 'type' in track:
            track['type'] = 'voice'

        track_type = track['type']
        if track_type == 'music':
            input_file['algorithms']['denoise'] = False
            input_file['algorithms']['hipfilter'] = False
            input_file['algorithms']['backforeground'] = 'foreground'
        else:
            input_file['algorithms']['denoise'] = True
            input_file['algorithms']['hipfilter'] = True
            input_file['algorithms']['backforeground'] = 'foreground'

        for key in list(track):
            value = track[key]
            if key == 'denoise':
                input_file['algorithms']['denoise'] = value
            elif key == 'hipfilter':
                input_file['algorithms']['hipfilter'] = value
            elif key == 'backforeground':
                input_file['algorithms']['backforeground'] = value
            elif key == 'duck':
                input_file['algorithms']['backforeground'] = 'ducking'

        files[input_file['id']] = (input_file['id'], open(input_file['id'], 'rb'))
        json_data['multi_input_files'].append(input_file)

    json_data['metadata'] = {}
    json_data['metadata']['title'] = config['title']
    json_data['metadata']['artist'] = config['author']
    json_data['metadata']['album'] = config['podcast']
    json_data['metadata']['track'] = config['episode']
    json_data['metadata']['genre'] = auphonic_config['genre']
    json_data['metadata']['year'] = config['year']
    json_data['metadata']['publisher'] = config['publisher']
    json_data['metadata']['url'] = config['url']
    json_data['metadata']['license'] = config['license']
    json_data['metadata']['license_url'] = config['license_url']

    json_data['output_basename'] = auphonic_config['output_basename']

    json_data['output_files'] = []
    for output_file in auphonic_config['output']:
        output = {}
        for attr in output_file:
            output[attr] = output_file[attr]
        json_data['output_files'].append(output)

    json_data['algorithms'] = {}
    json_data['algorithms']['leveler'] = auphonic_config['algorithms']['leveler']
    json_data['algorithms']['gate'] = auphonic_config['algorithms']['gate']
    json_data['algorithms']['loudnesstarget'] = auphonic_config['algorithms']['loudnesstarget']
    json_data['algorithms']['crossgate'] = auphonic_config['algorithms']['crossgate']

    json_data['image'] = config['image']

    data = json.dumps(json_data)
    print()
    print(data)

    response = requests.post('https://auphonic.com/api/productions.json', headers=headers, data=data, auth=('yannick@frenchguy.ch', 'Kxtj3YOxNGQs'))
    resp = response.json()
    print()
    print(resp)

    uuid = resp['data']['uuid']
    print(uuid)
    response = requests.post(f"https://auphonic.com/api/production/{uuid}/upload.json", files=files, auth=('yannick@frenchguy.ch', 'Kxtj3YOxNGQs'))
    print(response)

import yaml
import requests


def get_steles_index(base_url='https://github.com/mehmetoguzderin/tonqq/raw/master/steles/', map_url='steles.yaml'):
    get_steles_yaml = requests.get(base_url + map_url)
    steles_yaml = get_steles_yaml.text
    steles_index = yaml.safe_load(steles_yaml)
    for stele in steles_index['steles']:
        for face in steles_index['steles'][stele]['faces']:
            for line in steles_index['steles'][stele]['faces'][face]['lines']:
                steles_index['steles'][stele]['faces'][face]['lines'][line] = int(
                    steles_index['steles'][stele]['faces'][face]['lines'][line])
    return steles_index['steles']


def to_url(steles_index, stele, face, line, base_url='https://github.com/mehmetoguzderin/tonqq/raw/master/steles/'):
    return (base_url + format(int(stele), '01d') +
            '/faces/' + format(int(face), '01d') +
            '/lines/' + format(int(line), '02d') +
            '/inscriptions.yaml')


def get_inscriptions(steles_index, stele, face, line, base_url='https://github.com/mehmetoguzderin/tonqq/raw/master/steles/'):
    get_inscriptions_yaml = requests.get(
        to_url(steles_index, stele, face, line, base_url=base_url))
    inscriptions_yaml = get_inscriptions_yaml.text
    inscriptions = inscriptions_yaml.split('\n')[1:-1]
    for index, inscription in enumerate(inscriptions):
        split_tokens = inscription.split('"')[1]
        if len(split_tokens) > 1:
            inscriptions[index] = inscription.split('"')[1]
    return inscriptions


def get_line(steles_index, stele, face, line, base_url='https://github.com/mehmetoguzderin/tonqq/raw/master/steles/', end_token=u'\u200F'):
    return ''.join(get_inscriptions(steles_index, stele, face, line, base_url=base_url)) + end_token


def get_face(steles_index, stele, face, base_url='https://github.com/mehmetoguzderin/tonqq/raw/master/steles/', end_token=u'\u200F'):
    lines = []
    for line in steles_index[stele]['faces'][face]['lines'].keys():
        lines.append(get_line(steles_index, stele, face, line,
                              base_url=base_url, end_token=end_token))
    return lines


def get_stele(steles_index, stele, base_url='https://github.com/mehmetoguzderin/tonqq/raw/master/steles/', end_token=u'\u200F'):
    faces = []
    for face in steles_index[stele]['faces'].keys():
        faces.append(get_face(steles_index, stele, face,
                              base_url=base_url, end_token=end_token))
    return faces


def get_steles(steles_index, base_url='https://github.com/mehmetoguzderin/tonqq/raw/master/steles/', end_token=u'\u200F'):
    steles = []
    for stele in steles_index.keys():
        steles.append(get_stele(steles_index, stele,
                                base_url=base_url, end_token=end_token))
    return steles

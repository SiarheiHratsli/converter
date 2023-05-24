import argparse
import json

parser = argparse.ArgumentParser(description='Jest to program ktory sluzy do konwersji plikow json/yaml/xml')
parser.add_argument('indir', type=str, help='Input files')
parser.add_argument('outdir', type=str, help='Output files')
args = parser.parse_args()


def parsowanie(input_file):
    rozszerzenie = input_file.split('.')[-1].lower()
    if rozszerzenie == 'json':
        return pars_json(input_file)
    elif rozszerzenie == 'yaml' or rozszerzenie == 'yml':
        return pars_yaml(input_file)
    elif rozszerzenie == 'xml':
        return pars_xml(input_file)
    else:
        print(f'Takie rozszerzenie {rozszerzenie} nie jest obslugowane tym programem')
        print(f'Aby dowiedziec sie co robi ten program i jakie rozszerzenie są obslugowane '
              f'tym programem wpisz --help/-h')


def pars_json(input_file):
    try:
        with open(input_file, 'r') as file:
            data = json.load(file)

            text = convert_to_text(data)
        return text
    except FileNotFoundError:
        print(f'Nie znaleziono pliku {input_file}')
    except json.decoder.JSONDecodeError:
        print(f'Plik {input_file} ma złą składnie')


def pars_yaml(input_file):
    print('jest to plik z rozszerzeniem yaml')


def pars_xml(input_file):
    print('jest to plik z rozszerzeniem xml')


def convert_to_text(data):
    text = ''
    for key, value in data.items():
        text += f'{key}: {value}\n'
    return text

wczytany_tekst = parsowanie(args.indir)
print(wczytany_tekst)

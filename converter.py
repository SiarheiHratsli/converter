import argparse
import json
from benedict import benedict
import yaml
import xml.etree.ElementTree as ET
import xmltodict
import sys

print(f'''
Hej!
Jest to program ktory sluzy do konwersji plikow json/yaml/xml
Aby zacząc konwersje musisz podać dwa pliki (plik wejściowy) oraz (opik wyjsciowy)
Aby zobaczyc dodatkowe dane wpisz -h lub --help
''')
parser = argparse.ArgumentParser(description='Jest to program ktory sluzy do konwersji plikow json/yaml/xml')
parser.add_argument('indir', type=str, help='Input files')
parser.add_argument('outdir', type=str, help='Output files')
try:
    args = parser.parse_args()
except SystemExit:
    print('Nie podales wymaganych argumentow')
    sys.exit()



def parsowanie(input_file):
    try:
        rozszerzenie = input_file.split('.')[-1].lower()
        if rozszerzenie == 'json':
            return pars_json(input_file)
        elif rozszerzenie == 'yaml' or rozszerzenie == 'yml':
            return pars_yaml(input_file)
        elif rozszerzenie == 'xml':
            return pars_xml(input_file)
        else:
            print(f'Takie rozszerzenie {rozszerzenie} nie jest obslugowane tym programem')
            print(f'Aby dowiedziec sie co robi ten program i jakie '
                  f'rozszerzenie są obslugowane tym programem wpisz --help/-h')
            sys.exit()
    except FileNotFoundError:
        print(f'Nie znaleziono pliku {input_file}')
        sys.exit()


def zapisanie(output_file, text, input_file):
    try:
        rozszerzenie = output_file.split('.')[-1].lower()
        if rozszerzenie == 'json':
            return zapis_json(output_file, text)
        elif rozszerzenie == 'yaml' or rozszerzenie == 'yml':
            return zapis_yaml(output_file, text)
        elif rozszerzenie == 'xml':
            return zapis_xml(output_file, text)
        else:
            print(f'Takie rozszerzenie {rozszerzenie} nie jest obslugowane tym programem')
            print(f'Aby dowiedziec sie co robi ten program i jakie rozszerzenie '
                  f'są obslugowane tym programem wpisz --help/-h')
            sys.exit()
    except TypeError:
        print(f'Nie znaleziono pliku {input_file}')
        sys.exit()


def pars_json(input_file):
    try:
        with open(input_file, 'r') as file:
            data = json.load(file)

        return data
    except json.decoder.JSONDecodeError:
        print(f'Plik {input_file} ma złą składnie')


def zapis_json(output_file, text):
    try:
        with open(output_file, 'w') as file:
            file.write(benedict(text).to_json())
        print(f'Zapisano plik {output_file}')
    except IOError:
        print(f'Nie udało się zapisać pliku {output_file}')


def pars_yaml(input_file):
    try:
        with open(input_file, 'r') as file:
            data = yaml.safe_load(file)

        return data
    except yaml.YAMLError:
        print(f'Plik {input_file} ma złą składnie')


def zapis_yaml(output_file, text):
    try:
        with open(output_file, 'w') as file:
            file.write(benedict(text).to_yaml())
        print(f'Zapisano plik {output_file}')
    except IOError:
        print(f'Nie udało się zapisać pliku {output_file}')


def pars_xml(input_file):
    try:
        text = {}
        ET.parse(input_file)

        tree = ET.parse(input_file)
        root = tree.getroot()

        for element in root.iter():
            if element.tag != root.tag:
                text[element.tag] = element.text
        return text
    except ET.ParseError:
        print(f'Plik {input_file} ma złą składnie')


def zapis_xml(output_file, text):
    try:
        data = {
            'root': text
        }

        with open(output_file, 'w') as file:
            xmltodict.unparse(data, output=file, pretty=True)
        print(f'Zapisano plik {output_file}')
    except IOError:
        print(f'Nie udało się zapisać pliku {output_file}')


wczytanyTekst = parsowanie(args.indir)
print(zapisanie(args.outdir, wczytanyTekst, args.indir))

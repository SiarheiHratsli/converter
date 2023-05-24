import argparse

parser = argparse.ArgumentParser(description='Jest to program ktory sluzy do konwersji plikow json/yaml/xml')
parser.add_argument('indir', type=str, help='Input files')
parser.add_argument('outdir', type=str, help='Output files')
args = parser.parse_args()


def parsowanie(input_file):
    rozszerzenie = input_file.split('.')[-1].lower()
    if rozszerzenie == 'json':
        pars_json(input_file)
    elif rozszerzenie == 'yaml' or rozszerzenie == 'yml':
        pars_yaml(input_file)
    elif rozszerzenie == 'xml':
        pars_xml(input_file)
    else:
        print(f'Takie rozszerzenie {rozszerzenie} nie jest obslugowane tym programem')
        print(f'Aby dowiedziec sie co robi ten program i jakie rozszerzenie są obslugowane '
              f'tym programem wpisz --help/-h')


def pars_json(input_file):
    print('jest to plik z rozszerzeniem json')


def pars_yaml(input_file):
    print('jest to plik z rozszerzeniem yaml')


def pars_xml(input_file):
    print('jest to plik z rozszerzeniem xml')

print(parsowanie(args.indir))

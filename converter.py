from tkinter import *
from tkinter import filedialog as fd
import json
import yaml
import xml.etree.ElementTree as ET
import xmltodict
from tkinter import messagebox


# wyłołanie głównego okna
root = Tk()
root.title('Converter')
root.geometry('500x160+300+200')
root.resizable(False, False)


def parsowanie(input_file_pars):
    try:
        rozszerzenie = input_file_pars.split('.')[-1].lower()
        if rozszerzenie == 'json':
            return pars_json(input_file_pars)
        elif rozszerzenie == 'yaml' or rozszerzenie == 'yml':
            return pars_yaml(input_file_pars)
        elif rozszerzenie == 'xml':
            return pars_xml(input_file_pars)
        else:
            open('error.txt', 'w').write(f'Such extension {rozszerzenie} is not supported with this program')
            handle_error()
    except FileNotFoundError:
        open('error.txt', 'w').write(f'File not found {input_file_pars}')
        handle_error()


def zapisanie(output_file_zapis, text_zapis):
    rozszerzenie = output_file_zapis.split('.')[-1].lower()
    if rozszerzenie == 'json':
        return zapis_json(output_file_zapis, text_zapis)
    elif rozszerzenie == 'yaml' or rozszerzenie == 'yml':
        return zapis_yaml(output_file_zapis, text_zapis)
    elif rozszerzenie == 'xml':
        return zapis_xml(output_file_zapis, text_zapis)


def pars_json(input_file_json):
    try:
        with open(input_file_json, 'r') as file:
            data = json.load(file)

        return data
    except json.decoder.JSONDecodeError:
        open('error.txt', 'w').write(f'File {input_file_json} has bad syntax')
        handle_error()


def zapis_json(output_file_json, text_json):
    try:
        text_json = json.dumps(text_json)
        with open(output_file_json, 'w') as file:
            file.write(text_json)
        complete()
    except IOError:
        open('error.txt', 'w').write(f'Failed to save file {output_file_json}')
        handle_error()


def pars_yaml(input_file_yaml):
    try:
        with open(input_file_yaml, 'r') as file:
            data = yaml.safe_load(file)

        return data
    except yaml.YAMLError:
        open('error.txt', 'w').write(f'File {input_file_yaml} has bad syntax')
        handle_error()


def zapis_yaml(output_file_json, text_yaml):
    try:
        text_yaml = yaml.dump(text_yaml)
        with open(output_file_json, 'w') as file:
            file.write(text_yaml)
        complete()
    except IOError:
        open('error.txt', 'w').write(f'Failed to save file {output_file_json}')
        handle_error()


def pars_xml(input_file_xml):
    try:
        text_x = {}
        ET.parse(input_file_xml)

        tree = ET.parse(input_file_xml)
        root_x = tree.getroot()

        for element in root_x.iter():
            if element.tag != root_x.tag:
                text_x[element.tag] = element.text
        return text_x
    except ET.ParseError:
        open('error.txt', 'w').write(f'File {input_file_xml} has bad syntax')
        handle_error()


def zapis_xml(output_file_xml, text_xml):
    try:
        data = {'root': text_xml}

        with open(output_file_xml, 'w') as file:
            xmltodict.unparse(data, output=file, pretty=True)
        complete()
    except IOError:
        open('error.txt', 'w').write(f'Failed to save file {output_file_xml}')
        handle_error()


# ERROR window
def handle_error():
    messagebox.showerror("ERROR", open('error.txt', 'r').read())


# complete window
def complete():
    messagebox.showinfo("Complete", 'Complete')


# funckja help
def help_funktion():
    help_window = Toplevel(root)
    help_window.title('Help')
    help_window.geometry('410x80+350+250')
    help_window.resizable(False, False)
    text_help = Label(help_window, text=f'''Hello, this program converts JSON, YAML and XML files.
Choose the input file and output format, then start the conversion.

Contact: hratsli.s@gmail.com''')
    text_help.place(x=0, y=0)


# button help
button_help = Button(root, text='Help', command=help_funktion)
button_help.place(x=435, y=130)

# pole dla podania nazwy pliku wyjsciowego
text = Label(root, text='Enter name')
text.place(x=110, y=80)
entry = Entry(root)
entry.place(x=192, y=80, width=100)


# funkcji dla przycisków
def file_selection():
    name = fd.askopenfilename()
    line_0.config(state='normal')
    line_0.delete(0, END)
    line_0.insert(0, name)
    line_0.config(state='readonly')


# linijka wyboru pllika
line_0 = Entry(root, width=40, state='readonly')
line_0.place(x=120, y=11)

json_var = IntVar()
yaml_var = IntVar()
xml_var = IntVar()


def konwertuj():
    input_file_konwert = line_0.get()
    output_file_konwert = entry.get()

    # sprawdzenie pliku wejsciowego
    if input_file_konwert == '':
        open('error.txt', 'w').write('Specify the name of the input file')
        handle_error()
        return

    # sprawdzenie checkboksów
    elif json_var.get() + yaml_var.get() + xml_var.get() == 0:
        open('error.txt', 'w').write('Select conversion format')
        handle_error()
        return

    # sprawdzenie pliku wyjsciowego
    elif output_file_konwert == '':
        open('error.txt', 'w').write('Specify the name of the output file')
        handle_error()
        return

    elif json_var.get() == 1:
        output_file_konwert += '.json'
    elif yaml_var.get() == 1:
        output_file_konwert += '.yaml'
    elif xml_var.get() == 1:
        output_file_konwert += '.xml'
    wczytany_tekst = parsowanie(input_file_konwert)
    zapisanie(output_file_konwert, wczytany_tekst)


# button
button_1 = Button(root, text='Select file', command=file_selection)
button_1.place(x=10, y=10)
button_2 = Button(root, text='Convert', command=lambda: konwertuj())
button_2.place(x=200, y=110)


# wybor pliku wyjsciowego
checkbox1 = Checkbutton(root, text='json', variable=json_var)
checkbox2 = Checkbutton(root, text='jaml', variable=yaml_var)
checkbox3 = Checkbutton(root, text='xml', variable=xml_var)

checkbox1.place(x=250, y=50)
checkbox2.place(x=310, y=50)
checkbox3.place(x=370, y=50)

# text
text = Label(root, text='Select the format of the resulting file')
text.place(x=10, y=50)

root.mainloop()

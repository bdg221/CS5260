#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import annotations
import csv, os, re


# read_csv is a utility to read and parse the initial CSV files
# code by John Ford

def read_csv(file_path: str) -> dict[dict]:
    entries = {}
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        csvFile = csv.DictReader(file)
        for entry in csvFile:
            entries[entry[list(entry.keys())[0]]] = entry
    return entries


# init_state method takes the initial state file and returns a
# dictionary of dictionaries
def init_state(file_path: str) -> dict[dict]:
    return read_csv(file_path)


def init_resources(file_path: str) -> dict[dict]:
    return read_csv(file_path)


def init_transforms(folder_path: str) -> dict[dict]:
    # read from folder file_path and loop through template files
    # add each template file to the rules dict[dict]
    transforms = {}
    for x in os.listdir(folder_path):
        if x.endswith(".tmpl"):
            temp = parse(folder_path+"/"+x)
            transforms[temp['name']] = temp
    return transforms


# code by John Ford to read in template files
# modified to use dictionaries instead of the dataclass
def read_file(file_path: str) -> str:
    file_contents = None
    with open(file_path, mode='r') as file:
        file_contents = file.read()
    return file_contents


def validate_nonempty(template: str = "") -> bool:
    return template != ""


def validate_enclosed(template: str = "") -> bool:
    left_paren_count = template.count("(")
    right_paren_count = template.count(")")
    if left_paren_count != right_paren_count:
        return False
    return True


def validate_keywords(template: str = "") -> bool:
    transform_keywords = ["TRANSFORM", "INPUTS", "OUTPUTS"]
    for keyword in transform_keywords:
        if not keyword in template:
            return False
    return True


def validate(template: str = ""):
    if not validate_nonempty(template):
        raise Exception("Empty template")
    if not validate_enclosed(template):
        raise Exception("Incorrect parentheses counts, verify all expressions are properly enclosed")
    elif not validate_keywords(template):
        raise Exception("Missing required keywords, verify transform is syntactically correct")


def build_resource_quantities(resource_quantities_block) -> [dict]:
    quantities = []

    regex = r"\(([A-Za-z]+) (\d)\)"
    matches = re.finditer(regex, resource_quantities_block, re.MULTILINE)
    for match in matches:
        resource_name, resource_quantity = match.groups()
        quantities.append({'name': resource_name,
                           'quantity': int(resource_quantity)})

    return quantities


def build_transform_template(template_path: str, template: str) -> dict:
    transform = {'name': '',
                 'inputs': [dict],
                 'outputs': [dict]
                 }
    basename = os.path.basename(template_path)
    transform_name = os.path.splitext(basename)[0]
    transform['name'] = transform_name

    inputs_start = template.index("INPUTS")
    outputs_start = template.index("OUTPUTS")

    inputs_string = template[inputs_start:outputs_start]
    outputs_string = template[outputs_start:]

    transform['inputs'] = build_resource_quantities(inputs_string)
    transform['outputs'] = build_resource_quantities(outputs_string)

    return transform


def parse(template_path: str) -> dict:
    template = read_file(template_path)
    validate(template)
    transform_template = build_transform_template(template_path, template)
    return transform_template

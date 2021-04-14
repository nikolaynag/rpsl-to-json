#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
from collections import OrderedDict
import json


if sys.version_info < (3, 3):
    sys.stderr.write(
        "Sorry, this script could not run with Python {}.{}, "
        "Python 3.3 or higher is required\n".format(*sys.version_info))
    sys.exit(1)


def print_object(obj):
    values = OrderedDict()
    for name in obj:
        if len(obj[name]) == 1:
            values[name] = obj[name][0]
        else:
            values[name] = obj[name]
    print(json.dumps(values))


def main():
    input = io.TextIOWrapper(sys.stdin.buffer, encoding='ISO-8859-1')
    current_object = None
    current_attr_name = None
    line_num = 0
    for line in input:
        line_num += 1
        line = line[:-1]  # remove trailing newline
        try:
            if line.startswith("%") or line.startswith("#"):
                continue
            # empty line - end of object or empty space
            if not line:
                if current_object is not None:
                    print_object(current_object)
                    current_object = None
                    current_attr_name = None
                continue
            payload, _, _ = line.partition("#")  # remove trailing comments
            if payload[0] in " \t+":
                # multi-line attribute value
                if current_attr_name is None:
                    raise ValueError("continuation without active attr")
                current_object[current_attr_name][-1] += payload[1:].lstrip()
                continue
            name, delim, value = payload.partition(":")
            if delim != ':':
                # if line is not comment, is not empty and does not start with
                # whitespace or '+' - it should contain attribute name and ':'
                raise ValueError("':' expected but not found")
            value = value.lstrip()
            if current_object is None:
                current_object = OrderedDict()
                current_object["class"] = name
                current_attr_name = name
                current_object[current_attr_name] = [value]
                continue
            values = current_object.get(name, [])
            values.append(value)
            current_object[name] = values
            current_attr_name = name
        except Exception as E:
            sys.stdout.write(
                "Error at line[{}]: '{}'\n".format(line_num, line)
            )
            raise E


if __name__ == '__main__':
    main()

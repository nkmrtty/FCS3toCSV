import sys
import re
import os
import os.path
from struct import unpack

key_fromat = re.compile("^\$[a-zA-Z0-9]+")

name_label_format = "$P{0}N"
name_label_format_short = "$P{0}S"

# data_format[datatype][datasize] = format character
data_format = {
    "I": {16: "H", 32: "I"},
    "F": {32: "f", 64: "d"},
    "D": {64: "d"}
}


def error(message, e):
    print("Error: {0}".format(message))
    print(e)
    sys.exit()


def read_fcs(fpath):
    fpath = os.path.abspath(fpath)
    indir, fname = os.path.split(fpath)
    os.chdir(indir)

    raw_str = bytes()
    with open(fname, "r+b") as fp:
        for line in fp:
            raw_str += line

    return raw_str, indir, os.path.splitext(fname)[0]


def extract_header(raw_str, offset=(0, 58)):
    # get header slice from fcs raw string
    header_str = raw_str[offset[0]:offset[1]].decode("utf-8")

    # start parsing
    header = {}

    # version
    header["version"] = header_str[0:6]
    if header["version"] != "FCS3.0":
        error("invalid file format", None)

    # offset
    try:
        header["offset_text"] = \
            (int(header_str[10:18]), int(header_str[18:26])+1)
        header["offset_data"] = \
            (int(header_str[26:34]), int(header_str[34:42])+1)
        header["offset_analysis"] = \
            (int(header_str[42:50]), int(header_str[50:58])+1)
    except ValueError as e:
        error("invalid file format", e)

    return header


def extract_text_segment(raw_str, offset):
    # get text segment slice from fcs raw string
    text_str = raw_str[offset[0]:offset[1]].decode("utf-8")

    # the first character is delimiter (ex. /)
    delimiter = text_str[0]

    # escape
    escaped_delimiter = re.compile(delimiter*2)
    text_str = escaped_delimiter.sub("\x01", text_str)

    # start parse
    text = {}
    row = text_str[1:len(text)-1].split(delimiter)
    itr = 0
    while itr < len(row):
        if key_fromat.match(row[itr]):
            key, value = row[itr:itr+2]
            text[key] = value.replace("\x01", delimiter)
            itr += 2
        else:
            itr += 1

    return text


def check_text_segment(text):
    try:
        # number of parameters
        par = int(text["$PAR"])

        # name label of parameters
        name_label = []
        if "$P1N" in text:
            # long name label
            for i in range(1, par+1):
                name_label.append(text[name_label_format.format(i)])
        else:
            for i in range(1, par+1):
                name_label.append(text[name_label_format_short.format(i)])

        # endian
        if text["$BYTEORD"] == "1,2,3,4":
            # little endian
            endian = "<"
        else:
            # big endian
            endian = ">"

        # data type
        dtype = data_format[text["$DATATYPE"]][int(text["$P1B"])]

        # record format
        record_fmt = endian + dtype * par

        # record length
        record_len = int(int(text["$P1B"]) / 8 * par)
    except (KeyError, ValueError) as e:
        error("text segment is invalid format", e)
    return name_label, record_fmt, record_len


def extract_data_segment(raw_str, offset, format, length):
    # get data segment
    data_str = raw_str[offset[0]:offset[1]]
    # start parse
    data = []
    for itr in range(0, len(data_str), length):
        record_str = data_str[itr: itr+length]
        record = unpack(format, record_str)
        data.append(record)
    return data


def save_csv(outdir, fname, name_label, data):
    # check working direcroty
    os.chdir(outdir)
    # save file
    fpath = os.path.join(outdir, fname+".csv")
    with open(fpath, "w") as fp:
        # name label
        line = ",".join(name_label)
        fp.write(line + "\n")
        # data
        for record in data:
            line = ",".join(map(str, record))
            fp.write(line + "\n")
    return


def run(infpath):
    print("START: {0}".format(infpath))
    print("> Read FCS file".format(infpath))
    raw_str, indir, fname = read_fcs(infpath)
    print("> Get header segment")
    header = extract_header(raw_str)
    print("> Get text segment")
    text = extract_text_segment(raw_str, header["offset_text"])
    name_label, record_fmt, record_len = check_text_segment(text)
    print("> Get data segment")
    data = extract_data_segment(
        raw_str, header["offset_data"], record_fmt, record_len
    )
    print("> Save CSV file")
    save_csv(indir, fname, name_label, data)
    print("END")

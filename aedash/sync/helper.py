
import csv
import os

import aedash.sync.error

def open_file(name, mode, buffering = -1):
    '''
    :type name: str
    :type mode: str
    :type buffering: int
    '''
    try:
        return open(name, mode, buffering)
    except IOError as e:
        raise aedash.sync.error.AssertionException(str(e))

def normalize_string(string_value):
    '''
    :type string_value: str
    '''
    return string_value.strip().lower() if string_value != None else None    
    
def guess_delimiter_from_filename(filename):
    '''
    :type filename
    :rtype str
    '''
    _base_name, extension = os.path.os.path.splitext(filename)
    normalized_extension = normalize_string(extension)
    if (normalized_extension == '.csv'):
        return ','
    if (normalized_extension == '.tsv'):
        return '\t'
    return '\t'

def iter_csv_rows(file_path, delimiter = None, recognized_column_names = None, logger = None):
    '''
    :type file_path: str
    :type delimiter: str
    :type recognized_column_names: list(str)
    :type logger: logging.Logger
    '''
    with open_file(file_path, 'r', 1) as input_file:
        if (delimiter == None):
            delimiter = guess_delimiter_from_filename(file_path)
        reader = csv.DictReader(input_file, delimiter = delimiter)

        if (recognized_column_names != None):
            unrecognized_column_names = [column_name for column_name in reader.fieldnames if column_name not in recognized_column_names] 
            if (len(unrecognized_column_names) > 0 and logger != None):
                logger.warn("Unrecognized column names: %s", unrecognized_column_names)

        for row in reader:
            yield row
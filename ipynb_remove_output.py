"""
Jupyter notebook could be good for educational purpose.
Before release in class, output generated during testing and execution number need to be removed.
"""

import os
import sys

import nbformat


# Use this module to read or write notebook files as particular nbformat versions.

def read_file(nb_filename):
    assert os.path.exists(nb_filename)

    txt = ''

    with open(nb_filename, 'rb') as nb_file:
        txt = nb_file.read()

    nb_node = nbformat.reads(txt.decode(), nbformat.NO_CONVERT)

    return nb_node


def process_nb_node(nb_node):
    for cell in nb_node['cells']:
        remove_cell_output(cell)

    return nb_node


def has_symbol(cell):
    """
     if symbol definition line included, return the line numbers and the contents in a list

    :param nbformat.notebooknode.NotebookNode cell:
    :return: list of tuple([line_number, line_content])
    """
    result = []
    if 'code' == cell['cell_type']:
        if 'source' in cell:
            for k, source_line in enumerate(cell['source'].splitlines()):
                if ('sy.symbols' in source_line) or ('sy.Symbol' in source_line):
                    result.append((k, source_line))

    return result


def remove_cell_output(cell):
    if 'code' == cell['cell_type']:
        if 'outputs' in cell:
            cell['outputs'] = []
        if 'execution_count' in cell:
            cell['execution_count'] = None


def write_file(nb_node, nb_filename):
    nbformat.write(nb_node, nb_filename)


def process_nb_file(nb_filename):
    nb_node = read_file(nb_filename)

    processed_node = process_nb_node(nb_node)

    write_file(processed_node, nb_filename)


if __name__ == '__main__':

    def main(argv):
        if 1 < len(argv):
            filename = argv[1]
            process_nb_file(filename)
        else:
            print("Usage : python %s <notebook file path>" % os.path.split(__file__)[-1])
            help(nbformat)


    main(sys.argv)

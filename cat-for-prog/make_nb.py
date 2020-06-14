'''
will prob use this:
https://pypi.org/project/ipynb-py-convert/

'''
import sys
import nbformat
from nbformat.v4 import new_notebook, new_code_cell

nb = new_notebook()
with open(sys.argv[1]) as f:
    code = f.read()

nb.cells.append(new_code_cell(code))
nbformat.write(nb, sys.argv[1]+'.ipynb')

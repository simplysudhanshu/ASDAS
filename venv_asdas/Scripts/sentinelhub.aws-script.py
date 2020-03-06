#!D:\Sudhanshu\pycharm\venv_asdas\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'sentinelhub==3.0.0b1','console_scripts','sentinelhub.aws'
__requires__ = 'sentinelhub==3.0.0b1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('sentinelhub==3.0.0b1', 'console_scripts', 'sentinelhub.aws')()
    )

from datetime import datetime
import os
import sys
import json
from warnings import warn
import logging

def debug_logger(level=logging.NOTSET):
    logger = logging.getLogger(__name__)
    FORMAT = "[%(asctime)s][%(filename)s:%(lineno)s][%(funcName)20s()] %(message)s"
    logging.basicConfig(format=FORMAT)
    logger.setLevel(level)
    return logger


def frozen_check():
    '''
    Checks the running script to see if it is compiled to a single exe.
    If compiled, the resources will be stored in a temp folder.
    If not, then they will be in the script's working directory.
    '''
    if getattr(sys, 'frozen', False):
    # Running in a bundle
        bundle_dir = sys._MEIPASS # pylint: disable=no-member
    else:
    # Running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
    return bundle_dir
def debug_dump_variables(obj):
    """
    Dumps variables of provided object to a log file.
    """
    if not hasattr(obj, 'dump_logger'):
        if hasattr(obj, 'batch_folder'):
            root = obj.batch_folder
        else:
            root = os.getcwd()
        obj.dump_logger = obj.setup_logger('Debug Dump', log_file='Debug_Dump', root_dir=root)
    obj.dump_logger.debug(f"Dumping variables for {type(obj.__name__)}:")
    for k, v in vars(obj).items():
        obj.debug_logger.debug(k, v)
        obj.dump_logger.debug(f'{k} : {v}')

def get_case_insensitive_key_value(input_dict, key):
    return next((value for dict_key, value in input_dict.items() if dict_key.lower() == key.lower()), None)

def create_batch_folder(root='', batch_code=None, include_time=False, test=False):
    """
    Used to set up a batch folder to store any log files or screenshots during an automation run.
    
    Parameters:
    - root: The root directory where the batch folder will be created.
    - batch_code: Optional batch code to use instead of generated one.
    - include_time: If True, appends the current time to the batch code.
    - test: If True, uses 'TEST' for the batch folder path; otherwise, uses 'PROD'.

    Returns:
    - The path to the created batch folder.
    """
    if batch_code and include_time:
        warn('batch_code and time arguments are not supported together. Ignoring time argument.')
        include_time = False

    db = 'TEST' if test else 'PROD'
    now = datetime.now()
    b_code = batch_code or now.strftime('%Y%m%d')
    b_time = now.strftime('%H%M')
    folder_name = f'{b_code}_{b_time}' if include_time else b_code
    batch_folder = os.path.join(root, 'batch_codes', db, folder_name)
    os.makedirs(batch_folder, exist_ok=True)
    return batch_folder
def setup_logger(name, log_file='log.log', file_format='DAILY',
                     level=logging.DEBUG, formatter=None, root_dir=None):
    """
    To setup as many loggers as you want.

    The log file name will have the date pre-pended to whatever is added as the
    log file name

    Default formatter %(asctime)s - %(name)s - %(levelname)s - %(message)s
    """
    if formatter == None:
        formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    _name = str(name)
    _file_format = str(file_format).upper()
    today = datetime.now()
    _formatter = logging.Formatter(formatter)
    if _file_format == 'DAILY':
        log_date = today.strftime("%Y_%m_%d_")
    elif _file_format == 'MONTHLY':
        log_date = today.strftime("%Y_%m_")
    else:
        log_date = ''
    _log_file = log_date + log_file
    if root_dir:
        _log_file = os.path.join(root_dir, _log_file)
    handler = logging.FileHandler(_log_file, mode='a', encoding='utf-8')
    handler.setFormatter(_formatter)
    logger = logging.getLogger(_name)
    logger.setLevel(level)
    if not logger.hasHandlers():
        logger.addHandler(handler)
    return logger

def read_updated(in_file):
    updated_records = []
    if os.path.exists(in_file):
        with open(in_file, 'r', encoding='utf-8') as f:
            updated_records = json.load(f)
    return updated_records or []

def save_updated(in_file, dict):
    with open(in_file, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(dict, indent=4))

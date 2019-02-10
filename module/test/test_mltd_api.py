import pytest
import tempfile
import os
import json
import module.mltd_api as mltd_api
from module.get_cfg import get_setting_cfg
from shutil import copyfile
from glob import glob

def setup_module(module):
    temp_folder = tempfile.gettempdir()
    for f in glob(os.path.join('data', '*')):
        copyfile(f, os.path.join(temp_folder, os.path.basename(f)))
    for f in glob(os.path.join('module/test/test_data', '*')):
        copyfile(f, os.path.join('data', os.path.basename(f)))
    
def teardown_module(module):
    temp_folder = tempfile.gettempdir()
    for f in glob(os.path.join('data', '*')):
        copyfile(os.path.join(temp_folder, os.path.basename(f)), f)

def test_validate_event_id_1():
    test_id = '55'
    mltd_api.validate_event_id(test_id)

def test_validate_event_id_2():
    test_id = 'qweqe'
    with pytest.raises(Exception):
        mltd_api.validate_event_id(test_id)

def test_validate_event_id_3():
    test_id = ''
    with pytest.raises(Exception):
        mltd_api.validate_event_id(test_id)

def test_get_last_event_id():
    assert mltd_api.get_last_event_id() == '2'

def test_get_event_id_1():
    assert mltd_api.get_event_id('FAKE EVENT') == '1'
    assert mltd_api.get_event_id('FAKE EVENT2') == '2'

def test_get_event_id_2():
    assert mltd_api.get_event_id('not found') == None

def test_is_event_has_rank():
    assert mltd_api.is_event_has_rank('1')
    assert not mltd_api.is_event_has_rank('2')

def test_calculate_speed_1():
    speed_dict = mltd_api.calculate_speed('1', 'hour')
    assert speed_dict['2500'] == 2400
    assert speed_dict['5000'] == 1200
    assert speed_dict['10000'] == 600

def test_calculate_speed_2():
    speed_dict = mltd_api.calculate_speed('1', 'half_hour')
    assert speed_dict['2500'] == 1200
    assert speed_dict['5000'] == 600
    assert speed_dict['10000'] == 300

def test_calculate_speed_3():
    speed_dict = mltd_api.calculate_speed('1', 'quarter_hour')
    assert speed_dict['2500'] == 600
    assert speed_dict['5000'] == 300
    assert speed_dict['10000'] == 150

def test_calculate_speed_4():
    speed_dict = mltd_api.calculate_speed('1', 'min')
    assert speed_dict['2500'] == 40
    assert speed_dict['5000'] == 20
    assert speed_dict['10000'] == 10



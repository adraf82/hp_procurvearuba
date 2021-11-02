from hp_procurvearuba import HP
import yaml
import pytest
import mock

with open('devices.yml', 'r') as f:
    device_data = yaml.safe_load(f)
    device_data = device_data.pop('devices')
    device_data = device_data

#pytest fixture for test_mocks.py
@pytest.fixture(scope='module')
def mocked_hp_connect():
    for device in device_data:
        hp_obj = HP(**device)
    return mock.Mock(spec=hp_obj)

#pyest fixture for test_funcs.py
@pytest.fixture(scope='module')
def hp_connect(request):
    for device in device_data:
        hp_obj = HP(**device)

    def fin():
        hp_obj.disconnect()

    request.addfinalizer(fin)
    return hp_obj

def test_mock_find_stp_mode(mocked_hp_connect):
    mocked_hp_connect.find_stp_mode.return_value = 'STP-compatible'
    assert 'STP-compatible' == mocked_hp_connect.find_stp_mode.return_value

def test_mock_find_rstp_mode(mocked_hp_connect):
    mocked_hp_connect.find_stp_mode.return_value = 'RSTP'
    assert 'RSTP' == mocked_hp_connect.find_stp_mode.return_value

def test_mock_find_rpvst_mode(mocked_hp_connect):
    mocked_hp_connect.find_stp_mode.return_value = 'RPVST'
    assert 'RPVST' == mocked_hp_connect.find_stp_mode.return_value

def test_mock_find_mstp_mode(mocked_hp_connect):
    mocked_hp_connect.find_stp_mode.return_value = 'MSTP'
    assert 'MSTP' == mocked_hp_connect.find_stp_mode.return_value

def test_mock_find_stp_status(mocked_hp_connect):
    mocked_hp_connect.find_stp_status.return_value = 'NO'
    assert 'NO' == mocked_hp_connect.find_stp_status.return_value

def test_mock_find_vlan(mocked_hp_connect):
    mocked_hp_connect.find_vlan.return_value = '300'
    assert '300' == mocked_hp_connect.find_vlan.return_value

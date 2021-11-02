def test_find_rpvst_mode(hp_connect, capsys):
    hp_connect.find_stp_mode()
    captured = capsys.readouterr()
    assert 'RPVST' in captured.out

def test_find_mstp_mode(hp_connect, capsys):
    hp_connect.find_stp_mode()
    captured = capsys.readouterr()
    assert 'MSTP' in captured.out

def test_find_rstp_mode(hp_connect, capsys):
    hp_connect.find_stp_mode()
    captured = capsys.readouterr()
    assert 'RSTP' in captured.out

def test_find_stp_mode(hp_connect, capsys):
    hp_connect.find_stp_mode()
    captured = capsys.readouterr()
    assert 'STP-compatible' in captured.out

def test_find_stp_disabled_switch(hp_connect, capsys):
    hp_connect.find_stp_disabled_switch()
    captured = capsys.readouterr()
    assert hp_connect.hostname in captured.out

def test_find_stp_enabled_switch(hp_connect, capsys):
    hp_connect.find_stp_enabled_switch()
    captured = capsys.readouterr()
    assert hp_connect.hostname in captured.out

def test_find_stp_root(hp_connect, capsys):
    hp_connect.find_stp_root()
    captured = capsys.readouterr()
    assert hp_connect.hostname in captured.out

def test_find_stp_root_rpvst_vlan(hp_connect, capsys):
    hp_connect.find_stp_root(rpvst_vlan=100)
    captured = capsys.readouterr()
    assert hp_connect.hostname in captured.out

def test_find_stp_forwarding_port(hp_connect, capsys):
    hp_connect.find_stp_forwarding_port()
    captured = capsys.readouterr()
    assert 'Forwarding' in captured.out

def test_find_stp_forwarding_port_rpvst(hp_connect, capsys):
    hp_connect.find_stp_forwarding_port(rpvst_vlan=100)
    captured = capsys.readouterr()
    assert 'Forwarding' in captured.out

def test_find_stp_blocking_port(hp_connect, capsys):
    hp_connect.find_stp_blocking_port()
    captured = capsys.readouterr()
    assert 'Blocking' in captured.out

def test_find_stp_blocking_port_rpvst(hp_connect, capsys):
    hp_connect.find_stp_blocking_port(rpvst_vlan=100)
    captured = capsys.readouterr()
    assert 'Blocking' in captured.out

def test_find_stp_disabled_port(hp_connect, capsys):
    hp_connect.find_stp_disabled_port()
    captured = capsys.readouterr()
    assert 'Disabled' in captured.out

def test_find_stp_disabled_port_rpvst(hp_connect, capsys):
    hp_connect.find_stp_disabled_port(rpvst_vlan=100)
    captured = capsys.readouterr()
    assert 'Disabled' in captured.out

def test_find_mac_address_port(hp_connect, capsys):
    mac = ['1458d0-13258c']
    hp_connect.find_mac_address_port(mac)
    captured = capsys.readouterr()
    assert hp_connect.hostname in captured.out

def test_find_mac_address_port_multiple_mac_port(hp_connect, capsys):
    mac = ['1458d0-13258c']
    hp_connect.find_mac_address_port(mac, multiple_mac_port=True)
    captured = capsys.readouterr()
    assert hp_connect.hostname in captured.out

def test_find_vlans(hp_connect, capsys):
    hp_connect.find_vlans([100])
    captured = capsys.readouterr()
    assert hp_connect.hostname in captured.out

def test_find_intrusion_alerts(hp_connect, capsys):
    hp_connect.find_intrusion_alerts()
    captured = capsys.readouterr()
    assert hp_connect.hostname in captured.out

def test_sftp_backup_config(hp_connect, capsys):
    sftp_server = '192.168.1.3'
    hp_connect.sftp_backup_config(sftp_server)
    captured = capsys.readouterr()
    assert hp_connect.hostname in captured.out

def test_sftp_backup_config_with_authentication(hp_connect, capsys):
    sftp_server = '192.168.1.3'
    hp_connect.sftp_backup_config(sftp_server, username='username', password='password')
    captured = capsys.readouterr()
    assert hp_connect.hostname in captured.out

def test_sftp_load_config(hp_connect, capsys):
    sftp_server = '192.168.1.3'
    filename = 'HP_2_2021-10-13'
    hp_connect.sftp_load_config(sftp_server, filename)
    captured = capsys.readouterr()
    assert hp_connect.hostname in captured.out

def test_sftp_load_config_with_authentication(hp_connect, capsys):
    sftp_server = '192.168.1.3'
    filename = 'HP_2_2021-10-13'
    hp_connect.sftp_load_config(sftp_server, filename, username='username', password='password')
    captured = capsys.readouterr()
    assert hp_connect.hostname in captured.out

def test_sftp_load_firmware_with_authentication_no_reboot(hp_connect, capsys):
    sftp_server = '192.168.1.3'
    firmware = 'WB_16_04_0016.swi'
    boot_image = 'secondary'
    hp_connect.sftp_load_firmware(sftp_server, firmware, boot_image, username='username', password='password')
    captured = capsys.readouterr()
    assert hp_connect.hostname in captured.out

def test_sftp_load_firmware_with_authentication_reboot(hp_connect, capsys):
    sftp_server = '192.168.1.3'
    firmware = 'WB_16_04_0016.swi'
    boot_image = 'secondary'
    hp_connect.sftp_load_firmware(sftp_server, firmware, boot_image, username='username', password='password', reboot=True)
    captured = capsys.readouterr()
    assert 'Rebooting' in captured.out

def test_sftp_load_firmware_no_reboot(hp_connect, capsys):
    sftp_server = '192.168.1.3'
    firmware = 'WB_16_04_0016.swi'
    boot_image = 'secondary'
    hp_connect.sftp_load_firmware(sftp_server, firmware, boot_image)
    captured = capsys.readouterr()
    assert hp_connect.hostname in captured.out

def test_sftp_load_firmware_reboot(hp_connect, capsys):
    sftp_server = '192.168.1.3'
    firmware = 'WB_16_04_0016.swi'
    boot_image = 'secondary'
    hp_connect.sftp_load_firmware(sftp_server, firmware, boot_image, reboot=True)
    captured = capsys.readouterr()
    assert 'Rebooting' in captured.out

def test_tftp_backup_config(hp_connect, capsys):
    tftp_server = '192.168.1.3'
    hp_connect.tftp_backup_config(tftp_server)
    captured = capsys.readouterr()
    assert hp_connect.hostname in captured.out

def test_tftp_load_config(hp_connect, capsys):
    tftp_server = '192.168.1.3'
    filename = 'HP_1_2021-10-14'
    hp_connect.tftp_load_config(tftp_server, filename)
    captured = capsys.readouterr()
    assert 'Rebooting' in captured.out

def test_tftp_load_firmware_no_reboot(hp_connect, capsys):
    tftp_server = '192.168.1.3'
    firmware = 'WB_16_04_0016.swi'
    boot_image = 'secondary'
    hp_connect.sftp_load_firmware(tftp_server, firmware, boot_image)
    captured = capsys.readouterr()
    assert hp_connect.hostname in captured.out

def test_tftp_load_firmware_reboot(hp_connect, capsys):
    tftp_server = '192.168.1.3'
    firmware = 'WB_16_04_0016.swi'
    boot_image = 'secondary'
    hp_connect.sftp_load_firmware(tftp_server, firmware, boot_image, reboot=True)
    captured = capsys.readouterr()
    assert 'Rebooting' in captured.out

def test_find_firmware_version(hp_connect, capsys):
    hp_connect.find_firmware_version()
    captured = capsys.readouterr()
    assert hp_connect.hostname in captured.out

def test_find_switch_mac_address(hp_connect, capsys):
    hp_connect.find_switch_mac_address()
    captured = capsys.readouterr()
    assert hp_connect.hostname in captured.out

def test_find_switch_mac_address_switch_mac_addr(hp_connect, capsys):
    switch_mac_addr = ['288023-4c77c0']
    hp_connect.find_switch_mac_address(switch_mac_addr)
    captured = capsys.readouterr()
    assert hp_connect.hostname in captured.out

def test_find_switch_serial_number(hp_connect, capsys):
    hp_connect.find_switch_serial_number()
    captured = capsys.readouterr()
    assert hp_connect.hostname in captured.out

def test_find_ports_down(hp_connect, capsys):
    hp_connect.find_ports_down()
    captured = capsys.readouterr()
    assert 'Down' in captured.out

def test_find_ports_up(hp_connect, capsys):
    hp_connect.find_ports_up()
    captured = capsys.readouterr()
    assert 'Up' in captured.out

def test_find_ip_from_mac_address(hp_connect, capsys):
    mac_address = ['1458d0-13537a']
    hp_connect.find_ip_from_mac_address(mac_address)
    captured = capsys.readouterr()
    assert hp_connect.hostname in captured.out

def test_find_mac_from_ip_address(hp_connect, capsys):
    ip_address = ['192.168.1.3']
    hp_connect.find_mac_from_ip_address(ip_address)
    captured = capsys.readouterr()
    assert hp_connect.hostname in captured.out

def test_find_port_security_enabled_ports(hp_connect, capsys):
    hp_connect.find_port_security_enabled_ports()
    captured = capsys.readouterr()
    assert 'Static' in captured.out

def test_find_port_security_disabled_ports(hp_connect, capsys):
    hp_connect.find_port_security_disabled_ports()
    captured = capsys.readouterr()
    assert 'Continuous' in captured.out

def test_find_jumbo_vlan(hp_connect, capsys):
    hp_connect.find_jumbo_vlan([100])
    captured = capsys.readouterr()
    assert hp_connect.hostname in captured.out

def test_find_voice_vlan(hp_connect, capsys):
    hp_connect.find_voice_vlan(50)
    captured = capsys.readouterr()
    assert hp_connect.hostname in captured.out

def test_find_poe_enabled_ports(hp_connect, capsys):
    hp_connect.find_poe_enabled_ports()
    captured = capsys.readouterr()
    assert 'Yes' in captured.out

def test_find_poe_disabled_ports(hp_connect, capsys):
    hp_connect.find_poe_disabled_ports()
    captured = capsys.readouterr()
    assert 'No' in captured.out

def test_find_poe_switch_status(hp_connect, capsys):
    hp_connect.find_poe_switch_status()
    captured = capsys.readouterr()
    assert hp_connect.hostname in captured.out

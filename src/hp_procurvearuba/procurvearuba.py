"""The procurvearuba module consists of  a class HP with custom methods to

manage HP Procurve and Aruba switches

Class HP is a composite of the netmiko library HPProcurveSSH class

"""
from netmiko.hp import HPProcurveSSH
from datetime import date
import re

from forwardable import forwardable, def_delegators


@forwardable()
class HP:
    """Class HP provides custom methods to manage HP Procurve and Aruba
    switches"""

    def_delegators(
        "HPProcurveSSH",
        "send_command_timing, send_command, find_prompt, disconnect",
    )

    def __init__(self, hostname, *args, **kwargs):
        """
        Parameters
        ----------
        hostname : str
            The hostname of the device.
        *args :
            Variable length argument list. Additional arguments
            should be passed in as keyword arguments.
        **kwargs :
            Arbitary keyword arguments. For extra arguments to 'HP': refer
            to the netmiko library documentation for a list of arguments to
            HPProcurveSSH class.
        """
        self.hostname = hostname
        self.HPProcurveSSH = HPProcurveSSH(*args, **kwargs)

    def __repr__(self):
        """Displays the device hostname of the HP class object instance"""
        return f"{self.hostname}"

    def find_stp_mode(self):
        """Finds the spanning tree mode of the switch"""
        output = self.send_command_timing("show spanning-tree")
        print("-" * 20)
        print(f"{'HOSTNAME':^10}{'STP_MODE':^10}")
        print("-" * 20)
        try:
            rpvst = re.search(r"^\s+Mode\s+:\s+(?P<mode>RPVST)", output, flags=re.M)
            print(f"{self.hostname:^10}{rpvst.group('mode'):^10}")
            print("-" * 20)
        except AttributeError:
            try:
                mstp = re.search(
                    r"^\s+Force\s+Version\s+:\s+(?P<mode>MSTP)", output, flags=re.M
                )
                print(f"{self.hostname:^10}{mstp.group('mode'):^10}")
                print("-" * 20)
            except AttributeError:
                try:
                    rstp = re.search(
                        r"^\s+Force\s+Version\s+:\s+(?P<mode>RSTP)", output, flags=re.M
                    )
                    print(f"{self.hostname:^10}{rstp.group('mode'):^10}")
                    print("-" * 20)
                except AttributeError:
                    try:
                        stp = re.search(
                            r"^\s+Force\s+Version\s+:\s+(?P<mode>STP-compatible)",
                            output,
                            flags=re.M,
                        )
                        print(f"{self.hostname:^10}{stp.group('mode'):^10}")
                        print("-" * 20)
                    except AttributeError:
                        print(f"{self.hostname:^10}{'CHECK SPANNING TREE IS ENABLED'}")

    def find_stp_disabled_switch(self):
        """Finds the switch which has spanning tree disabled."""
        print("-" * 20)
        output = self.send_command_timing("show spanning-tree")
        print(f"{'STP_DISABLED_SWITCH':^20}")
        print("-" * 20)
        try:
            if (
                re.search(
                    r"^\s+STP\s+Enabled\s+(\[No\]\s+:\s+No|:\s+No)", output, flags=re.M
                ).group(0)
                in output
            ):
                print(f"{self.hostname:^20}")
                print("-" * 20)
        except AttributeError:
            print("-" * 20)

    def find_stp_enabled_switch(self):
        """Finds and displays the switch which has spanning tree enabled."""
        output = self.send_command_timing("show spanning-tree")
        print("-" * 20)
        print(f"{'STP_ENABLED_SWITCH':^20}")
        print("-" * 20)
        try:
            if (
                re.search(
                    r"^\s+STP\s+Enabled\s+(\[No\]\s+:\s+Yes|:\s+Yes)",
                    output,
                    flags=re.M,
                ).group(0)
                in output
            ):
                print(f"{self.hostname:^20}")
                print("-" * 20)
        except AttributeError:
            print("-" * 20)

    def find_stp_root(self, rpvst_vlan=None):
        """Finds and displays the spanning tree root bridge.

        Parameters
        ----------
        rpvst_vlan : int
                    if rpvst is enabled on the switch, the rpvst_vlan
                    parameter allows the option to specify the keyword
                    argument to rpvst_vlan as a vlan integer.

        """
        if rpvst_vlan:
            output = self.send_command("show spanning-tree vlan " + str(rpvst_vlan))
            try:
                if (
                    re.search(r"(This switch is root)", output, flags=re.M).group(0)
                    in output
                ):
                    print(f"{'STP_ROOT_HOSTNAME':^10}{'VLAN':^10}")
                    print("-" * 25)
                    print(f"{self.hostname:^10}{rpvst_vlan:>13}")
                    print("-" * 25)
            except AttributeError:
                print("-" * 20)
        else:
            output = self.send_command("show spanning-tree")
            try:
                if (
                    re.search(r"(This switch is root)", output, flags=re.M).group(0)
                    in output
                ):
                    print("-" * 20)
                    print(f"{'STP_ROOT_HOSTNAME':^20}")
                    print("-" * 20)
                    print(f"{self.hostname:^20}")
                    print("-" * 20)
            except AttributeError:
                print("-" * 20)

    def find_stp_forwarding_port(self, rpvst_vlan=None):
        """Finds and displays the spanning tree forwarding ports

        Parameters
        ----------
        rpvst_vlan : int
                    if rpvst is enabled on the switch, the rpvst_vlan
                    parameter allows the option to specify the keyword
                    argument to rpvst_vlan as a vlan integer.

        """
        if rpvst_vlan:
            print("-" * 80)
            print(f"{'HOSTNAME :':>40}{self.hostname:>5}")
            print("-" * 80)
            print(
                f"{'PORT':>5}{'TYPE':>10}{'COST':>10}{'PRIORITY':>10}"
                f"{'ROLE':>10}{'STATE':>10}{'DESIGNATED_BRIDGE':>20}"
            )
            output = self.send_command("show spanning-tree vlan " + str(rpvst_vlan))
            output = output.strip().splitlines()
            print("-" * 80)
            for line in output:
                if "Forwarding" in line:
                    print(line)
                    print("-" * 80)
        else:
            print("-" * 80)
            print(f"{'HOSTNAME :':>40}{self.hostname:>5}")
            print("-" * 80)
            print(
                f"{'PORT':>5}{'TYPE':>10}{'COST':>10}{'PRIORITY':>10}"
                f"{'STATE':>10}{'DESIGNATED_BRIDGE':^20}{'HELLO':>5}"
                f"{'PTP':^5}{'EDGE':^5}"
            )
            print(f"{'TIME':>70}")
            output = self.send_command("show spanning-tree")
            output = output.strip().splitlines()
            print("-" * 80)
            for line in output:
                if "Forwarding" in line:
                    print(line)
                    print("-" * 80)

    def find_stp_blocking_port(self, rpvst_vlan=None):
        """Finds and displays the spanning tree blocked ports.

        Parameters
        ----------
        rpvst_vlan : int
                    if rpvst is enabled on the switch, the rpvst_vlan
                    parameter allows the option to specify the keyword
                    argument to rpvst_vlan as a vlan integer.

        """
        if rpvst_vlan:
            print("-" * 80)
            print(f"{'HOSTNAME :':>40}{self.hostname:>5}")
            print("-" * 80)
            print(
                f"{'PORT':>5}{'TYPE':>10}{'COST':>10}{'PRIORITY':>10}"
                f"{'ROLE':>10}{'STATE':>10}{'DESIGNATED_BRIDGE':>20}"
            )
            output = self.send_command("show spanning-tree vlan " + str(rpvst_vlan))
            output = output.strip().splitlines()
            print("-" * 80)
            for line in output:
                if "Blocking" in line:
                    print(line)
                    print("-" * 80)
        else:
            print("-" * 80)
            print(f"{'HOSTNAME :':>40}{self.hostname:>5}")
            print("-" * 80)
            print(
                f"{'PORT':>5}{'TYPE':>10}{'COST':>10}{'PRIORITY':>10}"
                f"{'STATE':>10}{'DESIGNATED_BRIDGE':^20}{'HELLO':>5}"
                f"{'PTP':^5}{'EDGE':^5}"
            )
            print(f"{'TIME':>70}")
            output = self.send_command("show spanning-tree")
            output = output.strip().splitlines()
            print("-" * 80)
            for line in output:
                if "Blocking" in line:
                    print(line)
                    print("-" * 80)

    def find_stp_disabled_port(self, rpvst_vlan=None):
        """Finds and displays the spanning tree disabled ports.

        Parameters
        ----------
        rpvst_vlan : int
                    if rpvst is enabled on the switch, the rpvst_vlan
                    parameter allows the option to specify the keyword
                    argument to rpvst_vlan as a vlan integer.

        """
        if rpvst_vlan:
            print("-" * 80)
            print(f"{'HOSTNAME :':>40}{self.hostname:>5}")
            print("-" * 80)
            print(
                f"{'PORT':>5}{'TYPE':>10}{'COST':>10}{'PRIORITY':>10}"
                f"{'ROLE':>10}{'STATE':>10}{'DESIGNATED_BRIDGE':>20}"
            )
            output = self.send_command("show spanning-tree vlan " + str(rpvst_vlan))
            output = output.strip().splitlines()
            print("-" * 80)
            for line in output:
                if "Ignore" in line:
                    continue
                if "Disabled" in line:
                    print(line)
                    print("-" * 80)
        else:
            print("-" * 80)
            print(f"{'HOSTNAME :':>40}{self.hostname:>5}")
            print("-" * 80)
            print(
                f"{'PORT':>5}{'TYPE':>10}{'COST':>10}{'PRIORITY':>10}"
                f"{'STATE':>10}{'DESIGNATED_BRIDGE':^20}{'HELLO':>5}"
                f"{'PTP':^5}{'EDGE':^5}"
            )
            print(f"{'TIME':>70}")
            output = self.send_command("show spanning-tree")
            output = output.strip().splitlines()
            print("-" * 80)
            for line in output:
                if "Disabled" in line:
                    print(line)
                    print("-" * 80)

    def find_mac_address_port(self, mac_addresses, multiple_mac_port=False):
        """Finds and displays the switch hostname, port and vlan of the specified
        mac addresses.

        Parameters
        ----------
        mac_addresses : list of str
                      The mac_addresses parameter accepts a list of one or more
                      mac addresses.
        multiple_mac_port : bool
                          Set the multiple_mac_port parameter to True when
                          searching for a mac address which is likely to be
                          found on a port containing multiple mac addresses.
        """
        print("-" * 40)
        print(f"{'HOSTNAME':^10}{'PORT':^10}{'MAC_ADDRESS':^10}{'VLAN':^10}")
        print("-" * 40)
        output = self.send_command_timing("show mac-address", use_textfsm=True)
        for mac in output:
            for m in mac_addresses:
                if mac["mac"] == m:
                    mac_addr = mac["mac"]
                    ports = mac["port"]
                    vlan = mac["vlan"]
                    output_2 = self.send_command_timing("show mac-address " + ports)
                    line_output = output_2.splitlines()
                    if multiple_mac_port:
                        for line in line_output:
                            if mac_addr in line:
                                print(
                                    f"{self.hostname:^10}{ports:^10}{mac_addr:^10}{vlan:^10}"
                                )
                                print("-" * 40)
                    else:
                        if len(line_output) <= 7:
                            for line in line_output:
                                if mac_addr in line:
                                    print(
                                        f"{self.hostname:^10}{ports:^10}{mac_addr:^10}{vlan:^10}"
                                    )
                                    print("-" * 40)

    def find_vlans(self, vlan):
        """Finds and displays the specified vlan if it exists on the switch.

        Parameters
        ----------
        vlan : list
             The vlan parameter accepts one or more vlan integer as input to the
             find_vlan function.
        """
        print("-" * 20)
        print(f"{'HOSTNAME':^10}{'VLAN':^10}")
        output = self.send_command_timing("show vlans", use_textfsm=True)
        print("-" * 20)
        for v in output:
            for vlan_num in vlan:
                if v["vlan_id"] == str(vlan_num):
                    print(f"{self.hostname:^10}{v['vlan_id']:^10}")
                    print("-" * 20)

    def find_interface_errors(self):
        """Finds and displays transmit or/and receive errors on the interface."""
        print("-" * 40)
        print(f"{'HOSTNAME':^10}{'PORT':^10}{'ERRORS_RX':^10}{'DROPS_TX':^10}")
        print("-" * 40)
        output = self.send_command_timing("show interfaces", use_textfsm=True)
        for errors in output:
            if errors["errors_rx"] > "0" or errors["drops_tx"] > "0":
                print(
                    f"{self.hostname:^10}{errors['port']:^10}{errors['errors_rx']:^10}"
                    f"{errors['drops_tx']:^10}"
                )
                print("-" * 40)

    def find_intrusion_alerts(self):
        """Finds and displays port security intrusion alarms on an interface."""
        output = self.send_command_timing("show interfaces brief", use_textfsm=True)
        print("-" * 40)
        print(f"{'HOSTNAME':^10}{'PORT':^10}{'INTRUSION':^10}{'STATUS':^10}")
        print("-" * 40)
        for alerts in output:
            if alerts["intrusion_alert"] == "Yes":
                print(
                    f"{self.hostname:^10}{alerts['port']:^10}{alerts['intrusion_alert']:^10}"
                    f"{alerts['status']:^10}"
                )
                print("-" * 40)

    def sftp_backup_config(self, sftp_server_ip, username=None, password=None):
        """Backs up the startup configuration to an sftp server.

        Parameters
        ----------
        sftp_server_ip : str
                       Specify the sftp server IP address
        username : str
                 Specify the username of the sftp server
        password : str
                 Specify the password of the sftp server
        """
        if username and password:
            output = self.send_command_timing(
                "copy startup-config sftp "
                + username
                + "@"
                + sftp_server_ip
                + " "
                + str(self.hostname)
                + "_"
                + str(date.today())
            )
            output += self.send_command_timing(password)
            if "SFTP download" in output:
                # if self.find_prompt():
                print(
                    f"Startup configuration successfully backed up for {self.hostname}"
                )
        else:
            output = self.send_command_timing(
                "copy startup-config sftp "
                + sftp_server_ip
                + " "
                + str(self.hostname)
                + "_"
                + str(date.today())
            )
            output += self.send_command_timing("\n")
            if "SFTP download" in output:
                # if self.find_prompt():
                print(
                    f"Startup configuration successfully backed up for {self.hostname}"
                )

    def sftp_load_config(self, sftp_server_ip, filename, username=None, password=None):
        """Loads a startup configuration from an sftp server.

        Parameters
        ----------
        sftp_server_ip : str
                      Specify the sftp server IP address
        filename : str
                Specify the filename of the configuration to be loaded
        username : str
                    Specify the username of the sftp server
        password : str
                    Specify the password of the sftp server
        """
        if username and password:
            output = self.send_command_timing(
                "copy sftp startup-config "
                + username
                + "@"
                + sftp_server_ip
                + " "
                + filename
            )
            output += self.send_command_timing("y")
            output += self.send_command_timing(password)
            print("Rebooting ", self.hostname)
        else:
            output = self.send_command_timing(
                "copy sftp startup-config " + sftp_server_ip + " " + filename
            )
            output += self.send_command_timing("y")
            output += self.send_command_timing("\n")
            print("Rebooting ", self.hostname)

    def sftp_load_firmware(
        self,
        sftp_server_ip,
        filename,
        boot_image,
        username=None,
        password=None,
        reboot=False,
    ):
        """Loads firmware from an sftp server.

        Parameters
        ----------
        sftp_server_ip : str
                       Specify the sftp server IP address
        filename : str
                  Specify the filename of the configuration to be loaded
        boot_image : str
                    Specify the boot image. Can be primary or secondary boot image.
        username : str
                  Specify the username of the sftp server
        password : str
                  Specify the password of the sftp server
        reboot : bool
               Set to True if switch is to be rebooted after firmware has been loaded
        """
        if username and password:
            output = self.send_command_timing(
                "copy sftp flash "
                + username
                + "@"
                + sftp_server_ip
                + " "
                + filename
                + " "
                + boot_image
            )
            output += self.send_command_timing("y")
            output += self.send_command_timing(password, delay_factor=10)
            print("Firmware loaded for ", self.hostname)
            if reboot:
                self.send_command_timing("boot system flash " + boot_image)
                self.send_command_timing("y")
                print("Rebooting ", self.hostname)
                self.disconnect()
        else:
            output = self.send_command_timing(
                "copy sftp flash " + sftp_server_ip + " " + filename + " " + boot_image
            )
            output += self.send_command_timing("y")
            output += self.send_command_timing("\n", delay_factor=10)
            print("Firmware loaded for ", self.hostname)
            if reboot:
                self.send_command_timing("boot system flash " + boot_image)
                self.send_command_timing("y")
                print("Rebooting ", self.hostname)
                self.disconnect()

    def tftp_backup_config(self, tftp_server_ip):
        """Backs up the startup configuration to a tftp server.

        Parameters
        ----------
        tftp_server_ip : str
                      Specify the tftp server IP address
        """
        output = self.send_command_timing(
            "copy startup-config tftp "
            + tftp_server_ip
            + " "
            + self.hostname
            + "_"
            + str(date.today())
        )
        if "TFTP download" in output:
            print(f"Startup configuration successfully backed up for {self.hostname}")

    def tftp_load_config(self, tftp_server_ip, filename):
        """Loads a startup configuration from an sftp server.

        Parameters
        ----------
        tftp_server_ip : str
                         Specify the tftp server IP address
        filename : str
                   Specify the filename of the configuration to be loaded
        """
        output = self.send_command_timing(
            "copy tftp startup-config " + tftp_server_ip + " " + filename
        )
        output += self.send_command_timing("y")
        output += self.send_command_timing("\n")
        print("Rebooting ", self.hostname)

    def tftp_load_firmware(self, tftp_server_ip, filename, boot_image, reboot=False):
        """Loads the switch firmware from a tftp server.

        Parameters
        ----------
        tftp_server_ip : str
                       Specify the tftp server IP address
        filename : str
                  Specify the filename of the configuration to be loaded
        boot_image : str
                    Specify the boot image. Can be primary or secondary boot image
        reboot : bool
               Set to True if switch is to be rebooted after firmware has been loaded
        """
        output = self.send_command_timing(
            "copy tftp flash " + tftp_server_ip + " " + filename + " " + boot_image
        )
        output += self.send_command_timing("y")
        output += self.send_command_timing("\n", delay_factor=10)
        print("Firmware loaded for ", self.hostname)
        if reboot:
            self.send_command_timing("boot system flash " + boot_image)
            self.send_command_timing("y")
            print("Rebooting ", self.hostname)
            self.disconnect()

    def find_firmware_version(self):
        """Displays the version of firmware on the switch."""
        print("-" * 25)
        print(f"{'HOSTNAME':^10}{'VERSION':^10}")
        print("-" * 25)
        output = self.send_command("show version")
        version = re.search(r"^(\s+\S+\.\S+\.\S+.*)", output, flags=re.M).group(1)
        print(f"{self.hostname:^10}{version.strip():^10}")
        print("-" * 25)

    def find_switch_mac_address(self, switch_mac_addr=None):
        """Finds and displays the switch with the specified mac address

        Parameters
        ----------
        switch_mac_addr : list
                       Specify the switch mac address
        """
        print("-" * 25)
        print(f"{'HOSTNAME':^10}{'MAC_ADDRESS':^10}")
        print("-" * 25)
        if switch_mac_addr:
            output = self.send_command("show spanning-tree")
            output = output.strip().splitlines()
            for i in output:
                for switch in switch_mac_addr:
                    if "Switch MAC Address" in i and switch in i:
                        print("-" * 25)
                        print(f"{self.hostname:^10}{switch:^10}")
                        print("-" * 25)
        else:
            output = self.send_command("show spanning-tree")
            switch_mac = re.search(
                r"^\s+Switch MAC Address\s+:\s+(\S{6}-\S{6}.*)", output, flags=re.M
            ).group(1)
            print(f"{self.hostname:^10}{switch_mac.strip():^10}")
            print("-" * 25)

    def find_switch_serial_number(self):
        """Finds and displays the switch hostname and associated serial number"""
        print("-" * 25)
        print(f"{'HOSTNAME':^10}{'SERIAL_NUMBER':^10}")
        print("-" * 25)
        output = self.send_command("show system")
        serial_number = re.search(
            r"^\s+ROM.*Serial Number\s+:\s+(\S+.*)", output, flags=re.M
        ).group(1)
        print(f"{self.hostname:^10}{serial_number.strip():^10}")
        print("-" * 25)

    def find_ports_down(self):
        """Finds and displays the interfaces in a 'DOWN' state."""
        print("-" * 12)
        print(f"{self.hostname:^10}")
        print("-" * 12)
        print(f"{'PORT':5}{'STATUS':5}")
        print("-" * 12)
        output = self.send_command_timing("show int brief", use_textfsm=True)
        count = 0
        for ports in output:
            if ports["status"] == "Down":
                count += 1
                print(f"{ports['port']:^5}{ports['status']:^5}")
                print("-" * 12)
        print()
        print(f"number of ports down: {count}")

    def find_ports_up(self):
        """Finds and displays the interfaces in an 'UP' state."""
        print("-" * 12)
        print(f"{self.hostname :^10}")
        print("-" * 12)
        print(f"{'PORT':5}{'STATUS':5}")
        print("-" * 12)
        output = self.send_command_timing("show int brief", use_textfsm=True)
        count = 0
        for ports in output:
            if ports["status"] == "Up":
                count += 1
                print(f"{ports['port']:^5}{ports['status']:^5}")
                print("-" * 12)
        print()
        print(f"number of ports up: {count}")

    def find_ip_from_mac_address(self, mac_address):
        """Finds and displays the IP address from the specified mac address

        Parameters
        ----------
        mac_addresses : list
                       Specify the mac address(s)
        """
        print("-" * 70)
        print(f"{'HOSTNAME':^20}{'MAC_ADDRESS':>20}{'IP_ADDRESS':>20}")
        print("-" * 70)
        output = self.send_command_timing("show arp", use_textfsm=True)
        for ip in output:
            for i in mac_address:
                if ip["mac"] == i:
                    print(f"{self.hostname :^20}{ip['mac']:^30}{ip['ip']:^10}")
                    print("-" * 70)

    def find_mac_from_ip_address(self, ip_address):
        """Finds and displays the mac address from the specified IP address(s)

        Parameters
        ----------
        ip_address : list
                       Specify the IP address(s)
        """
        print("-" * 70)
        print(f"{'HOSTNAME':^20}{'MAC_ADDRESS':>20}{'IP_ADDRESS':>20}")
        print("-" * 70)
        output = self.send_command_timing("show arp", use_textfsm=True)
        for ip_addr in output:
            for i in ip_address:
                if ip_addr["ip"] == i:
                    print(
                        f"{self.hostname :^20}{ip_addr['mac']:^30}{ip_addr['ip']:^10}"
                    )
                    print("-" * 70)

    def find_port_security_enabled_ports(self):
        """Finds and displays the ports enabled for port security"""
        print("-" * 85)
        print(f"{self.hostname:^85}")
        print("-" * 85)
        print(
            f"{'PORT':^20}{'LEARN_MODE':^20}{'ACTION':^20}{'EAVESDROP_PREVENTION':^25}"
        )
        print("-" * 85)
        output = self.send_command_timing("show port-security", use_textfsm=True)
        for port in output:
            if port["learn_mode"] != "Continuous":
                print(
                    f"{port['port'] :^20}{port['learn_mode'] :^20}{port['action'] :^20}"
                    f"{port['eavesdrop_prevention'] :^25}"
                )
                print("-" * 85)

    def find_port_security_disabled_ports(self):
        """Finds and displays the ports not enabled for port security"""
        print("-" * 85)
        print(f"{self.hostname:^85}")
        print("-" * 85)
        print(
            f"{'PORT':^20}{'LEARN_MODE':^20}{'ACTION':^20}{'EAVESDROP_PREVENTION':^25}"
        )
        print("-" * 85)
        output = self.send_command_timing("show port-security", use_textfsm=True)
        for port in output:
            if port["learn_mode"] == "Continuous":
                print(
                    f"{port['port'] :^20}{port['learn_mode'] :^20}{port['action'] :^20}"
                    f"{port['eavesdrop_prevention'] :^25}"
                )
                print("-" * 85)

    def find_jumbo_vlan(self, jumbo_vlan):
        """Finds and displays the vlan with jumbo configuration

        Parameters
        ----------
        jumbo_vlan : list
                   Specify the jumbo vlan
        """
        print("-" * 20)
        print(f"{'HOSTNAME':^10}{'JUMBO_VLAN':^10}")
        print("-" * 20)
        output = self.send_command_timing("show vlans", use_textfsm=True)
        for j in output:
            for v in jumbo_vlan:
                if j["jumbo"] == "Yes" and j["vlan_id"] == str(v):
                    print(f"{self.hostname:^10}{j['vlan_id']:^10}")
                    print("-" * 20)

    def find_voice_vlan(self, voice_vlan):
        """Finds and displays the vlan with voice configuration

        Parameters
        ----------
        voice_vlan : int
                   Specify the voice vlan
        """
        print("-" * 20)
        print(f"{'HOSTNAME':^10}{'VOICE_VLAN':^10}")
        print("-" * 20)
        output = self.send_command_timing("show vlans", use_textfsm=True)
        for v in output:
            if v["voice"] == "Yes" and v["vlan_id"] == str(voice_vlan):
                print(f"{self.hostname:^10}{v['vlan_id']:^10}")
                print("-" * 20)

    def find_poe_enabled_ports(self):
        """Finds and displays the POE+ enabled ports"""
        print("-" * 25)
        print(f"{self.hostname :^25}")
        print("-" * 25)
        print(f"{'PORT':^10}{'POE_ENABLED':^10}")
        output = self.send_command("show power-over-ethernet brief")
        output = output.strip().splitlines()
        for line in output:
            if re.search(r"^\s+\d+\s+Yes\s+", line, flags=re.M):
                port, poe_status, *extra = line.split()
                print(f"{port: ^10}{poe_status: ^10}")
                print("-" * 25)

    def find_poe_disabled_ports(self):
        """Finds and displays the POE+ disabled ports"""
        print("-" * 25)
        print(f"{self.hostname :^25}")
        print("-" * 25)
        print(f"{'PORT':^10}{'POE_ENABLED':^10}")
        print("-" * 25)
        output = self.send_command("show power-over-ethernet brief")
        output = output.strip().splitlines()
        for line in output:
            if re.search(r"^\s+\d+\s+No\s+", line, flags=re.M):
                port, poe_status, *extra = line.split()
                print(f"{port: ^10}{poe_status: ^10}")
                print("-" * 25)

    def find_poe_switch_status(self):
        """Finds and displays the switch with POE+ capability."""
        print("-" * 25)
        print(f"{'HOSTNAME':^10}{'POE_ENABLED':^10}")
        print("-" * 25)
        output = self.send_command("show power-over-ethernet")
        output = output.strip().splitlines()
        for line in output:
            if "POE+ Connected" in line:
                print(f"{self.hostname:^10}{'YES':^10}")
                print("-" * 25)

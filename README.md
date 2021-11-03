<div id="top"></div>

[![Code style][black-shield]][black-url]
[![PyPI][python-shield]][python-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/adraf82/hp_procurvearuba">
    <img src="images/switch.jpg" alt="Logo" width="500" height="90">
  </a>

<h3 align="center">hp_procurvearuba</h3>

  <p align="center">
    For easy management of hp procurve and aruba switches
    <br />
    <a href="https://github.com/adraf82/hp_procurvearuba"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/adraf82/hp_procurvearuba/issues">Report Bug</a>
    ·
    <a href="https://github.com/adraf82/hp_procurvearuba/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#installation">Installation</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#getting-started">Getting Started</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>
<!-- ABOUT THE PROJECT -->

## About hp_procurvearuba
The hp_procurvearuba project was created with the aim of simplifying the management of
HP procurve and aruba switches. The project provides a wrapper around the netmiko HPProcurveSSH
class consisting of a composite class called HP with custom functions to manage HP procurve and aruba switches.

The project consists of functions that will find and display only the information requested such as the
find_switch_serial_number function which displays the serial number of the switch;

```sh
-------------------------
 HOSTNAME SERIAL_NUMBER
-------------------------
   HP_1   SG59FLX6CK
-------------------------
```
There are many other practical functions in the hp_procurvearuba library such as functions for backing up configuration files, uploading configuration files and loading firmware with tftp and sftp.

To view the full list of functions and docstrings inclued in the library see the procurvearuba module [here](https://github.com/adraf82/hp_procurvearuba/tree/main/src/hp_procurvearuba)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Installation

The hp_procurvearuba package can be installed with pip as follows;

```sh
pip install hp_procurvearuba
```

### Prerequisites

External dependencies for the package will be installed with pip. To see the full list of dependencies see requirements.txt [here](https://github.com/adraf82/hp_procurvearuba/blob/master/requirements.txt)

The hp_procurvearuba project uses textfsm from the ntc-templates library for many functions. Set the environment variable NET_TEXTFSM to point to the index file in ntc-templates as below;

```sh
export NET_TEXTFSM=/path/to/ntc-templates/ntc_templates/templates
```

### Getting Started

Create a dictionary with your device details. Here is a list of devices displayed in yaml format;

```sh
devices:
- device_type: hp_procurve
  ip: 192.168.1.1
  hostname: HP_1
  password: password
  username: username
- device_type: hp_procurve
  ip: 192.168.1.2
  hostname: HP_2
  password: password
  username: username
```
Import the HP class with the following line;

```sh
from hp_procurvearuba import HP
```
Create an instance of the HP class;

```sh
with open('devices.yml', 'r') as f:
    device_data = yaml.safe_load(f)
    device_data = device_data.pop('devices')
    device_data = device_data

for device in device_data:
    hp_obj = HP(**device)
```

Invoke the function you require;

```sh
hp_obj.sftp_backup_config('192.168.1.3')
```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

For an example of a useable script and a devices inventory file please refer to the example_script.py and devices.yaml files in [examples](https://github.com/adraf82/hp_procurvearuba/tree/master/examples)

Included in the package is a set of unit tests. Pytest can be run against any of the functions. The full list of test functions can be found in the test_funcs.py file [here](https://github.com/adraf82/hp_procurvearuba/tree/master/tests)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions to the project are welcome. Any contributions you make are **greatly appreciated**. Please fork the repository and create a pull request. Run the tox program inside the root folder hp_procurvearuba when testing your changes. If you are adding a new function to the project, please add an accompanying unit test to the test_funcs.py file [here](https://github.com/adraf82/hp_procurvearuba/tree/master/tests)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Adeel Rauf - adraf2000@gmail.com

Project Link: [https://github.com/adraf82/hp_procurvearuba](https://github.com/adraf82/hp_procurvearuba)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Credit goes to the creators and maintainers of the following projects;

* [netmiko](https://github.com/ktbyers/netmiko)
* [ntc-templates](https://github.com/networktocode/ntc-templates)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[black-shield]:https://img.shields.io/badge/code%20style-black-000000.svg
[black-url]:https://github.com/ambv/black
[python-shield]:https://img.shields.io/pypi/v/hp_procurvearuba
[python-url]:https://pypi.org/project/hp-procurvearuba

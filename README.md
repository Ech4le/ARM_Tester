# ARM Tester

ARM Tester is a tool to estimate CPU performence for ARM devices.
Results will be printed in terminal, or saved to txt file.
Note: Device should have low load before testing, due to lower capacity of cores.

## TODO
 - [ ] Online API to compare common SBC
 - [ ] Comparision of results between devices (gui ?)

## Requirements

Git and sudo privileges to init apt install script.

## Installation

```bash
apt install git -y
git clone https://github.com/Ech4le/ARM_Tester/
cd ARM_Tester/
bash install.sh
```

## Usage

```bash
python3 main.py
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
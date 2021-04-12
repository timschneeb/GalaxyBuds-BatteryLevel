# GalaxyBuds-BatteryLevel
Simple python script to read battery values and the current wearing status from the Samsung Galaxy Buds, Buds+, Buds Live, and Buds Pro.

## Requirements

This script requires **Python 3.x**!

You need to install PyBluez:
```
pip install PyBluez
```
## AUR

You can find an installation package made by [@AriaMoradi](https://github.com/AriaMoradi) for Arch on the [AUR](https://aur.archlinux.org/packages/galaxybuds-batterylevel-git/):
```
yay -S galaxybuds-batterylevel-git
```


## Showcase

```
❯ python buds_battery.py 80:7B:3E:21:79:EC --help
usage: buds_battery.py [-h] [-m] [-t] [-w] [-v] mac-address

Read battery values of the Samsung Galaxy Buds or Buds+ [Left, Right, Case (Buds+)]

positional arguments:
  mac-address           MAC-Address of your Buds

optional arguments:
  -h, --help            show this help message and exit
  -m, --monitor         Notify on change
  -t, --monitor-timestamp
                        Notify on change and print timestamps
  -w, --wearing-status  Print wearing status instead
  -v, --verbose         Print debug information
```
```
❯ python3 buds_battery.py 80:7B:3E:21:79:EC
90,75,100
```
```
❯ python3 buds_battery.py 80:7B:3E:21:79:EC --wearing-status
Wearing,InCase
```
```
❯ python buds_battery.py 80:7B:3E:21:79:EC --monitor
97,81,86
96,81,86
96,82,86
```

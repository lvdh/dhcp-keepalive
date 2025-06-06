# dhcp-keepalive

Broadcast `DHCP DISCOVER` packets with a configurable interval.

## assumptions
- [Armbian] Linux v6.12 Minimal/IOT
- tools: `git`, `make`, `tcpdump`
- repo cloned to `/opt/dhcp-keepalive`
- cwd: `/opt/dhcp-keepalive`

## quick start
```
make help
```
### full setup, with system service
default interface: `end0`
```
sudo make all
```
custom interface:
```
sudo make INTERFACE=eth0 all
```
### install dependencies only
```
sudo make setup
```
### run without system service
```
sudo make run
```
### monitor packets
```
sudo make dump
```

## disclaimer
This tool was developed on personal time and equipment.

[Armbian]: https://www.armbian.com/

VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
INTERFACE ?= end0

.PHONY: all setup run dump service help clean
.ONESHELL: setup help run

all: setup service dump
setup:
	grep -q "bookworm" /etc/os-release && apt install -y python3.11-venv
	python3 -m venv $(VENV)
	. $(VENV)/bin/activate
	$(PIP) install scapy
run:
	. $(VENV)/bin/activate
	@# run with defaults
	$(PYTHON) dhcp-keepalive.py -i $(INTERFACE)
	@# run with random MAC (default) and 20s interval
	@#$(PYTHON) dhcp-keepalive.py -i $(INTERFACE) -t 20
	@# run with real interface MAC and 15s interval (default)
	@#$(PYTHON) dhcp-keepalive.py -i $(INTERFACE) -r
dump:
	tcpdump -i $(INTERFACE) udp port 68 and udp port 67
service: /etc/systemd/system/dhcp-keepalive.service
	systemctl enable dhcp-keepalive
	systemctl start dhcp-keepalive
/etc/systemd/system/dhcp-keepalive.service:
	cat dhcp-keepalive.service >/etc/systemd/system/dhcp-keepalive.service
	sed -i 's/INTERFACE/$(INTERFACE)/' /etc/systemd/system/dhcp-keepalive.service
help:
	. $(VENV)/bin/activate
	$(PYTHON) dhcp-keepalive.py --help
clean:
	rm -rf $(VENV)

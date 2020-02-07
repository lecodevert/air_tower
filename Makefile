UNAME := $(shell uname)
SHELL := $(shell which bash)

ifeq ($(UNAME),Darwin)
	oscad = /Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD
else
	oscad = /usr/bin/openscad
endif
output_dir = stl/

.ONESHELL:

stl:$(output_dir)base.stl $(output_dir)cover.stl $(output_dir)holder.stl $(output_dir)display.stl $(output_dir)support.stl

$(output_dir)base.stl: scad/base.scad
	$(oscad) -o $@ $<

$(output_dir)holder.stl: scad/holder.scad
	$(oscad) -o $@ $<

$(output_dir)cover.stl: scad/cover.scad
	$(oscad) -o $@ $<

$(output_dir)display.stl: scad/display.scad
	$(oscad) -o $@ $<

$(output_dir)support.stl: scad/support.scad
	$(oscad) -o $@ $<

clean:
	rm $(output_dir)*.stl

init: .make.python.packages .make.influxdb .make.grafana .make.mosquitto .make.venv requirements.txt
	pip3 install -r requirements.txt

lint: daemon.py modules/display/e_paper.py modules/mqtt/__init__.py
	pylint $^
	flake8 $^

.make.venv:
	python3 -m venv .
	source bin/activate

.make.python.packages:
	sudo apt install python3-venv libatlas-base-dev libopenjp2-7-dev
	touch .make.python.packages

.make.grafana:
	sudo apt-get install -y apt-transport-https software-properties-common wget
	wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
	echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
	sudo apt-get update
	sudo apt-get install grafana-rpi
	touch .make.grafana

.make.mosquitto:
	sudo apt install mosquitto
	touch .make.mosquitto

.make.influxdb:
	sudo apt install influxd
	touch .make.influxdb

.make.berrylan:
	echo -e "\n## nymea repo\ndeb http://repository.nymea.io buster main\ndeb-src http://repository.nymea.io buster main" | sudo tee /etc/apt/sources.list.d/nymea.list
	sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key A1A19ED6
	sudo apt update
	sudo apt install nymea-networkmanager
	touch .make.berrylan

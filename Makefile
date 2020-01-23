UNAME := $(shell uname)
.ONESHELL:

ifeq ($(UNAME),Darwin)
	oscad = /Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD
else
	oscad = /usr/bin/openscad
endif
output_dir = stl/

all:$(output_dir)base.stl $(output_dir)cover.stl $(output_dir)holder.stl $(output_dir)display.stl $(output_dir)support.stl

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

init:
	python3 -m venv .
	source bin/activate
	pip3 install -r requirements.txt

lint:daemon.py modules/display/e_paper.py
	pylint $<
	flake8 $<

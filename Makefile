UNAME := $(shell uname)

ifeq ($(UNAME),Darwin)
	oscad = /Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD
else
	oscad = /usr/bin/openscad
endif
output_dir = stl/

all:$(output_dir)base.stl $(output_dir)cover.stl $(output_dir)holder.stl

$(output_dir)base.stl: scad/base.scad
	$(oscad) -o $@ $<

$(output_dir)holder.stl: scad/holder.scad
	$(oscad) -o $@ $<

$(output_dir)cover.stl: scad/cover.scad
	$(oscad) -o $@ $<

clean:
	rm $(output_dir)*.stl

init:
	pip3 install -r requirements.txt

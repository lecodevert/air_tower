include <config.scad>;

use <base.scad>;
use <cover.scad>;
use <display.scad>;
use <holder.scad>;

color("Turquoise") base();
% translate([0, 0, cover_height + 2])
    rotate([180, 0, 0])
        cover();
color("Crimson") translate([0, 0, base_height + display_height - 2])
    rotate([180, 0, 75])
        display();
color("MediumSlateBlue") translate([0, 0, pms_height + base_height])
    holder(inner_diameter);

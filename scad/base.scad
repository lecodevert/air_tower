$fn = 100;
clearance = 0.1;

inner_diameter = 63 - clearance;
outer_diameter = 69;



module pi_mount() {
    for(i = [-1,1]) {
        difference(){
            union(){
                translate([-8.5, i*11.5, 4.5]) cube([5, 5, 9], center=true);
                translate([9, i*11.5, 4.5]) cube([5, 5, 9], center=true);
            }
            # translate([0, i*11.5, 4.5]) rotate([0, 90, 0]) cylinder(d=2.5 + clearance, h=25, center=true);
        }
    }
      % translate([-6, -16, 68]) rotate([0, 90, 0]) {
        import("Pi_Zero_W.stl");
        cube([67, 31, 12]);
    } // clearance for enviroplus hat
}


difference() {
    cylinder(h=70, d=outer_diameter);
    translate([-outer_diameter/2, -19, 2]) cube([outer_diameter, outer_diameter, 150]);
    translate([-10, -40, 4]) cube([20, 20, 60]);
    translate([-9, -21, 10.9]) cube([10, 10, 10]);
    translate([-9, -21, 23.5]) cube([10, 10, 10]);
}

cylinder(h=4, d=inner_diameter);

translate([0, 0, 4]) pi_mount();

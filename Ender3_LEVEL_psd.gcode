; Bed levelling cycle for the Creality Ender-3 V2: the nozzle goes down to Z0 over the four
; corners and the middle of the bed, four rounds, waiting a few seconds at each, for levelling
; the bed by hand.
;
; "Creality Leveling Cycle GCodes" by psdesign (Peter Solomon)
; https://www.thingiverse.com/thing:4761680
; Licensed under the Creative Commons Attribution licence (CC BY).
; Unchanged below this header.


G92 E0 ; reset extruder
; done purging extruder
G1 Z1.0 F3000 ; move z up little to prevent scratching of surface
M117 peter solomon design




; FIRST PASS
G0 Z10 F7200 ; Raise nozzle
G0 X30 Y35 Z10 ; Go to pos above 1st location
G0 X30 Y35 Z0 ; Go to 1st location
M117 First Corner 1st Round ; displays status
G4 S8 ; Wait 8 seconds

G0 Z10 ; Raise nozzle
G0 X30 Y205 Z10 ; Go to pos above 2nd location
G0 X30 Y205 Z0 ; Go to 2nd location
M117 Second Corner 1st Round ; displays status
G4 S8 ; Wait 8 seconds

G0 Z10 ; Raise nozzle
G0 X200 Y205 Z10 ; Go to pos above 3rd location
G0 X200 Y205 Z0 ; Go to 3rd location
M117 Third Corner 1st Round ; displays status
G4 S8 ; Wait 8 seconds

G0 Z10 ; Raise nozzle
G0 X200 Y35 Z10 ; Go to pos above 4th location
G0 X200 Y35 Z0 ; Go to 4th location
M117 Fourth Corner 1st Round ; displays status
G4 S8 ; Wait 8 seconds

G0 Z10 ; Raise nozzle
G0 X115 Y118 Z10 ; Go to pos above middle
G0 X115 Y118 Z0 ; Go to middle
M117 Middle 1st Round ; displays status
G4 S5 ; Wait 5 seconds


; SECOND PASS
G0 Z10 F7200 ; Raise nozzle
G0 X30 Y35 Z10 ; Go to pos above 1st location
G0 X30 Y35 Z0 ; Go to 1st location
M117 First Corner 2nd Round ; displays status
G4 S6 ; Wait 6 seconds

G0 Z10 ; Raise nozzle
G0 X30 Y205 Z10 ; Go to pos above 2nd location
G0 X30 Y205 Z0 ; Go to 2nd location
M117 Second Corner 2nd Round ; displays status
G4 S6 ; Wait 6 seconds

G0 Z10 ; Raise nozzle
G0 X200 Y205 Z10 ; Go to pos above 3rd location
G0 X200 Y205 Z0 ; Go to 3rd location
M117 Third Corner 2nd Round ; displays status
G4 S6 ; Wait 6 seconds

G0 Z10 ; Raise nozzle
G0 X200 Y35 Z10 ; Go to pos above 4th location
G0 X200 Y35 Z0 ; Go to 4th location
M117 Fourth Corner 2nd Round ; displays status
G4 S6 ; Wait 6 seconds

G0 Z10 ; Raise nozzle
G0 X115 Y118 Z10 ; Go to pos above middle
G0 X115 Y118 Z0 ; Go to middle
M117 Middle 2nd Round ; displays status
G4 S5 ; Wait 5 seconds


; THIRD PASS
G0 Z10 F7200 ; Raise nozzle
G0 X30 Y35 Z10 ; Go to pos above 1st location
G0 X30 Y35 Z0 ; Go to 1st location
M117 First Corner 3rd Round ; displays status
G4 S4 ; Wait 4 seconds

G0 Z10 ; Raise nozzle
G0 X30 Y205 Z10 ; Go to pos above 2nd location
G0 X30 Y205 Z0 ; Go to 2nd location
M117 Second Corner 3rd Round ; displays status
G4 S4 ; Wait 4 seconds

G0 Z10 ; Raise nozzle
G0 X205 Y205 Z10 ; Go to pos above 3rd location
G0 X205 Y205 Z0 ; Go to 3rd location
M117 Third Corner 3rd Round ; displays status
G4 S4 ; Wait 4 seconds

G0 Z10 ; Raise nozzle
G0 X200 Y35 Z10 ; Go to pos above 4th location
G0 X200 Y35 Z0 ; Go to 4th location
M117 Fourth Corner 3rd Round ; displays status
G4 S4 ; Wait 4 seconds

G0 Z10 ; Raise nozzle
G0 X115 Y118 Z10 ; Go to pos above middle
G0 X115 Y118 Z0 ; Go to middle
M117 Middle 3rd Round ; displays status
G4 S4 ; Wait 4 seconds


; FOURTH PASS
G0 Z10 F7200 ; Raise nozzle
G0 X30 Y35 Z10 ; Go to pos above 1st location
G0 X30 Y35 Z0 ; Go to 1st location
M117 First Corner 4th Round ; displays status
G4 S3 ; Wait 3 seconds

G0 Z10 ; Raise nozzle
G0 X30 Y205 Z10 ; Go to pos above 2nd location
G0 X30 Y205 Z0 ; Go to 2nd location
M117 Second Corner 4th Round ; displays status
G4 S3 ; Wait 3 seconds

G0 Z10 ; Raise nozzle
G0 X200 Y205 Z10 ; Go to pos above 3rd location
G0 X200 Y205 Z0 ; Go to 3rd location
M117 Third Corner 4th Round ; displays status
G4 S2 ; Wait 2 seconds

G0 Z10 ; Raise nozzle
G0 X200 Y35 Z10 ; Go to pos above 4th location
G0 X200 Y35 Z0 ; Go to 4th location
M117 Fourth Corner 4th Round ; displays status
G4 S3 ; Wait 3 seconds

G0 Z10 ; Raise nozzle
G0 X115 Y118 Z10 ; Go to pos above middle
G0 X115 Y118 Z0 ; Go to middle
M117 Middle  4th Round ; displays status
G4 S3 ; Wait 3 seconds

G0 Z30 ; Raise nozzle
M117 Done Leveling ; displays status

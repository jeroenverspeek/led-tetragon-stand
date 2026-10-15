# The LED tetragon: measurements

Everything measured on the panel and what is fixed to it, in mm. The stand is
built from these; in `build_stand.py` they are in the `Params` spreadsheet,
in `check_stand.py` the ones only used for checking.

Seen from the back means: looking at the back of the panel, standing upright
with the USB ports of the Pi at the top. "From the left" and "from the top"
are then from the edges of the panel. Seen from the front, left and right
swap.

## Photos

`photos/` has two photos of the back of the panel in its frame, taken on
2026-10-11, without the plugs in:

- `panel_back_photo.jpg`: straight from above, with a tape measure below it.
- `panel_back_flat.jpg`: taken at an angle and flattened with the Genius Scan
  app to the square of the panel (2531 x 2533 pixels for 192 x 192 mm, so
  13.2 pixels per mm). The panel itself gives the scale, no ruler needed.
  It is the same way round as "seen from the back" here: the middle bar
  upright, the connectors in the left half.

`photos/grid.py` cuts a region out of the flattened photo, enlarges it and
draws a millimetre grid over it, for example the power connector:

    python3 photos/grid.py photos/panel_back_flat.jpg power.png 36 64 72 92

The numbers are millimetres from the left and the top as seen in the photo
(left, right, top, bottom). This turned out to be a quick and precise way to
measure: the sizes of the connectors and the positions of the screw holes
below come from it, and it confirmed the hand measurements of the
connectors' positions to within 1-2 mm. Those last millimetres are
parallax: the flattening is exact in the plane of the back of the frame, but
the board lies 12 mm deeper. Heights, such as how far a plug sticks out, need
a photo from the side with a ruler next to it.

## Panel

- One 64 x 64 LED panel, P3: 192 x 192 mm.
- Front of the LEDs to the back of the factory frame: 14, the LEDs with their
  board 2 and the frame 12.
- Weight with the frame: about 400 g (guess).
- The panel lies a quarter turn round from how it was first mounted; the
  pictures are turned to match in software.

## Frame

- Five bars, all the full 12 deep, their backs flush: four round the edge,
  16 wide, and one up the middle, 20 wide. No other bars, no magnets.
- All holes are M3 with brass inserts; a screw can go all the way in, to the
  LED board. The positions below are the middles of the holes, from the
  flattened photo (2026-10-11). The inserts lie flush with the back of the
  frame, so there is no parallax, and the holes on the left and the right
  agree to within 0.5 mm. The hand measurements were 1-1.5 mm off.
- Middle bar: 4 holes, evenly spaced, in the middle of the bar: 9 from the
  top, then 66 and 126 (in a recess, deeper in the bar), and 9 from the
  bottom. The Pi is on the middle two.
- Left (seen from the back): a hole in each corner, in the top and bottom
  bars, 16 from the left and 8 from the top or bottom; and one in the left
  bar, 8 from the left and 88.5 from the top. The left bar has a small pin
  that can be snapped off if it is in the way.
- Right: the corner holes mirrored, 16 from the right. The one in the right
  bar is not mirrored but turned half round: 8 from the right and 88.5 from
  the bottom (103.5 from the top).

## Connectors of the panel

All on the left half, seen from the back.

- HUB75 IN (the lower of the two, the only one used): a 16-pin box header,
  28 wide and 9 high (from a flattened photo, 2026-10-11), its left side 30
  from the left, its middle 39 from the bottom. The
  header does not stick out past the bars, but the plug with its cable does,
  further than the power plug (how far is not measured). The ribbon leaves
  the plug upwards and goes over the hat to the lowest of the hat's three
  HUB75 connectors.
- HUB75 OUT: the same connector, the same way round, in the top corner:
  its left side 30 from the left, its middle 39 from the top. Not used here
  (the tetragon has one panel; on the LED hexahedron the panels are chained).
- Power: 16.5 wide (from the photo), its left side 40 from the left. From
  the top: 75 free, its snap-clip 4, the connector 7, and 106 free to the
  bottom (so its middle, clip included, 80.5 from the top). With its plug in it reaches 20 behind the back of the LED board,
  8 past the bars; the cable leaves the plug on the top side.

## Raspberry Pi with the electrodragon hat

- The hat: [RGB matrix panel drive board](https://www.electrodragon.com/product/rgb-matrix-panel-drive-board-raspberry-pi/)
  ([wiki](https://w.electrodragon.com/w/RPI_RMP_HDK)).
- In portrait on the middle two holes of the middle bar, USB ports at the
  top, the USB power port on the right side seen from the back.
- Seen from the back: from 90 from the left to 40 from the right, and from 40
  from the top (the USB ports). The hat sticks out below the Pi, down to 39
  from the bottom.
- Behind the LED board: the Pi's board at 22, the hat's at 33. With about
  3 of solder under the Pi and 9 of parts on the hat (guesses) it reaches from
  7 to 30 behind the frame.
- The feed of the electrodragon board and the Pi's power (via a USB adapter)
  are separate cables.
- Two USB cables in its ports, for the speaker and the micro:bit. Seen from
  the back the Pi 4 lies a quarter turned, its ports along its top: the USB
  2.0 pair 9 from its right edge to their middle, the USB 3.0 pair 27 (from
  its drawing). The plugs (about 16 x 8, 25 long with their grip; guess)
  stay below the top edge of the panel, 15 below it; the cables are stiff
  and stick out above it, about 50 before they bend over (guess). Which
  ports they are in is a guess too: the lower one of each pair.
- Weight with the cables: about 120 g (guess).

## USB speaker

- Kiwi Electronics KW-2835 (HK-5002), the same as Adafruit 3369: one box
  with two drivers, USB audio and power over one USB-A cable of about 1.2 m.
- 84 x 43 x 32, 74 g. The grille is on the flat face, a rectangle with half
  round ends (84 x 43); behind it the body is rounded.
- The cable leaves the bottom side, 33 from the left end of the face (seen
  from the back, grille backwards), pointing down; with its sleeve it needs
  10 below the speaker.
- On the back of the panel: grille backwards, 20 from the top and 5 from the
  left, so its rounded end stays clear of the corner of the Pi.

## micro:bit V2

- 51.6 x 42 x 11.65 (with its parts), about 10 g.
- In a USB port of the Pi with a 20 cm cable. Only tilted together with the
  panel; its buttons are not used.
- Its USB plug with the sleeve sticks out 40 straight from the micro:bit.
- On the back of the panel: upright between the power connector and HUB75
  IN, its USB port towards the Pi, LEDs towards the panel.

## Measured and decided

- `lip_height` 1 mm is fine.
- The back wall of the cradle was 40 mm high; the HUB75 IN plug, 32 mm up,
  sticks out behind the frame, so it is 28 mm now. That clears the hat too
  (it comes down to 39 mm, 19 mm behind the frame).
- Countersunk screws instead of knobs. From the outside of a cheek to the
  inside of an ear is 12.5 mm, so the screws are M5 x 12; a longer one
  reaches into the panel (a 19 mm one by 7 mm), so cut it to 12 mm. Making
  cheek and ear thicker instead would make the base too wide for the bed.

## Still guessed

- The weight of the panel (400 g) and the Pi (120 g): only used to check that
  the stand does not tip.
- The shape of the speaker's rounded back (from pictures); the cup only holds
  it by its flat face and leaves room behind it.
- How far the parts on the Pi and the hat stick out.
- How far the HUB75 IN plug sticks out and how much bigger it is than the
  header (12 mm and 2 mm all round). The cradle, the holder and the ribbon's
  bend depend on it.

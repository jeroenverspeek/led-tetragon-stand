# The LED tetragon: measurements

Everything measured on the panel and what is fixed to it, in mm. The stand is
built from these; in `build_stand.py` they are in the `Params` spreadsheet,
in `check_stand.py` the ones only used for checking.

Seen from the back means: looking at the back of the panel, standing upright
with the USB ports of the Pi at the top. "From the left" and "from the top"
are then from the edges of the panel. Seen from the front, left and right
swap.

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
  LED board.
- Middle bar: 4 holes, evenly spaced, the top one 10 from the top. The Pi is
  on the middle two.
- Left (seen from the back): a hole in each corner, in the top and bottom
  bars, 17 from the left and 8 from the top or bottom; and one in the left
  bar, 9 from the left and 87 from the top. The left bar has a small pin that
  can be snapped off if it is in the way.
- Right: the same holes, mirrored.

## Connectors of the panel

All on the left half, seen from the back.

- HUB75 IN (the lower of the two, the only one used): 26 wide and about 10
  high, its left side 30 from the left, its middle 39 from the bottom. The
  header does not stick out past the bars, but the plug with its cable does,
  further than the power plug (how far is not measured). The ribbon leaves
  the plug upwards and goes over the hat to the lowest of the hat's three
  HUB75 connectors.
- HUB75 OUT: above it, also 30 from the left; not used, not measured.
- Power: 18 wide and 8 high round its middle, 39 from the left and 80 from
  the top. With its plug in it reaches 20 behind the back of the LED board,
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

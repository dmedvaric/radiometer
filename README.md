# Radiometer: a low-cost night-sky light sensor

A photodiode-based radiometer built around an Arduino Uno and a 16-bit ADC (AD7705).
It records fast light signals such as lightning, meteors and street-lamp flicker,
and saves them as CSV files for later analysis.

!\[Radiometer sensor with photodiodes](docs/images/build/sensor\_photodiodes.png)

> \*\*Note:\*\* This is my high-school final thesis (\*završni rad\*), written in
> \*\*2018\*\*. The original thesis
> is in Croatian (\[PDF](docs/thesis\_original\_hr.pdf)); this repository is an
> English translation and summary. It is published as a portfolio project, and
> the code is shown as it was written at the time (see \[Known limitations](#known-limitations)).

## What it does

* Collects light signals with photodiodes and amplifies them with an op-amp.
* Digitizes the signal at 16-bit resolution, about 500 samples per second.
* Sends the data to a computer over serial, where a Python script plots it
and stores it in CSV files (10 seconds per file, about 5000 values each).
* Can detect lightning, measure light pollution, and show small deviations
in mains frequency through the flicker of street lighting.
* Total build cost is under 550 HRK (about 73 EUR), including a Raspberry Pi.

## How it works

```
Photodiodes -> Op-amp (LMC6462) -> AD7705 16-bit ADC -> Arduino Uno -> Computer (Python)
```

!\[Block diagram](hardware/schematics/block\_diagram.png)

1. **Sensor board:** six BPW34 photodiodes (two in parallel per input) feed an
LMC6462 op-amp. A trimmer potentiometer sets the sensitivity (set to maximum
for meteor recording). The board runs from a 9 V battery through a 5 V regulator.
2. **ADC:** the AD7705 digitizes the signal to 16 bits (the Arduino's built-in
ADC has only 10 bits).
3. **Arduino:** reads the ADC over SPI and sends every 16-bit value as two bytes
(low byte, high byte) over serial at 115200 baud.
4. **Python:** reassembles the bytes, timestamps the samples, plots the signal
with Matplotlib and saves it to CSV.

### Arduino to AD7705 wiring

|Arduino pin|AD7705 pin|
|-|-|
|10|CS|
|11|DIN|
|12|DOUT|
|13|SCK|

## Results (short version)

* **Test with a potentiometer** as a fake sensor: the system measured about
**492 samples per second** (target 500), confirming that the ADC, serial link
and Python code work together.
* **Street lamp:** the flicker of a street lamp was recorded and the
mains-frequency signal was visible in the data.
* **Lightning:** a thunderstorm was recorded from a window, and individual
flashes are clearly visible as peaks on the graph.

!\[Lightning recorded during a thunderstorm](docs/images/results/lightning\_1.png)

Details and graphs: [docs/results.md](docs/results.md)

## Repository contents

|Path|Description|
|-|-|
|[`firmware/radiometer\_arduino/`](firmware/radiometer_arduino/)|Arduino sketch that reads the AD7705 and streams data over serial|
|[`software/`](software/)|Python script for recording and plotting a 10-second block|
|[`hardware/BOM.md`](hardware/BOM.md)|Bill of materials|
|[`hardware/schematics/`](hardware/schematics/)|Block diagram, electrical schematic, assembly drawing, PCB layout|
|[`docs/schematics.md`](docs/schematics.md)|Components, signal path, assembly and housing|
|[`docs/results.md`](docs/results.md)|Test procedure, measurements and noise filter|
|[`docs/thesis\_original\_hr.pdf`](docs/thesis_original_hr.pdf)|The original thesis (Croatian)|

## Getting started

**Hardware:** see the [BOM](hardware/BOM.md) and [schematics](docs/schematics.md).

**Software requirements (as used in 2018):**

* Arduino IDE
* [AD770X library by Kerry Wong](http://www.kerrywong.com/2012/04/18/ad7705ad7706-library-revisited/)
(not included here, download it from the original source)
* Python 2.7 with `pyserial`, `numpy`, `matplotlib` (and `scipy` for the filter)

**Steps:**

1. Upload `firmware/radiometer\_arduino/radiometer\_arduino.ino` to the Arduino.
2. Edit the serial port in the Python script (`serial.Serial('COM3', 115200)`)
to match your system (Device Manager on Windows).
3. Run `software/readArduino.py`. It opens the data block on the Arduino, records for
10 seconds and plots the result.

## Known limitations

* The Python code is written for **Python 2** (`print` statements, `time.clock()`)
and will not run on Python 3 without changes.
* The serial port is hard-coded (`COM3`).
* Recording and plotting are separate steps, not a live view.
* Testing was done indoors; the outdoor enclosure described in the thesis was
designed but not fully built and tested.
* The thesis also mentions longer-running recording and plotting scripts
(`radiometarRecord`, `radiometarPlot`); only the 10-second script from the
thesis appendix is included here.

## Future improvements

**Planned in the thesis:**

* **Outdoor, standalone version:** replace the PC with a Raspberry Pi and put
everything in a waterproof installation box (155 x 80 x 60 mm), with the
3D-printed photodiode housing inside, so it can record all night outdoors.
* **Rechargeable power:** a battery module that charges the 9 V battery and
powers the Raspberry Pi at the same time, for places with no mains power.
* **Live view:** show the current signal values on a live-updating graph
instead of recording blocks first.
* **Broader applications:** extend use to more kinds of light-signal observation.

**Ideas I would add today:**

* Port the code to Python 3 and make the serial port a command-line argument.
* Better filtering. The moving-average filter removes mains ripple but also
smooths very short events, so a high-pass or notch filter would suit meteors better.
* Automatic event detection (threshold-based) that saves only the interesting
moments instead of everything.
* Timestamps from a real-time clock or GPS for correlating events with other observers.
* A proper PCB design export (Gerber files) and a version-controlled CAD model of the housing.

## Author

Dora Medvarić




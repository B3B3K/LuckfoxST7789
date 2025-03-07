# SPI Display Driver (spi.py)

## Overview

This Python script (`spi.py`) is an SPI-based driver for a 240x135 pixel LCD display. It uses the `spidev` library for SPI communication and the `periphery` library for GPIO control. The driver includes functions for initializing the display, drawing pixels, clearing the screen, and setting rotation.

## Features

- **SPI Communication**: Uses `spidev` to send commands and data to the LCD.
- **GPIO Control**: Manages RESET, DC, CS, and optional backlight pins.
- **Basic Graphics Functions**:
  - Clear screen or specific areas
  - Set individual pixels
  - Change screen rotation
- **Configurable SPI Speed**: Default set to 100 kHz.

## Requirements

- Python 3
- `spidev` library for SPI communication
- `periphery` library for GPIO control

### Install Dependencies

```sh
Luckfox has required libs.
```

## Hardware Connections

| Pin           | Which     |
| ------------- | --------- |
| RES           | 20th Pin  |
| DC\_PIN       | 19th Pin  |
| CS\_PIN       | CS        |
| BL\_PIN       | 1.3V      |
| DIN           | MISO      |

## Usage

### Running the Script

```sh
python3 spi.py
```

### Key Functions

#### Initialize Display

```python
lcd_init()
```

#### Clear Screen

```python
lcd_clear(0xFFFF)  # White background
```

#### Set Pixel

```python
lcd_set_pixel(10, 10, 0xF800)  # Red pixel at (10, 10)
```

#### Set Screen Rotation

```python
lcd_set_rotation(1)  # Rotate screen 90 degrees
```

**Rotation Options:**

- `0`: 0° (Default)
- `1`: 90° (Landscape)
- `2`: 180° (Upside Down)
- `3`: 270° (Reverse Landscape)

## Cleanup

The script ensures proper resource cleanup by closing SPI and GPIO resources when exiting.

## Notes

- Do not forget to enable SPI on "luckfox-config"
- Ensure correct SPI bus and GPIO mappings for your hardware.

## License

No warranty, try your self lol


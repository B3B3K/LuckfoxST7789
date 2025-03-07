import spidev
import time
from periphery import GPIO

# GPIO pins
RES_PIN = 145
DC_PIN = 144
CS_PIN = 0  # Assuming CS is controlled by SPI, set to 0 if not used
BL_PIN = 0  # Backlight pin (if available, otherwise ignore)

# Initialize GPIO
res_gpio = GPIO(RES_PIN, "out")
dc_gpio = GPIO(DC_PIN, "out")
cs_gpio = GPIO(CS_PIN, "out") if CS_PIN != 0 else None
bl_gpio = GPIO(BL_PIN, "out") if BL_PIN != 0 else None

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI bus 0, device 0
spi.max_speed_hz = 100000  # Set SPI speed to 100000 Hz
spi.mode = 0
spi.bits_per_word = 8

# Display dimensions
LCD_WIDTH = 240
LCD_HEIGHT = 135

def digital_write(pin, value):
    if pin is not None:
        if value == 0:
            value = False
        else:
            value = True
        pin.write(value)

def delay_ms(ms):
    time.sleep(ms / 1000.0)

def spi_write(data):
    if isinstance(data, int):
        data = [data]
    spi.xfer2(data)

def lcd_write_command(cmd):
    digital_write(dc_gpio, 0)  # DC pin low for command
    digital_write(cs_gpio, 0)  # CS pin low to select device
    spi_write(cmd)
    digital_write(cs_gpio, 1)  # CS pin high to release device

def lcd_write_data(data):
    digital_write(dc_gpio, 1)  # DC pin high for data
    digital_write(cs_gpio, 0)  # CS pin low to select device
    spi_write(data)
    digital_write(cs_gpio, 1)  # CS pin high to release device

def lcd_write_data_word(data):
    lcd_write_data((data >> 8) & 0xFF)
    lcd_write_data(data & 0xFF)

def lcd_reset():
    digital_write(res_gpio, 0)
    delay_ms(20)
    digital_write(res_gpio, 1)
    delay_ms(20)

def lcd_set_backlight(value):
    if bl_gpio is not None:
        # Assuming PWM control for backlight
        bl_gpio.write(value > 0)

def lcd_init():
    lcd_reset()

    #************* Start Initial Sequence **********//
    lcd_write_command(0x36)
    lcd_write_data(0x70)

    lcd_write_command(0x3A)
    lcd_write_data(0x05)

    lcd_write_command(0xB2)
    lcd_write_data(0x0C)
    lcd_write_data(0x0C)
    lcd_write_data(0x00)
    lcd_write_data(0x33)
    lcd_write_data(0x33)

    lcd_write_command(0xB7)
    lcd_write_data(0x35)

    lcd_write_command(0xBB)
    lcd_write_data(0x19)

    lcd_write_command(0xC0)
    lcd_write_data(0x2C)

    lcd_write_command(0xC2)
    lcd_write_data(0x01)

    lcd_write_command(0xC3)
    lcd_write_data(0x12)

    lcd_write_command(0xC4)
    lcd_write_data(0x20)

    lcd_write_command(0xC6)
    lcd_write_data(0x0F)

    lcd_write_command(0xD0)
    lcd_write_data(0xA4)
    lcd_write_data(0xA1)

    lcd_write_command(0xE0)
    lcd_write_data(0xD0)
    lcd_write_data(0x04)
    lcd_write_data(0x0D)
    lcd_write_data(0x11)
    lcd_write_data(0x13)
    lcd_write_data(0x2B)
    lcd_write_data(0x3F)
    lcd_write_data(0x54)
    lcd_write_data(0x4C)
    lcd_write_data(0x18)
    lcd_write_data(0x0D)
    lcd_write_data(0x0B)
    lcd_write_data(0x1F)
    lcd_write_data(0x23)

    lcd_write_command(0xE1)
    lcd_write_data(0xD0)
    lcd_write_data(0x04)
    lcd_write_data(0x0C)
    lcd_write_data(0x11)
    lcd_write_data(0x13)
    lcd_write_data(0x2C)
    lcd_write_data(0x3F)
    lcd_write_data(0x44)
    lcd_write_data(0x51)
    lcd_write_data(0x2F)
    lcd_write_data(0x1F)
    lcd_write_data(0x1F)
    lcd_write_data(0x20)
    lcd_write_data(0x23)

    lcd_write_command(0x21)
    lcd_write_command(0x11)
    lcd_write_command(0x29)

def lcd_set_cursor(x_start, y_start, x_end, y_end):
    lcd_write_command(0x2A)
    lcd_write_data_word(x_start + 40)
    lcd_write_data_word(x_end + 40)

    lcd_write_command(0x2B)
    lcd_write_data_word(y_start + 53)
    lcd_write_data_word(y_end + 53)

    lcd_write_command(0x2C)

def lcd_clear(color):
    lcd_set_cursor(0, 0, LCD_WIDTH - 1, LCD_HEIGHT - 1)
    for _ in range(LCD_WIDTH * LCD_HEIGHT):
        lcd_write_data_word(color)

def lcd_clear_window(x_start, y_start, x_end, y_end, color):
    lcd_set_cursor(x_start, y_start, x_end - 1, y_end - 1)
    for _ in range((x_end - x_start) * (y_end - y_start)):
        lcd_write_data_word(color)

def lcd_set_pixel(x, y, color):
    lcd_set_cursor(x, y, x, y)
    lcd_write_data_word(color)

# Main program
def lcd_set_rotation(rotation):
    """
    Set screen rotation.
    rotation: 0 (0°), 1 (90°), 2 (180°), 3 (270°)
    """
    rotation_values = {
        0: 0x00,  # Normal
        1: 0x60,  # 90 degrees
        2: 0xC0,  # 180 degrees
        3: 0xA0   # 270 degrees
    }

    if rotation not in rotation_values:
        print("Invalid rotation! Use 0, 1, 2, or 3.")
        return

    lcd_write_command(0x36)  # MADCTL (Memory Data Access Control)
    lcd_write_data(rotation_values[rotation])

# Example usage
if __name__ == "__main__":
    try:
        lcd_init()  # Initialize the display
        lcd_set_rotation(1)  # Set screen rotation to 90 degrees
        lcd_clear(0xFFFF)  # Clear the screen with white color

    finally:
        lcd_set_pixel(10, 10, 0xF800)
        spi.close()
        res_gpio.close()
        dc_gpio.close()
        if cs_gpio is not None:
            cs_gpio.close()
        if bl_gpio is not None:
            bl_gpio.close()



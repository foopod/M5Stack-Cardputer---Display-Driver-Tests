""" M5STACK Cardputer 135x240 display """

from machine import Pin, freq
import s3lcd

BL = Pin(38, Pin.OUT)

TFA = 1
BFA = 1
WIDE = 1
TALL = 0

freq(240_000_000)

def config(rotation=0, options=0):
    """Configure the display and return an ESPLCD instance."""

    BL.value(1)
    
    custom_init = (
        ( b'\x11', b'\x00', 120),               # Exit sleep mode
        ( b'\x13', b'\x00', 0),                 # Turn on the display
        ( b'\xb6', b'\x0a\x82', 0),             # Set display function control
        ( b'\x3a', b'\x55', 10),                # Set pixel format to 16 bits per pixel (RGB565)
        ( b'\xb2', b'\x0c\x0c\x00\x33\x33', 0), # Set porch control
        ( b'\xb7', b'\x35', 0),                 # Set gate control
        ( b'\xbb', b'\x28', 0),                 # Set VCOMS setting
        ( b'\xc0', b'\x0c', 0),                 # Set power control 1
        ( b'\xc2', b'\x01\xff', 0),             # Set power control 2
        ( b'\xc3', b'\x10', 0),                 # Set power control 3
        ( b'\xc4', b'\x20', 0),                 # Set power control 4
        ( b'\xc6', b'\x0f', 0),                 # Set VCOM control 1
        ( b'\xd0', b'\xa4\xa1', 0),             # Set power control A
                                                # Set gamma curve positive polarity
        ( b'\xe0', b'\xd0\x00\x02\x07\x0a\x28\x32\x44\x42\x06\x0e\x12\x14\x17', 0),
                                                # Set gamma curve negative polarity
        ( b'\xe1', b'\xd0\x00\x02\x07\x0a\x28\x31\x54\x47\x0e\x1c\x17\x1b\x1e', 0),
        ( b'\x21', b'\x00', 0),                 # Enable display inversion
        ( b'\x29', b'\x00', 120)                # Turn on the display
    )

    custom_rotations = (
        (135, 240, 52, 40, False, False, False),
        (240, 135, 40, 53, True, True, False),
        (135, 240, 53, 40, False, True, True),
        (240, 135, 40, 52, True, False, True))

    bus = s3lcd.SPI_BUS(
        2, mosi=35, sck=36, dc=34, cs=37, pclk=40000000, swap_color_bytes=True
    )

    return s3lcd.ESPLCD(
        bus,
        135,
        240,
        inversion_mode=True,
        color_space=s3lcd.BGR,
        reset=33,
        rotations=custom_rotations,
        rotation=rotation,
        dma_rows=32,
        options=options,
    )


def deinit(tft, display_off=False):
    """Take an ESPLCD instance and Deinitialize the display."""
    tft.deinit()
    if display_off:
        BL.value(0)

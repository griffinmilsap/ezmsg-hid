import asyncio
import typing
import math
import time

from pathlib import Path

import ezmsg.core as ez

from ezmsg.hid.device import HIDDevice, HIDDeviceSettings
from ezmsg.hid.messages import MouseMessage

class MouseMessageGeneratorSettings(ez.Settings):
    pub_rate: float = 10 # Hz

class MouseMessageGenerator(ez.Unit):
    SETTINGS: MouseMessageGeneratorSettings

    OUTPUT = ez.OutputStream(MouseMessage)

    @ez.publisher(OUTPUT)
    async def output_mouse(self) -> typing.AsyncGenerator:
        while True:
            await asyncio.sleep(1.0 / self.SETTINGS.pub_rate)

            w = 2.0 * math.pi * 0.1 * time.time()
            yield self.OUTPUT, MouseMessage(
                relative_x = ((math.cos(w) / 2.0) + 1.0) * 0.01,
                relative_y = ((math.sin(w) / 2.0) + 1.0) * 0.01
            )

if __name__ == '__main__':

    generator = MouseMessageGenerator()

    mouse_device = HIDDevice(
        HIDDeviceSettings(
            device = Path('/dev/hidg1')
        )
    )

    ez.run(
        GENERATOR = generator,
        MOUSE_DEVICE = mouse_device,
        connections = (
            (generator.OUTPUT, mouse_device.INPUT_HID),
        )
    )




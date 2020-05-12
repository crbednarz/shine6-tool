import math
from Shine6 import commands as cmd
from Shine6.commands import LightingMode
from Shine6.keyboard import open_keyboard, KeyLayout


def getColor(x, y, t):
    x /= 5
    y /= 5

    r = math.sin(x + t * 0.1) * 0.5 + 0.5
    g = math.sin(y + t * 0.05 + 0.5) * 0.5 + 0.5
    b = math.cos(y + t * 0.07 + 0.25) * 0.5 + 0.5

    return (int(r * 255) & 0xFF, int(g * 255) & 0xFF, int(b * 255) & 0xFF)

if __name__ == '__main__':
    with open_keyboard() as keyboard:
        keyboard.send_packets(
            cmd.lock_settings() +
            cmd.use_host_lighting()
        )

        colors = bytearray(140 * 3)
        for i in range(0, 1000):
            for y in range(0, 6):
                for x in range(0, 21):
                    index = y * 21 + x
                    index = KeyLayout[index]
                    if (index == -1):
                        continue
                    result = getColor(x, y, i)
                    colors[index * 3 + 0] = result[0]
                    colors[index * 3 + 1] = result[1]
                    colors[index * 3 + 2] = result[2] 
            
            keyboard.send_packets(
                cmd.set_leds(colors) +
                cmd.use_lighting_mode(LightingMode.Custom)
            )

        keyboard.send_packets(
            cmd.unlock_settings()
        )
        
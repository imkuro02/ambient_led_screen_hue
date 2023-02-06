def hex_to_rgb(hex):
    rgb = []
    for i in (0,2,4):
        decimal = int(hex[i:i+2], 16)
        rgb.append(decimal)
    return tuple(rgb)

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

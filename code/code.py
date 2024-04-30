import board
from kmk.kmk_keyboard import KMKKeyboard, UnicodeMode
from kmk.keys import KC, make_key
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.combos import Combos, Sequence
from kmk.modules.layers import Layers

total_layers = 2

keyboard = KMKKeyboard()

keyboard.debug_enabled = True

encoder_handler = EncoderHandler()

layers = Layers()
combos = Combos()

keyboard.modules = [encoder_handler, layers, combos]

keyboard.extensions.append(MediaKeys())

keyboard.col_pins = (board.GP0, board.GP1, board.GP2, board.GP3)
keyboard.row_pins = (board.GP4, board.GP5, board.GP6, board.GP7)
keyboard.diode_orientation = DiodeOrientation.ROW2COL

encoder_handler.pins = ((board.GP26, board.GP27, board.GP28, True, 2),)

active, changed = 0, 0


def change_encoder_momentarily(*args, **kwargs):
    global active, changed

    active = keyboard.active_layers[0]
    changed = active
    print(active)
    print(changed)

    # TODO append extra knobs to encoder_preset
    encoder_handler.map = [
    # preset
    ((KC.TO(1), KC.TO(1), KC.NO),),
    ((KC.TO(0), KC.TO(0), KC.NO),),
]
    keyboard.keymap = keybrd_ops[active]
    keyboard.tap_key(KC.TO(0))


def reset_encoder(*args, **kwargs):
    global active, changed, keybrd_preset, keybrd_ops,encoder_preset

    changed = keyboard.active_layers[0]
    print(active)
    print(changed)

    # if active != changed:
    keybrd_preset.pop(active)
    keybrd_preset.insert(active, keybrd_ops[active][changed])
    encoder_handler.map = encoder_preset
    keyboard.keymap = keybrd_preset
    keyboard.tap_key(KC.TO(active))


# layers inside presets
make_key(
    names=("FNKEY",),
    on_press=change_encoder_momentarily,
    on_release=reset_encoder,
)

keybrd_ops = [
    # Preset 1
    [
        # layer 1
        [KC.A, KC.B, KC.C, KC.D] + [KC.NO] * 11 + [KC.FNKEY],
        [KC.E, KC.F, KC.G, KC.H] + [KC.NO] * 11 + [KC.FNKEY],
    ],
    # Preset 2
    [
        # layer 1
        [KC.N1, KC.N2, KC.N3, KC.N4] + [KC.NO] * 11 + [KC.FNKEY],
        [KC.N5, KC.N6, KC.N7, KC.N8] + [KC.NO] * 11 + [KC.FNKEY],
    ],
]

# keybrd_preset = [
#     keybrd_ops[0][0],
#     keybrd_ops[1][0],
# ]

keybrd_preset = [keybrd_ops[i][0] for i in range(total_layers)]

# encoder_preset = [
#     ((KC.TO(i + (total_layers - 1) % total_layers), KC.TO((i + 1) % total_layers)),)
#     for i in range(total_layers)
# ]
encoder_preset = [
    # preset
    ((KC.TO(1), KC.TO(1), KC.NO),),
    ((KC.TO(0), KC.TO(0), KC.NO),),
]

# TODO append extra knobs to encoder_preset

encoder_handler.map = encoder_preset

keyboard.keymap = keybrd_preset

# combos.combos = [
#     # function key
#     Sequence(
#         (15, 1),
#         KC.P,
#         fast_reset=False,
#         # per_key_timeout=False,
#         timeout=1000,
#         match_coord=True,
#     ),
# ]

if __name__ == "__main__":
    keyboard.go()

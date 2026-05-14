# Fix-ps2

Utilities and documented defaults for making the iPSX2/PCSX2 iOS port feel smoother, reduce avoidable frame drops, and recover safely from bad settings.

## FPS / smoothness optimizer

`tools/ipsx2_optimize_config.py` applies conservative INI settings for iPSX2/PCSX2:

- enables safe speed-hack defaults such as MTVU/VU threading;
- forces low-cost Metal rendering defaults, native internal resolution, and fewer expensive OSD counters;
- clamps known numeric settings to safe ranges so bad hand-edits do not create stalls or broken emulator state;
- writes atomically and creates a `.bak` backup by default to avoid corrupting configuration files.

### Usage

```bash
python tools/ipsx2_optimize_config.py /path/to/PCSX2.ini --preset smooth
```

Available presets:

| Preset | Goal |
| --- | --- |
| `smooth` | Best default for higher FPS and stable frame pacing. |
| `battery` | More aggressive CPU underclocking and less overlay work for cooler devices. |
| `quality` | Keeps some accuracy/quality options while still enabling safer performance defaults. |

Preview changes without writing:

```bash
python tools/ipsx2_optimize_config.py /path/to/PCSX2.ini --preset smooth --dry-run
```

Restore the previous file by copying the generated `.bak` over the edited INI.

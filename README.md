# Fix-ps2

Utilities, build scaffolding, and documented defaults for making the iPSX2/PCSX2 iOS port feel smoother, reduce avoidable frame drops, and recover safely from bad settings.

## Unsigned IPA build scaffold

The GitHub Actions workflow used by the upstream iPSX2 project runs CMake from `cpp/`. This repository now includes a minimal CMake/iOS target in that directory so the workflow can start, configure an Xcode project, archive an unsigned `iPSX2.app`, and package an `.ipa` instead of failing before the first build command because `cpp/` is missing.

The scaffold is intentionally small: it is an iOS shell that displays the compiled-in performance recommendations and keeps the IPA pipeline healthy while the full upstream PCSX2/iPSX2 engine sources are absent from this repository.

Local CMake sanity check on non-Apple hosts:

```bash
cmake -S cpp -B /tmp/ipsx2-cmake-check -G "Unix Makefiles"
cmake --build /tmp/ipsx2-cmake-check
```

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

# Klipper Maintenance

**Keep your 3D printer running smoothly**

---

## Features

Klipper Maintenance supports the following features:

- Maintenance reminders in the terminal
- Maintenance reminders on the printer display
- Print time thresholds
- Filament thresholds
- Time thresholds

## Get Started

Follow [Installation](install.md) to get started with Klipper Maintenance.

## How it Works

After installing, first you configure `[maintain xxx]` sections, passing in a `trigger`, `threshold`, `label`, and `message`:

```cfg
[maintain xyrods]
label: XY smooth rods
trigger: print_time
threshold: 250 # Trigger every 250 print hours
message: Lubricate XY smooth rods

[maintain extruder]
label: Extruder
trigger: filament
threshold: 660 # Trigger every 660 meters of filament (2kg of PLA)
message: Tighten extruder grub screw and perform a cold pull
```

There are three `trigger` options:

- `print_time` Print time, measured in hours
- `filament` Extruded filament, measured in meters (330m is roughly 1kg of PLA)
- `time` Time, measured in hours

Next, you configure a `[maintain]` section to manage all the maintenance:

```cfg
[maintain]
interval: 60 # optional, time (in seconds) between checking if maintenance is due (default is 60)
```
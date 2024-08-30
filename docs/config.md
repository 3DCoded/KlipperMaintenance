# Configuration

After installing KlipperMaintenance, follow this guide to configure it.

## Main Section

First, a main `[maintain]` section must be configured. This has two main purposes:

1. Check periodically if maintenance needs to be done
2. Provide the `MAINTAIN_STATUS` command

To configure it, add to your `printer.cfg`:

```cfg title="printer.cfg"
[maintain]
interval: 60 # optional, time (in seconds) between checking if maintenance needs to be done (default is 60)
```

## Maintenance Sections

Next, for each maintenance object, a `[maintain xxx]` config section should be configured. In this example, three maintenance objects will be configured (note the times here are purely for demonstration and are probably not ideal):

1. Lubricate XY rods (250 hours print time)
2. Replace air filter (500 hours time)
3. Clean and tighten extruder screws (700m filament)

For each `[maintain xxx]` section, there are four options that must be set:

- **`label`** text that will be displayed when referring to this maintenance object
- **`trigger`** type of event that triggers this maintenance. Currently three options:
    - **`print_time`** print time, in hours
    - **`filament`** extruded filament, in meters (330m is roughly 1kg of PLA)
    - **`time`** time, in hours
- **`threshold`** how often maintenance needs to be done. For `print_time` and `time`, this is in hours. For `filament`, this is in meters
- **`message`** message that will be displayed when maintenance needs to be done

!!! example "Experimental"
    - **`expired_gcode`** GCode to run after maintenance expires. Not required

Example:

```cfg title="printer.cfg"
# Lubricate XY rods
[maintain xyrods]
label: XY smooth rods
trigger: print_time
threshold: 250
message: Lubricate XY smooth rods

# Replace air filter
[maintain airfilter]
label: Air filter
trigger: time
threshold: 500
message: Replace HEPA and charcoal filters

# Extruder maintenance
[maintain extruder]
label: Extruder maintenance
trigger: filament
threshold: 700
message: Clean extruder gears and tighten extruder bolts
```
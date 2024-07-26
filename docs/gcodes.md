# G-Codes

KlipperMaintenance provides a few helper GCodes to manage your maintenance. Follow this guide to learn how to use them.

## MAINTAIN_STATUS

Shows the current status of maintenance. Accepts no parameters. Using the example from [Configuration](config.md#maintenance-sections) and assuming air filter is expired, here is an example:

```title="Input"
MAINTAIN_STATUS
```

```title="Output"
XY smooth rods: 200h remaining
Maintenance "Air filter" Expired!
Replace HEPA and charcoal filters
Extruder maintenance: 400m remaining
```

## CHECK_MAINTENANCE

Shows the current status of provided maintenance. Example:

```title="Input"
CHECK_MAINTENANCE NAME=xyrods
```

```title="Output"
Maintenance xyrods Status:
Next maintenance in 200h
Maintenance message: Lubricate XY smooth rods
```

## UPDATE_MAINTENANCE

Marks the provided maintenance as complete. Example:

```title="input"
UPDATE_MAINTENANCE NAME=xyrods
```

This resets the maintenance timer for the `xyrods` maintenance.
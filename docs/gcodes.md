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

You can also pass a `HOURS` parameter to set the current amount of working hours. Example:

Your `threshold` for `xyrods` is set to `350` print hours. You have printed for `100` hours so far.

Run the following command:

```title="input"
UPDATE_MAINTENANCE NAME=xyrods HOURS=100
```

This will ensure that KlipperMaintenance reminds you to lubricate your XY rods after **`250`** hours, not `350`.
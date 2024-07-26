# Installation

Follow this guide to install or update KlipperMaintenance.

## Install

To install KlipperMaintenance, run in your terminal:

```sh
cd ~
git clone https://github.com/3DCoded/KlipperMaintenance
cd KlipperMaintenance
sh install.sh
sudo service klipper restart
```

Add to your `moonraker.conf`:

```cfg title="moonraker.conf"
# KlipperMaintenance Update Manager
[update_manager KlipperMaintenance]
type: git_repo
path: ~/KlipperMaintenance
origin: https://github.com/3DCoded/KlipperMaintenance.git
primary_branch: dev
is_system_service: False
install_script: install.sh
```

## Update

To update KlipperMaintenance, update via Moonraker's update manager, then run in your terminal:

```sh
cd KlipperMaintenance
sh install.sh
sudo service klipper restart
```
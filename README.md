# Crackle

> **NOTE** if you were using crackle before v0.3.0 you will need to nuke your crackle install first before installing v0.3.0.

A project started by Fuseteam, inspired by [Pacstall](https://github.com/pacstall/pacstall), [Nix](https://github.com/NixOS/nix) and [nyaa](https://git.kreatea.space/kreato-linux/nyaa)

Crackle is a client which allows apt users to install stuff in their home directory, following the [XDG Base Directory specification](https://www.freedesktop.org/software/systemd/man/file-hierarchy.html#Home%20Directory).
 
## Installation

The project is currently a bunch of bash scripts, as such installation relatively simple~
- Download the code

[![download](https://raw.githubusercontent.com/Fuseteam/linus-proof/main/images/download.png)](https://github.com/tuxecure/crackle/releases/latest/download/crackle.zip)

- open a terminal
- run `unzip Downloads/crackle.zip -d crackle`
- run `crackle/crackle setup`
- ???
- profit

## Usage

To run the program, specify the operation, and the package to act on.

```bash
crackle
	install $PKG
	download $PKG
	crack $PKG
	search $PKG
	show $PKG
	remove $PKG
	sudo $BIN
	sudok $BIN
	list
	clean
	update
	upgrade
	setup
	debug
	nuke
```

Essentially, what each command does is what you would expect from using apt as usual, but with amendments for installing things locally, instead of system-wide.

Crackle specific commands:
- `setup`: Automagically configures and installs/upgrades crackle
- `debug`: Shows some debugging information. Doesn't do any changes to the system.
- `crack`: this will extract the package `$PKG` and it's dependencies to `$HOME/packages/$PKG` for easy inspection, usefull to see the file tree or navigate through the various files associated with the package or its dependencies
- `sudo`: this will make a symlink of the binary $BIN to `/root/.local/bin` for use with `sudo -i $BIN`
- `sudok`: this will remove the symlink of the binary $BIN from `/root/.local/bin`
- `click`: this will build a click package from the downloaded deb packages
- `reinstall`: this is equivalent to `apt install --reinstall $PKG`
- `nuke`: Automagically remove everything crackle related from the system

## Limitations

the following are the limitations of crackle:
- crackle doesn't work on systems with a readwrite rootfs
- crackle does not resolve dependencies when removing packages, dependencies have to be removed by name.
- crackle doesn't know how to deal with all packages, so it may be hit or miss please report packages that don't work on [GitLab](https://gitlab.com/tuxecure/crackle-apt/crackle)
- crackle needs to set up the correct environment in order for packages to find their files and libraries as such it is sometimes required to log off and back for them to work as intended

## Support

Support, question and suggestions for crackle can be filed on [GitLab](https://gitlab.com/tuxecure/crackle-apt/crackle). There is also a discussion & support group on [Telegram](https://t.me/CrackleApt)

## Status

Crackle should be considered Alpha, as packages are not aware of crackle they need to be patched to tell them where to find their files before they can work.

## Configuration

The installed packages will be found under `~/$HOME/.local/share/crackle`, modify the runtime configuration to change this, or pass in the `$CRACKLERC` variable to override.

Note that the configuration location for packages by default is in `$XDG_CONFIG_HOME/crackle`, as expected. The same goes for this package, found under `$XDG_CONFIG_HOME/.config/crackle/cracklerc`

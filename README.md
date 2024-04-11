# Crackle

> **NOTE** This project is being migrated to Rust. While the bash version is still maintained, it will eventually™ be superceded by the rust version

A project started by Fuseteam, inspired by [Pacstall](https://github.com/pacstall/pacstall), [Nix](https://github.com/NixOS/nix) and [nyaa](https://git.kreatea.space/kreato-linux/nyaa)

Crackle is a client which allows apt users to install stuff in their home directory, following the XDG Base Directory specification.
 
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
	clean
	setup
	debug
	nuke
```

Essentially, what each command does is what you would expect from using apt as usual, but with amendments for installing things locally, instead of system-wide.

Crackle specific commands:
- `setup`: Automagically configures and installs/upgrades crackle
- `debug`: Shows some debugging information. Doesn't do any changes to the system.
- `crack`: this will extract the package `$PKG` and it's dependencies to `$HOME/packages/$PKG` for easy inspection, usefull to see the file tree or navigate through the various files associated with the package or its dependencies
- `click`: this will build a click package from the downloaded deb packages
- `reinstall`: this is equivalent to `apt install --reinstall $PKG`
- `nuke`: Automagically remove everything crackle related from the system`*`

`*` except the references to it in `~/.bash_completion`. all those references are documented in crackle.conf

## Limitations

the following are the limitations of crackle:
- currently crackle starts all gui apps with xmir for the sake of running them on Ubuntu Touch
- crackle doesn't work on systems with a readwrite rootfs
- currently crackle doesn't know how to remove packages
- crackle doesn't know how to deal with all packages, so it may be hit or miss please report packages that don't work on gitlab
- crackle needs to set up the correct environment in order for packages to find their files and libraries as such it is sometimes required to log off and back for them to work as intended

## Support

Support, question and suggestions for crackle can be filed on [GitLab](https://gitlab.com/tuxecure/crackle-apt/crackle). There is also a discussion & support group on [Telegram](https://t.me/CrackleApt)

## Status

Crackle should considered Alpha, packages may or may not work and crackle is unable to remove packages, it can only remove itself and all the packages it installed with `crackle nuke`.

For 0.3.x considerations are being made to restructure how crackle installs packages to facililate package removal. However this update may require the user to run crackle nuke first, which will nuke all packages installed with crackle. But nothing is set in stone yet

## Configuration

The installed packages will be found under `~/$HOME/.local/share/crackle`, modify the runtime configuration to change this, or pass in the `$CRACKLERC` variable to override.

Note that the configuration location for packages by default is in `$XDG_CONFIG_HOME/crackle`, as expected. The same goes for this package, found under `$XDG_CONFIG_HOME/.config/crackle/cracklerc`

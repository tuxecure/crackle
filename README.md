# Crackle

> **NOTE** if you were using crackle before v0.5 you will need to nuke your crackle install first before installing

A project started by Fuseteam, inspired by [Pacstall](https://github.com/pacstall/pacstall), and [nyaa](https://git.kreatea.space/kreato-linux/nyaa)

Crackle is a client which makes possible to setup nix home manager on Ubuntu Touch, by utilizing the [XDG Base Directory specification](https://www.freedesktop.org/software/systemd/man/file-hierarchy.html#Home%20Directory).
 
## Installation

The project is currently a bunch of bash scripts, as such installation relatively simple~
- Download the code

[![download](https://raw.githubusercontent.com/Fuseteam/linus-proof/main/images/download.png)](https://github.com/tuxecure/crackle/releases/latest/download/crackle.zip)

- open a terminal
- run `unzip Downloads/crackle.zip -d crackle`
- run `crackle/crackle setup`
- ???
- profit

### One liner

```bash
wget https://github.com/tuxecure/crackle/releases/latest/download/crackle.zip && unzip crackle.zip -d crackle && crackle/crackle setup
```

## Usage

To run the program, specify the operation, and the package to act on.

```bash
crackle
	- setup
	- debug
	- crack $PKG
	- sudo $BIN
	- sudok $BIN
	- click $PKG
	- clean
	- install
	- remove
	- update
	- list
	- nuke
	- help
```
Crackle commands:
- `setup`: Automagically configures and installs crackle, nix and home-manager
- `debug`: Shows some debugging information. Doesn't do any changes to the system.
- `click debug`: Shows some debugging information about the click configuration. Doesn't do any changes to the system.
- `sudo debug`: Shows some debugging information about the sudo configuration. Doesn't do any changes to the system.
- `crack`: this will extract the package `$PKG` and it's dependencies to `$HOME/packages/$PKG` for easy inspection, usefull to see the file tree or navigate through the various files associated with the package or its dependencies
- `sudo`: this will make a symlink of the binary $BIN to `/root/.local/bin` for use with `sudo -i $BIN` or if avaialble `/snap/bin` for use with `sudo $BIN`
- `sudok`: this will remove the symlink of the binary $BIN created by `crackle sudo $BIN`
- `click`: this will build a click package from the downloaded deb packages
- `clean`: run `nix-collect-garbage` and removed all apt related directories and broken symlinks
- `install`: adds (a) package(s) to `~/.config/home-manager/home.nix` and runs `home-manager switch` to activate the package(s)
- `remove`: remove (a) package(s) to `~/.config/home-manager/home.nix` and runs `home-manager switch` to remove the package(s)
- `update`: run `nix-channel --update` to get the latest updates from the nix cache and runs `home-manager switch` to activate the newer version
- `list`: list installed applications
- `nuke`: Automagically removes everything crackle installed from the system
- `help`: shows the available commands of crackle

## Limitations

the following are the limitations of crackle:
- expects `apt` for the installation of curl and xz, needed for setting up nix

## Support

Support, question and suggestions for crackle can be filed on [GitLab](https://gitlab.com/tuxecure/crackle-apt/crackle). There is also a discussion & support group on [Telegram](https://t.me/CrackleApt)

## Status

Crackle should be considered Beta, there may be some lingering bugs and/or edge cases.

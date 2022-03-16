# Crackle

> **NOTE** This project is being migrated to Rust. While the bash version is still maintained, it will eventually™ be superceded by the rust version

An project by Fuseteam and others.

Crackle is a client which allows apt users to install stuff in their home directory, following the XDG Base Directory specification.
 
## Installation

The project is currently a bunch of bash scripts, as such installation relatively simple~
- Download the code

[![download](https://github.com/Fuseteam/linus-proof/blob/main/images/download.png)](https://github.com/tuxecure/crackle/releases/latest/download/crackle.zip)

- open a terminal
- run `cd Downloads`
- run `unzip crackle.zip`
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
	remove $PKG
	search $PKG
	show $PKG
	clean
	setup
	debug
```

Essentially, what each command does is what you would expect from using apt as usual, but with amendments for installing things locally, instead of system-wide.

Crackle specific commands:
- `setup`: Automagically reads the user configuration and saves it into cracklerc
- `setup`: Automagically reads the user configuration and saves it into cracklerc
- `crack`: this will extract the package `$PKG` and it's dependencies to `$HOME/packages/$PKG` for easy inspection, usefull to see the file tree or navigate through the various files associated with the package or its dependencies

## Configuration

The installed packages will be found under `~/$HOME/.local/share/crackle`, modify the runtime configuration to change this, or pass in the `$CRACKLERC` variable to override.

Note that the configuration location for packages by default is in `$XDG_CONFIG_HOME/crackle`, as expected. The same goes for this package, found under `$XDG_CONFIG_HOME/.config/crackle/cracklerc`

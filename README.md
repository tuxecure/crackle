# Crackle


An idea by Fuseteam and others.

Crackle is a client which allows apt users to install stuff in their home repositories, following the XDG Base Directory specification.
 
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
`setup`: Automagically reads the user configuration and saves it into cracklerc
`debug`: Shows some debugging information. Doesn't do any changes to the system.

## Requirements
You need the Rust compiler. And a cup of water which you should be drinking right now.


## Installation

Download this repository into wherever you want, and build it with make. Make sure you have `$XDG_CONFIG_HOME` set, as it is needed.
```sh
git clone git@github.com:tuxecure/crackle.git
git checkout rust
cd crackle/
make install
```

If you want to, you could build it manually, everything is explained in the Makefile.

The tldr, though, is that binaries are created into `build/`, a copy of the repository's `config/` files is placed into `$XDG_CONFIG_HOME/crackle/`, and a symlink to the generated `build/crackle` is added to `~/.local/bin/crackle`. You can edit all these locations easily in the header of the Makefile. That's it.

Oh, and also, you need to have `rustc` (the Rust compiler) in your $PATH. Install that however your distribution requires you to.


## Configuration

The installed packages will be found under `~/$HOME/packages`, modify the runtime configuration to change this, or pass in the `$CRACKLERC` variable to override.

Note that the configuration location for packages by default is in `$XDG_CONFIG_HOME/crackle`, as expected. The same goes for this package, found under `$XDG_CONFIG_HOME/.config/crackle/cracklerc`



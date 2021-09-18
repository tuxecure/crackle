# Crackle

A project by Fuseteam.

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

## Configuration

The installed packages will be found under `~/$HOME/packages`, modify the runtime configuration to change this, or pass in the `$CRACKLERC` variable to override.

Note that the configuration location for packages by default is in `$XDG_CONFIG_HOME/crackle`, as expected. The same goes for this package, found under `$XDG_CONFIG_HOME/.config/crackle/cracklerc`



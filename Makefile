#
SRC_PATH:=src
BUILD_PATH:=build
CONF_PATH:=config
SRC_FILES = $(wildcard ${SRC_PATH}/*.rs)
BIN_FILES = $(BUILD_PATH)/$(notdir $(SRC_FILES:.rs=))

INSTALL_PATH:=${HOME}/.local/bin
CONFIG_PATH:=${XDG_CONFIG_HOME}

.PHONY: clean purge

.DEFAULT: build
	

build: $(BIN_FILES)
	@# There is probably a cleaner way of doing this.
	@# We should already have the binary files under $BUILD_PATH/
	@# Although LTO could be a factor
	rustc --out-dir ${BUILD_PATH} ${SRC_FILES} --crate-name crackle

$(BUILD_PATH)/%: $(SRC_PATH)/%.rs
	@# Generate the binaries for all the source files
	@# TODO: For some reason, `make main`, for instance, says
	@# it's up to date, even when the file doesn't exist.
	rustc --out-dir ${BUILD_PATH} $<

install: 
	@# symbolic, force if exists
	ln -s $(shell readlink -f ./build/crackle) ${INSTALL_PATH}/crackle 

config: ${CONF_FILES}
	@# recursive
	cp -r ${CONF_PATH} ${XDG_CONFIG_HOME}/crackle

clean:
	rm -rf ./build/*

purge: clean
	rm -rf ${XDG_CONFIG_HOME}/crackle
	unlink ${INSTALL_PATH}/crackle

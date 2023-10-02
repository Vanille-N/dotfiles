USER = vanille
HOME = /home/${USER}
CONF = ${HOME}/.config
ENV = ${HOME}/.env

all: structure
include structure.mk

structure.mk: ./sync.sh ./macros-sync.sh
	./$<

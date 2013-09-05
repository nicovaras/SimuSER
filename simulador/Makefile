# This file is part of SimuSER.
#
# SimuSER is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SimuSER is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SimuSER.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2013 Federico Raimondo, Leandro Nuñez, Nicolás Rosner,
# Mariano Moscato, Diego Fernández Slezak, Ignacio Kovacs, Nicolas Varaschín
#
# Department of Computer Sciences, FCEyN, University of Buenos Aires

export  LC_ALL=C
.PHONY: clean 

VERSION=version.py
SYS:=$(shell gcc -dumpmachine)
ifneq (, $(findstring mingw, $(SYS)))
CP=copy
RM=del /Q /F
RMDIR=rmdir /s /q
SIMU=dist\simulador.exe
SEP=\\
SVNVERSION=$(shell echo $$WCREV$$ > rev.in && subwcrev . rev.in rev.out > nul && type rev.out)
else
RM=rm -f
SIMU=dist/simulador
SVNVERSION=$(shell ./evalrev)
endif

all: clean $(SIMU)


ifneq (, $(findstring mingw, $(SYS)))
$(SIMU): $(VERSION)
	python py2exe_setup.py
	$(CP) config.txt dist$(SEP)
	$(CP) img dist$(SEP)img
	$(CP) background dist$(SEP)background
	$(RMDIR) dist$(SEP)tests

$(VERSION):
	echo svnversion="${SVNVERSION}" > $@
else
$(SIMU): $(VERSION)
	mkdir -p dist/
	cp *.py dist/
	cp config.txt dist/
	cp -r img dist/
	cp -r background dist/
	echo "#!/bin/bash" > dist/simulador
	echo 'DIR="$$( cd "$$( dirname "$${BASH_SOURCE[0]}" )" && pwd )"' >> dist/simulador
	echo 'cd $$DIR' >> dist/simulador
	echo "python simulador.py \$$@" >> dist/simulador
	chmod +x dist/simulador 
$(VERSION):
	echo "svnversion=\"${SVNVERSION}\"" > $@
endif

ifneq (, $(findstring mingw, $(SYS)))
clean: clean-win
else ifneq (, $(findstring darwin, $(SYS)))
clean: clean-mac
else ifneq (, $(findstring linux, $(SYS)))
clean: clean-nix
endif

clean-win:
	if exist "$(SIMU)" $(RM) "$(SIMU)"
	if exist $(VERSION) $(RM) $(VERSION)

clean-mac:
	$(RM) -r dist $(SIMU) $(VERSION)

clean-nix:
	$(RM) -r dist $(SIMU) $(VERSION)

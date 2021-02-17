#!/usr/bin/env bash
##############################################################################
# Genera la documentacion de los modulos, requiere la instalacion de oca
# maintainers tools en tu maquina.
# bajalo de aca --> https://github.com/OCA/maintainer-tools y lo instalas asi:
#
# $ git clone git@github.com:OCA/maintainer-tools.git
# $ cd maintainer-tools
# $ virtualenv env
# $ . env/bin/activate
# $ python setup.py install
#
source /opt/maintainer-tools/env/bin/activate
oca-gen-addon-readme \
	--org-name jobiols \
	--repo-name odoo-jeo-ce \
	--branch 8.0 \
	--addons-dir "$PWD" \
	--gen-html

# pylint {} --load-plugins=pylint_odoo -d C0114,C0115,C0116
# ejecutar pylint en cada repositorio
#find ./* -type d -exec pylint {} --load-plugins=pylint_odoo -d C8101 \;

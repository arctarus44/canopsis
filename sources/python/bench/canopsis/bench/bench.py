# -*- coding:utf-8 -*-
# --------------------------------
# Copyright (c) 2016 "Capensis" [http://www.capensis.com]
#
# This file is part of Canopsis.
#
# Canopsis is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Canopsis is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Canopsis.  If not, see <http://www.gnu.org/licenses/>.
# ---------------------------------

"""
1: lookup du python path
2: boucle sur tout les  syspaths python package modules pour trouver les fonctions à bench qui sont déjà dans les modules et les modifier
3: getattr/setattr sur les fonctions pour appliquer le décorateur
4: get_task pour vérifier si c'est une tache
5: faire un register_task pour applique le décorateur à la task
6: refaire un passage dans les syspath package modules
7: setattr sur les task pour appliquer le décorateur
"""


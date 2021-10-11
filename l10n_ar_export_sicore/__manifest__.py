##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Exportacion sicore',
    'version': '13.0.1.0.0',
    'author':  'Moldeo Interactive, jeo Soft',
    'category': 'Accounting',
    'sequence': 14,
    'summary': '',
    'license': 'AGPL-3',
    'images': [
    ],
    'depends': [
        'base',
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/account_view.xml'
    ],
    'test': [
    ],
    "excludes": ['web_enterprise'],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import api, models


class WizardModel(models.TransientModel):
    _name = "module.wizard_model"

    def action_accept(self):
        self.ensure_one()
        self.do_something_useful()

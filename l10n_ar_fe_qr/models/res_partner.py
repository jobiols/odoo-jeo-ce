##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from openerp import models, api, _
from openerp.exceptions import Warning as UserError
@api.multi
class ResPartner(models.Model):
    _inherit = 'res.partner'

    def get_id_number_sanitize(self):
        """ Sanitize the identification number. Return the digits/interger value of
            the identification number
        """
        for rec in self:
            id_number = rec.document_number.replace('.', '').replace(' ', '')
            id_number = id_number.replace('-', '')
            if not id_number.isdigit():
                raise UserError(_('El numero de cuit es invalido para %s') % rec.name)
            return int(id_number)

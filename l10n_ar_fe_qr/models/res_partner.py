# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

#from io import BytesIO
#import qrcode
from openerp import models, api, _
#from openerp.tools import float_repr
from openerp.exceptions import Warning as UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.one
    def get_id_number_sanitize(self):
        """ Sanitize the identification number. Return the digits/interger value of
            the identification number
        """
        id_number = self.document_number.replace('.', '').replace(' ', '')
        id_number = id_number.replace('-', '')
        if not id_number.isdigit():
            raise UserError(_('El numero de cuit es invalido para %s') % self.name)
        res = int(id_number)
        return res

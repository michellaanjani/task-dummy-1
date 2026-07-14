from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"
    sale_description = fields.Char(string='Sale Description')
    
    def unlink(self):
        for order in self:
            # Cek jika status bukan draft/cancel
            if order.state not in ['draft', 'cancel']:       
                order.write({'state': 'cancel'})
                
        # Se
        # karang panggil super, karena status sudah 'cancel', super akan mengizinkan delete
        return super(SaleOrder, self).unlink()
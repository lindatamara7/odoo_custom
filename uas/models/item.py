from odoo import models, fields, api, _
from odoo.exceptions import UserError

class item(models.Model):
    _name= 'uas.item'
    _description= 'Daftar bahan baku di perusahaan'

    name = fields.Char('ID item', size=64, required=True, index=True,states={'draft': [('readonly', False)]})
    namaitem = fields.Char('Nama item', size=64, required=True, index=True,states={'draft': [('readonly', False)]})
    # jumlah = fields.Char('Jumlah', size=64, required=True, index=True,
    #                       states={'draft': [('readonly', False)]})
    harga = fields.Integer('Harga', size=64, required=True, index=True, readonly=False,
                            states={'draft': [('readonly', False)]})
    _sql_constraints = [('name_unik', 'unique(name)', _('Id must be unique!'))]
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'
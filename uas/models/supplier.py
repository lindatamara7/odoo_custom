from odoo import models, fields, api, _
from odoo.exceptions import UserError

class supplier(models.Model):
    _name= 'uas.supplier'
    _description= 'Daftar supplier di perusahaan'
    _rec_name = 'namasup'

    name = fields.Char('ID Supplier', size=64, required=True, index=True, states={})
    namasup = fields.Char('Nama Supplier', size=64, required=True, index=True,states={'draft': [('readonly', False)]})
    alamat = fields.Char('Alamat', size=64, required=True, index=True,states={'draft': [('readonly', False)]})
    tlp = fields.Char('No Telepon', size=64, required=True, index=True,states={'draft': [('readonly', False)]})
    email = fields.Char('Email', size=64, required=True, index=True,states={'draft': [('readonly', False)]})
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
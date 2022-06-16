from odoo import models, fields, api, _
from odoo.exceptions import UserError

class delivery(models.Model):
    _name= 'uas.delivery'
    _description= 'Daftar delivery pesanan di perusahaan'
    _rec_name = 'nama'

    name = fields.Char('ID delivery', size=64, required=True, index=True, states={})
    nama = fields.Char('Nama pengirim', size=64, required=True, index=True,states={'draft': [('readonly', False)]})
    ekspedisi = fields.Selection([('jne', 'JNE'),
                               ('sicepat', 'Sicepat')], 'Ekspedisi', required=True, readonly=False, default='active')
    alamat = fields.Char('Alamat', size=64, required=True, index=True,states={'draft': [('readonly', False)]})
    date_dl = fields.Date('Tanggal pengiriman', default=fields.Date.context_today, help='Please fill the date here',
                          readonly=False, states={'draft': [('readonly', False)]})
    # _sql_constraints = [('name_unik', 'unique(name)', _('Id must be unique!'))]

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
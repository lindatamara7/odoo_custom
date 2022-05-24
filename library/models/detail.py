from odoo import models, fields, api, _

class detail(models.Model):
    _name= 'library.detail'
    _description= 'Detail transaksi peminjaman atau pengembalian buku di Perpustakaan A'

    name = fields.Char('ID Detail Transaksi', size=64, required=True, index=True, readonly=True,states={'draft': [('readonly', False)]})
    transaksi_ids = fields.Many2one('library.transaksi', string='Transaction_id', domain="[('state', '=', 'done')]")
    buku_ids = fields.Many2one('library.buku', string='Buku_id', domain="[('state', '=', 'done'),('status', '=', 'available')]")
    subtotal = fields.Integer("Subtotal", related='buku_ids.biaya')
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


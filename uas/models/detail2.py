from odoo import models, fields, api, _

class detail2(models.Model):
    _name= 'uas.detail2'
    _description= 'Detail transaksi pembelian bahan baku di perusahaan A'

    name = fields.Char('ID Detail Transaksi', size=64, required=True, index=True,states={'draft': [('readonly', False)]})
    transaksi2_ids = fields.Many2one('uas.transaksi2', string='Transaction_id')
    item_ids = fields.Many2one('uas.item', string='item_id')
    jumlah = fields.Integer('Jumlah', size=64, required=True, index=True, readonly=False,
                           states={'draft': [('readonly', False)]})
    hrg = fields.Integer(related='item_ids.harga')
    subtotal = fields.Integer("subtotal", compute="_compute_subtotal", store=True, default=0)
    # _sql_constraints = [('name_unik', 'unique(name)', _('Id must be unique!'))]
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')

    @api.depends('jumlah', 'hrg')
    def _compute_subtotal(self):
        for i in self:
            if i.jumlah:
                a = float(i.jumlah)
                b = float(i.hrg)
                i.subtotal = a * b

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'


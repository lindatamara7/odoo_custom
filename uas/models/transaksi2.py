from odoo import models, fields, api, _
from odoo.exceptions import UserError

class transaksi2(models.Model):
    _name= 'uas.transaksi2'
    _description= 'Transaksi pembelian bahan baku di perusahaan A'

    name = fields.Char('ID Transaksi', size=64, required=True, index=True,states={'draft': [('readonly', False)]})
    employee_ids = fields.Many2one('uas.employee', string='Nama employee', domain="[('state', '=', 'confirmed')]")
    supplier_ids = fields.Many2one('uas.supplier', string='Nama supplier', domain="[('state', '=', 'confirmed')]")
    delivery_ids = fields.Many2one('uas.delivery', string='Nama pengirim', domain="[('state', '=', 'confirmed')]")
    detail2_ids = fields.One2many("uas.detail2", "transaksi2_ids", string='Detail_id')
    date_tr = fields.Date('Tanggal transaksi', default=fields.Date.context_today, help='Please fill the date here',
                       readonly=False, states={'draft': [('readonly', False)]})
    # total = fields.Integer("Total", compute="_compute_total", store=True, default=0)
    _sql_constraints = [('name_unik', 'unique(name)', _('Id must be unique!'))]
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')

    # @api.depends('detail2_ids.subtotal')
    # def _compute_total(self):
    #     for i in self:
    #         nilai = {
    #             "total": 0
    #         }
    #         for j in i.detail2_ids:
    #             a = float(j.subtotal)
    #             nilai['total'] += a
    #         i.update(nilai)

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'


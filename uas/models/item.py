from odoo import models, fields, api, _
from odoo.exceptions import UserError

class item(models.Model):
    _name= 'uas.item'
    _description= 'Daftar bahan baku di perusahaan'

    name = fields.Char('ID item', size=64, required=True, index=True,states={'draft': [('readonly', False)]})
    namaitem = fields.Char('Nama item', size=64, required=True, index=True,states={'draft': [('readonly', False)]})
    detail2_ids = fields.One2many('uas.detail2', 'item_ids', string='Detail_id')
    jml = fields.Integer("Jumlah", compute="_compute_jumlah", store=True, default=0)
    harga = fields.Integer('Harga', size=64, required=True, index=True, readonly=False,
                            states={'draft': [('readonly', False)]})
    _sql_constraints = [('name_unik', 'unique(name)', _('Id must be unique!'))]
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')

    @api.depends("detail2_ids.jumlah")
    def _compute_jumlah(self):
        for i in self:
            val = {
                "jml": 15,
            }

            for j in i.detail2_ids:
                val['jml'] += j.jumlah
        i.update(val)


    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'
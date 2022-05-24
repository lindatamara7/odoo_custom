from odoo import models, fields, api, _

class transaksi(models.Model):
    _name= 'library.transaksi'
    _description= 'Transaksi peminjaman atau pengembalian buku di Perpustakaan A'

    name = fields.Char('ID Transaksi', size=64, required=True, index=True, readonly=True,states={'draft': [('readonly', False)]})
    customer = fields.Many2one('res.partner', 'Customer', readonly=True,states={'draft': [('readonly', False)]})
    date_pinjam = fields.Date('Tanggal pinjam', default=fields.Date.context_today, help='Please fill the date here',
                       readonly=False, states={'draft': [('readonly', False)]})
    date_kembali_seharusnya = fields.Date('Tanggal kembali seharusnya', default=fields.Date.context_today, help='Please fill the date here',readonly=False, states={'draft': [('readonly', False)]})
    date_kembali_real = fields.Date('Tanggal kembali real', default=fields.Date.context_today,
                                          help='Please fill the date here',
                                          readonly=False, states={'draft': [('readonly', False)]})
    durasi = fields.Integer('Durasi sewa', size=64, required=True, index=True, readonly=False,
                            states={'draft': [('readonly', False)]})
    denda = fields.Integer("Denda", compute="_compute_denda", store=True, default=0)
    jumlah = fields.Integer('Jumlah buku', size=64, required=True, index=True, readonly=False,
                            states={'draft': [('readonly', False)]})
    total = fields.Integer("Total", compute="_compute_total", store=True, default=0)
    detail_ids = fields.One2many("library.detail", "transaksi_ids", string='Detail_id')
    _sql_constraints = [('name_unik', 'unique(name)', _('Id must be unique!'))]
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')

    @api.depends('date_kembali_seharusnya', 'date_kembali_real')
    def _compute_denda(self):
        if self.date_kembali_seharusnya and self.date_kembali_real:
            date_kembali_seharusnya = fields.Datetime.from_string(self.date_kembali_seharusnya)
            date_kembali_real = fields.Datetime.from_string(self.date_kembali_real)
            self.denda = abs((date_kembali_real - date_kembali_seharusnya).days) * 5000

    @api.depends('detail_ids.subtotal', 'denda')
    def _compute_total(self):
        for i in self:
            nilai = {
                "total": 0
            }
            for j in i.detail_ids:
                nilai['total'] = j.subtotal + i.denda
            i.update(nilai)

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'

    def action_done(self):
        self.state = 'done'
        t = self.env.context
        print(t.get('keterangan'))

    def tes_transaksi(self):
        print("ini transaksi")
        t = self.env.context.get("keterangan")
        print(t)

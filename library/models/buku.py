from odoo import models, fields, api, _
from odoo.exceptions import UserError


class buku(models.Model):
    _name= 'library.buku'
    _description= 'Daftar buku di Perpustakaan A'

    name = fields.Char('ID Buku', size=64, required=True, index=True, readonly=True, default="new", states={})
    judul = fields.Char('Judul Buku', size=64, required=True, index=True, readonly=True,states={'draft': [('readonly', False)]})
    tahun = fields.Char('Tahun terbit', size=64, required=True, index=True, readonly=True,states={'draft': [('readonly', False)]})
    penulis = fields.Char('Penulis', size=64, required=True, index=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')
    biaya = fields.Integer('Biaya sewa', size=64, required=True, index=True, readonly=False, states={'draft': [('readonly', False)]})
    status = fields.Selection([('available', 'Available'),
                             ('unavailable', 'Unavailable')], 'Status', required=True, readonly=False, default='available')
    date = fields.Date('Date Upload', default=fields.Date.context_today, help='Please fill the date here', readonly=True,states={'draft': [('readonly', False)]})
    #_sql_constraints = [('name_unik', 'unique(name)', _('Id must be unique!'))]
    @api.depends("voting_ids", "voting_ids.vote", "voting_ids.state") #kapan ngulang fungsi e->lek ... brubah
    def _compute_vote(self):
        for idea in self.filtered(lambda s:s.state=='done'):
            val = {
                "total_yes": 0,
                "total_no": 0,
                "total_abstain": 0,
            }
            for rec in idea.voting_ids.filtered(lambda s:s.state=='voted'):
                if rec.vote == 'yes':
                    val['total_yes'] += 1
                elif rec.vote == 'no':
                    val['total_no'] += 1
                else:
                    val['total_abstain'] += 1
            idea.update(val)

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'
        if self.name == 'new' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "library.buku")])
            if not seq:
                raise UserError(_("library.buku sequence not found, please create library.buku sequence"))
            self.name = seq.next_by_id(sequence_date=self.date)

    def action_settodraft(self):
        self.state = 'draft'

    def action_tes(self):
        #cth ambil active user
        print(self.env.user.name)
        #cth ambil active company
        print(self.env.company.name)
        #cth common orm method search
        a = self.env["res.partner"].search([('name', 'ilike', 'gemini')])
        a = self.env["res.partner"].search([], limit=2)

        # contoh context
        print(self.env.context.get('lang'))
        t = self.env.context.copy()
        t["keterangan"] = 'Ideku'
        self.with_context(t).action_done()

        b = self.env["library.transaksi"]
        b.with_context(t).tes_transaksi()

        # cth query select
        query = "select name from res_partner order by name desc limit 3"
        # besar ke kcl cm ambil 3
        self.env.cr.execute(query)
        reel = self.env.cr.fetchall()
        #for data in res:
            #print(data[0])

        query = "update idea state='done' where state in ('confirmed', 'draft')"
        self.env.cr.execute(query)
        self.env.cr.rollback()

        query = "delete idea where state='draft'"
        self.env.cr.execute(query)
        self.env.cr.rollback()

    def action_done(self):
        self.state = 'done'
        t = self.env.context
        print(t.get('keterangan'))
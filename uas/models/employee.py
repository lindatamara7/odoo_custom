from odoo import models, fields, api, _
from odoo.exceptions import UserError

class employee(models.Model):
    _name= 'uas.employee'
    _description= 'Daftar employee di perusahaan'
    _rec_name = 'namakar'

    name = fields.Char('id employee', size=64, required=True, index=True)
    namakar = fields.Char('Nama employee', size=64, required=True, index=True,states={'draft': [('readonly', False)]})
    alamat = fields.Char('Alamat', size=64, required=True, index=True,
                          states={'draft': [('readonly', False)]})
    date = fields.Date('Tanggal Lahir', default=fields.Date.context_today, help='Please fill the date here',
                        states={'draft': [('readonly', False)]})
    tlp = fields.Char('No Telepon', size=64, required=True, index=True, states={'draft': [('readonly', False)]})
    email = fields.Char('Email', size=64, required=True, index=True,states={'draft': [('readonly', False)]})
    line_ids = fields.One2many('uas.employee.lines', 'employee_id', string='employee', readonly=True,
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

    def action_wiz_uas(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Wizard Employee'),
            'res_model': 'wiz.uas.employee',
            'view_mode': 'form',
            'target': 'new',
            # 'context': {'active_id': self.id},
        }
class employee_lines(models.Model):
    _name = 'uas.employee.lines'
    _description = 'class untuk menyimpan transaksi employee'
    employee_id = fields.Many2one('uas.employee', string='employee', ondelete="cascade")
    tr_id = fields.Many2one('uas.transaksi2', string='transaksi', ondelete="restrict")
    status = fields.Selection([('on process', 'on process'),
                              ('done', 'done')])
from odoo import models, fields, api, _

class employee_lines_wiz(models.TransientModel):
    _name = 'wiz.uas.employee.lines'
    _description = 'class untuk menyimpan transaksi employee'

    wiz_header_id = fields.Many2one('wiz.uas.employee', string='employee')
    tr_id = fields.Many2one('uas.transaksi2', String='transaksi')
    ref_employee_lines_id = fields.Many2one('uas.employee.lines')
    status = fields.Selection([('on process', 'on process'),
                              ('done', 'done')])

class wizemployee(models.TransientModel):
    _name = 'wiz.uas.employee'
    _description = 'class untuk menyimpan data employee dan transaksi'

    employee_id = fields.Many2one('uas.employee', String='Employee')
    namakar = fields.Char(related='employee_id.namakar')
    alamat = fields.Char(related='employee_id.alamat')
    date = fields.Date(related='employee_id.date')
    email = fields.Char(related='employee_id.email')
    line_ids = fields.One2many('wiz.uas.employee.lines', 'wiz_header_id', string='List')


    @api.model
    def default_get(self, fields_list):  # ini adalah common method, semacam constructor, akan dijalankan saat create object. Ini akan meng-overwrite default_get dari parent
        res = super(wizemployee, self).default_get(fields_list)
        # res  merupakan dictionary beserta value yang akan diisi, yang sudah diproses di super class (untuk create record baru)
        res['employee_id'] = self.env.context['active_id']
        return res

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        if not self.employee_id:
            return
        vals = []
        line_ids = self.env['wiz.uas.employee.lines']
        for rec in self.employee_id.line_ids:
            line_ids += self.env['wiz.uas.employee.lines'].new({
                'wiz_header_id': self.id,
                'tr_id': rec.tr_id.id,
                'ref_employee_lines_id': rec.id
            })
        self.line_ids = line_ids

    def action_confirm(self):
        for rec in self.line_ids:
            rec.ref_employee_lines_id.status = rec.status






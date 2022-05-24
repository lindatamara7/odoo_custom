from odoo import models, fields, api, _
from odoo.exceptions import UserError


class idea(models.Model):
    _name= 'idea.idea'
    _description= 'class untuk berlatih ttg idea'
    _order = 'date desc'

    name = fields.Char('Number', size=64, required=True, index=True, readonly=True, default='new',states={})
    date = fields.Date('Date Release', default=fields.Date.context_today, help='Please fill the date here', readonly=True,states={'draft': [('readonly', False)]})
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')
    #readonly apa engga ngikuti state (misal abis confirm ada yg ga bs diganti lgi)
    description = fields.Text('Description', readonly=True,states={'draft': [('readonly', False)]})
    active = fields.Boolean('Active', readonly=True,states={'draft': [('readonly', False)]})
    confirm_date = fields.Date('Confirm Date')

    confirm_partner_id = fields.Many2one('res.partner', 'Confirm By', readonly=True)
    sponsor_ids = fields.Many2many('res.partner', string='Sponsors')

    score = fields.Integer('Score', default=0, readonly=True)
    owner = fields.Many2one('res.partner', 'Owner', index=True, readonly=True, states={'draft': [('readonly', False)]})

    voting_ids = fields.One2many('idea.voting', 'idea_id', string='Votes')
    total_yes = fields.Integer("Yes", compute="_compute_vote", store=True, default=0)
    total_no = fields.Integer("No", compute="_compute_vote", store=True, default=0)
    total_abstain = fields.Integer("Abstain", compute="_compute_vote", store=True, default=0)

    @api.depends("voting_ids", "voting_ids.vote", "voting_ids.state")
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
            seq = self.env['ir.sequence'].search([("code", "=", "idea.idea")])
            if not seq:
                raise UserError(_("idea.idea sequence not found, please create idea.idea sequence"))
            self.name = seq.next_by_id(sequence_date=self.date)

    def action_settodraft(self):
        self.state = 'draft'

    # def action_tes(self):
    #     #cth ambil active user
    #     print(self.env.user.name)
    #     #cth ambil active company
    #     print(self.env.company.name)
    #     #cth common orm method search
    #     a = self.env["res.partner"].search([('name', 'ilike', 'gemini')])
    #     a = self.env["res.partner"].search([], limit=2)


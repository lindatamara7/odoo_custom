from odoo import models, fields, api, _
from odoo.exceptions import UserError


class voting(models.Model):
    _name = 'idea.voting'
    _description = 'Voting'
    _order = 'date desc'

    name = fields.Char('Voting Number', size=64, required=True, index=True, default="new")
    date = fields.Date('Voting Date', default=fields.Date.context_today)
    state = fields.Selection([('draft', 'Draft'),
                              ('voted', 'Voted'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')
    vote = fields.Selection([('yes', 'Yes'),
                             ('no', 'No'),
                             ('abstain', 'Abstain')], 'Vote', required=True, readonly=False, default='abstain')
    voter_id = fields.Many2one('res.users', 'Voted By', readonly=True, ondelete="cascade", default=lambda self: self.env.user)
    idea_id = fields.Many2one('idea.idea', string='Idea_id', domain="[('state', '=', 'done'),('active', '=', 'true')]")
    idea_date = fields.Date("Idea Date", related='idea_id.date')

    def action_canceled(self):
        self.state = 'canceled'

    def action_voted(self):
        self.state = 'voted'

        if self.name == 'new' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "idea.idea")])
            if not seq:
                raise UserError(_("idea.idea sequence not found, please create idea.idea sequence"))
            self.name = seq.next_by_id()

    def action_settodraft(self):
        self.state = 'draft'

    @api.model_create_multi
    def create(self, vals_list):
        if self.name == 'new' or not self.name:
            seq = self.env['ir.sequence'].search([("code", "=", "idea.voting")])
            if not seq:
                raise UserError(_("Idea.voting sequence not found, please create idea.voting sequence"))
            for val in vals_list:
                val['name'] = seq.next_by_id()
            return super(voting, self).create(vals_list)

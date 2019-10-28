from odoo import api, fields, models


class CoopMembership(models.Model):
    _name = 'coop.membership'
    _description = 'Cooperative Membership'

    @api.multi
    @api.depends('partner_id.share_ids')
    def _compute_effective_date(self):
        # TODO change it to compute it from the share register
        for membership in self:
            share_ids = membership.partner_id.share_ids.filtered(
                            lambda record:
                            record.structure == membership.structure)
            if share_ids:
                membership.effective_date = share_ids[0].effective_date

    @api.multi
    @api.depends('subscription_request_ids.state')
    def _compute_coop_candidate(self):
        for membership in self:
            if membership.member:
                is_candidate = False
            else:
                sub_request = membership.subscription_request_ids.filtered(
                                lambda record:
                                record.structure == membership.structure)
                if len(sub_request.filtered(lambda record:
                                            record.state == 'done')) > 0:
                    is_candidate = True
                else:
                    is_candidate = False

            membership.coop_candidate = is_candidate

    partner_id = fields.Many2one('res.partner',
                                 string="Cooperator")
    structure = fields.Many2one(comodel_name='res.partner',
                                string="Platform Structure",
                                domain=[('is_platform_structure', '=', True)])
    cooperator_number = fields.Integer(string='Cooperator Number')
    member = fields.Boolean(string='Effective cooperator',
                            help="Check this box if this cooperator"
                            " is an effective member.")
    coop_candidate = fields.Boolean(string="Cooperator candidate",
                                    compute="_compute_coop_candidate",
                                    store=True,
                                    readonly=True)
    old_member = fields.Boolean(string='Old cooperator',
                                help="Check this box if this cooperator is"
                                " no more an effective member.")
    subscription_request_ids = fields.One2many(related='partner_id.subscription_request_ids') # noqa
    effective_date = fields.Date(string="Effective date",
                                 compute=_compute_effective_date,
                                 store=True)

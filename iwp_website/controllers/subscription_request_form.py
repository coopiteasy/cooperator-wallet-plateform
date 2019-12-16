# Copyright 2019 Coop IT Easy SCRLfs <http://coopiteasy.be>
#   Rémy Taymans <remy@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

"""Subscription Request Form"""

from datetime import date

from odoo.http import request
from odoo.tools.translate import _

from .form import Choice, Field, Form, FormValidationError
from .tools import monetary_to_text


class SubscriptionRequestForm(Form):
    """Form to create new Subscription Request for a user"""

    def __init__(self, **kw):
        super().__init__(**kw)
        context = kw["context"]
        self.fields["share_type"] = Field(
            label="Share Type",
            required=True,
            template="iwp_website.selection_field",
            choices=self._choices_share_type,
        )
        self.fields["quantity"] = Field(
            label="Quantity",
            required=True,
            att={"min": 1},
            validators=[self._validate_quantity],
            template="iwp_website.input_field",
            input_type="number",
        )
        self.fields["total_amount"] = Field(
            label="Total Amount",
            readonly=True,
            template="iwp_website.input_field",
            input_type="text",
        )
        self.fields["data_policy_approval"] = Field(
            label="Data Policy",
            content=context["struct"].data_policy_approval_text,
            required=True,
            template="iwp_website.checkbox_field",
        )
        self.fields["internal_rules_approval"] = Field(
            label="Internal Rules",
            content=context["struct"].internal_rules_approval_text,
            required=True,
            template="iwp_website.checkbox_field",
        )
        self.fields["financial_risk_approval"] = Field(
            label="Financial Risks",
            content=context["struct"].financial_risk_approval_text,
            required=True,
            template="iwp_website.checkbox_field",
        )

    def clean(self):
        """Check that user does not buy to much shares."""
        cleaned_data = super().clean()
        if "share_type" not in cleaned_data:
            return cleaned_data
        if "quantity" not in cleaned_data:
            return cleaned_data
        user = self.context.get("user")
        share_type = (
            request.env["product.template"]
            .sudo()
            .browse(int(cleaned_data["share_type"]))
        )
        amount = share_type.list_price * cleaned_data["quantity"]
        max_amount = share_type.can_buy_max_amount(user.commercial_partner_id)
        if 0 < max_amount < amount:
            raise FormValidationError(
                _(
                    "You cannot buy so much shares. The maximum amount is %d."
                    % max_amount
                )
            )
        min_amount = share_type.can_buy_min_amount(user.commercial_partner_id)
        if min_amount > amount:
            raise FormValidationError(
                _(
                    "You have to buy more shares. Minimum amount is %d."
                    % min_amount
                )
            )
        return cleaned_data

    def _validate_quantity(self, value):
        if value <= 0:
            raise FormValidationError("Quantity can not be nul or negative.")

    def _choices_share_type(self):
        user = self.context.get("user")
        struct = self.context.get("struct")
        if user.commercial_partner_id.is_company:
            share_types = struct.share_type_ids.filtered(
                lambda r: r.display_on_website and r.by_company
            )
        else:
            share_types = struct.share_type_ids.filtered(
                lambda r: r.display_on_website and r.by_individual
            )
        choices = []
        if struct:
            for st in share_types:
                choices.append(
                    Choice(
                        value=st.id,
                        display="%s - %s"
                        % (st.name, monetary_to_text(st.list_price)),
                        att={
                            "data-price": st.list_price,
                            "data-max_amount": st.can_buy_max_amount(
                                user.commercial_partner_id
                            ),
                            "data-min_amount": st.can_buy_min_amount(
                                user.commercial_partner_id
                            ),
                        },
                        obj=st,
                    )
                )
        return choices

# Copyright 2025 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models

MAPPING_TYPE = {
    "inbound": "register_customer_payment_state",
    "outbound": "register_vendor_payment_state",
}


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    def _check_payment_draft(self):
        return bool(self.env.company[MAPPING_TYPE.get(self.payment_type)] == "draft")

    def _create_payments(self):
        payments = super()._create_payments()
        if self._check_payment_draft():
            payments.filtered(lambda p: p.state != "draft").action_draft()
        return payments

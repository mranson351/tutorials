from odoo import models, Command


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def set_sold(self):
        for record in self:
            self.env["account.move"].create(
                {
                    "partner_id": record.buyer_id.id,
                    "move_type": "out_invoice",
                    "name": "FAC/2024/" + str(record.id),
                    "line_ids": [
                        Command.create(
                            {
                                "name": "Commission",
                                "quantity": "1",
                                "price_unit": 0.06 * record.selling_price,
                            }
                        ),
                        Command.create(
                            {
                                "name": "Administrative Feeds",
                                "quantity": "1",
                                "price_unit": 100,
                            }
                        ),
                    ],
                }
            )
        return super().set_sold()

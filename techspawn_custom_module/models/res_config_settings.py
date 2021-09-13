from odoo import api, fields, models, _


class ResSettings(models.TransientModel):
    _inherit = "res.config.settings"

    product_lines = fields.Boolean("Product Lines")

    @api.model
    def get_values(self):
        res = super(ResSettings, self).get_values()
        res.update(
            product_lines=self.env['ir.config_parameter'].sudo().get_param(
                'techspawn_custom_module.product_lines',default=False),
        )
        return res

    def set_values(self):
        super(ResSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        field1 = True if self.product_lines else False
        param.set_param('techspawn_custom_module.product_lines', field1)



from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
import base64
import logging
from io import BytesIO

_logger = logging.getLogger(__name__)
try:
    import xlsxwriter
except ImportError:
    _logger.debug("Can not import xlsxwriter`.")


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def print_sale_order_excel_report(self):
        return self.env.ref('techspawn_custom_module.report_custom_sale_order_excel_report').report_action(self)

    def action_quotation_send_excel(self):
        excel_obj = self.env['report.techspawn_custom_module.report_saleproforma_excel'].with_context(
            active_model='sale.order').create_xlsx_report(docids=self.ids, data={})
        data_record = base64.b64encode(excel_obj[0])
        ir_values = {
            'name': "sale_order.xlsx",
            'type': 'binary',
            'datas': data_record,
            'store_fname': data_record,
            'mimetype': 'application/x-xlsx',
        }
        data_id = self.env['ir.attachment'].create(ir_values)
        template_id = self._find_mail_template()
        template = self.env['mail.template'].browse(template_id)
        template.attachment_ids = [(6, 0, [data_id.id])]
        email_values = {'email_to': self.partner_id.email,
                        'email_from': self.env.user.email}
        template.send_mail(self.id, email_values=email_values, force_send=True)
        template.attachment_ids = [(3, data_id.id)]
        return True


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_lines = fields.Boolean(default=lambda self: self.env['ir.config_parameter'].sudo().get_param(
        'techspawn_custom_module.product_lines') or False)
    test_field_widget = fields.Float("widget Test")

    def _compute_values(self):
        # import wdb
        # wdb.set_trace()
        for rec in self:
            rec.product_lines = self.env['ir.config_parameter'].sudo().get_param(
                'techspawn_custom_module.product_lines') or False

    # product_id = fields.Many2one(
    #     'product.template' if product_lines else 'product.product', string='Product',
    #     domain="[('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    #     change_default=True, ondelete='restrict', check_company=True)  # Unrequired company

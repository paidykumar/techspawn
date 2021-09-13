from odoo import api, fields, models
from odoo.exceptions import ValidationError


class saleOrderExcel(models.AbstractModel):
    _name = 'report.techspawn_custom_module.report_saleproforma_excel'
    _inherit = "report.report_xlsx.abstract"

    def _get_report_values(self, docids, data=None):
        docs = self.env['sale.order'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'sale.order',
            'docs': docs,
            'proforma': True
        }

    def generate_xlsx_report(self, workbook, data, response):
        # import wdb
        # wdb.set_trace()
        for doc in response:
            currency_symbol = self.env.user.company_id.currency_id.symbol
            sheet = workbook.add_worksheet("Sale Order Report")
            sheet.set_column(0, 10, 25)
            cell_format = workbook.add_format({'font_size': '12px'})
            bold = workbook.add_format({'bold': True,
                                        'font_size': 10,
                                        })

            txt = workbook.add_format({'font_size': 10, 'bg_color': '#D3D3D3', 'border': 1, 'bold': True})

            txt_left = workbook.add_format({'align': 'left',
                                            'font_size': 10,
                                            })
            if doc.partner_shipping_id == doc.partner_invoice_id and doc.partner_invoice_id != doc.partner_id or doc.partner_shipping_id != doc.partner_invoice_id:
                if doc.partner_shipping_id == doc.partner_invoice_id:
                    sheet.write('A5', 'Invoicing and Shipping Address:', bold)
                    sheet.write('A6', doc.partner_id.name, txt_left)
                    sheet.write('A7', doc.partner_id.street, txt_left)
                    sheet.write('A8', str(doc.partner_id.city) + ' ' + str(doc.partner_id.state_id.name), txt_left)
                    sheet.write('A9', doc.partner_id.country_id.name, txt_left)
                    sheet.write('A10', doc.partner_id.phone, txt_left)

                if doc.partner_shipping_id != doc.partner_invoice_id:
                    sheet.write('A5', 'Invoicing Address:', bold)
                    sheet.write('A6', doc.partner_id.name, txt_left)
                    sheet.write('A7', doc.partner_id.street, txt_left)
                    sheet.write('A8', str(doc.partner_id.city) + ' ' + str(doc.partner_id.state_id.name), txt_left)
                    sheet.write('A9', doc.partner_id.country_id.name, txt_left)
                    sheet.write('A10', doc.partner_id.phone, txt_left)
            if doc.state not in ['draft', 'sent']:
                sheet.write('A12', 'Order #', bold)
                sheet.write('B12', doc.name, txt_left)

            if doc.state in ['draft', 'sent']:
                sheet.write('A12', 'Quotation #', bold)
                sheet.write('B12', doc.name, txt_left)

            if doc.client_order_ref:
                sheet.write('A13', 'Your Reference:', bold)
                sheet.write('A14', doc.client_order_ref, txt_left)
            if doc.date_order and doc.state not in ['draft', 'sent']:
                sheet.write('A15', 'Order Date:', bold)
                sheet.write('A16', doc.date_order, txt_left)
            if doc.date_order and doc.state in ['draft', 'sent']:
                sheet.write('A15', 'Quotation Date:', bold)
                sheet.write('A16', doc.date_order, txt_left)
            if doc.validity_date and doc.state in ['draft', 'sent']:
                sheet.write('A17', 'Expiration Date:', bold)
                sheet.write('A18', doc.validity_date, txt_left)
            if doc.user_id.name:
                sheet.write('A19', 'Salesperson:', bold)
                sheet.write('A20', doc.user_id.name, txt_left)

            display_discount = any([l.discount for l in doc.order_line])
            sheet.write('A22', 'Description', txt)
            sheet.write('B22', 'Quantity', txt)
            sheet.write('C22', 'Unit Price', txt)
            sheet.write('D22', 'Disc.%', txt)
            sheet.write('E22', 'Taxes', txt)
            sheet.write('F22', 'Amount', txt)

            current_subtotal = 0
            index = 0
            row_num = 23
            col_num = 0
            current_section = False
            for line in doc.order_line:
                current_subtotal = current_subtotal + line.price_total
                if not line.display_type:
                    sheet.write(row_num, col_num, line.name, txt_left)
                    sheet.write(row_num, col_num + 1, line.product_uom_qty, txt_left)
                    sheet.write(row_num, col_num + 2, line.price_unit, txt_left)
                    sheet.write(row_num, col_num + 3, line.discount, txt_left)
                    sheet.write(row_num, col_num + 4, ', '.join(map(lambda x: (x.description or x.name), line.tax_id)),
                                txt_left)
                    sheet.write(row_num, col_num + 5, line.price_total, txt_left)
                    row_num = row_num + 1
                if line.display_type == 'line_section':
                    sheet.write(row_num, col_num, line.name, txt_left)
                    current_section = line
                    current_subtotal = 0
                    row_num = row_num + 1
                if line.display_type == 'line_note':
                    sheet.write(row_num, col_num, line.name, txt_left)
                    row_num = row_num + 1
                if current_section and (doc.order_line[index + 1].display_type == 'line_section'):
                    sheet.write(row_num+1, col_num, 'Subtotal', txt_left)
                    row_num = row_num + 1

            sheet.write(row_num + 2, col_num, 'Subtotal', bold)
            sheet.write(row_num + 2, col_num+1, doc.amount_untaxed, txt_left)
            row_num = row_num + 1
            for amount_by_group in doc.amount_by_group:
                if amount_by_group[5] == 1 and doc.amount_untaxed == amount_by_group[2]:
                    sheet.write(row_num, col_num, str(amount_by_group[0]) + str(amount_by_group[2]), txt_left)
                    sheet.write(row_num, col_num+1, amount_by_group[1], txt_left)
                else:
                    sheet.write(row_num, col_num, str(amount_by_group[0]) + str(amount_by_group[2]), txt_left)
                    sheet.write(row_num, col_num + 1, amount_by_group[1], txt_left)
                row_num = row_num + 1
        return workbook




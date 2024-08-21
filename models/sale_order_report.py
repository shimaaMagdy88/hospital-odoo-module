from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SaleOrder(models.AbstractModel):
    _name = 'report.om_hospital.report_orders_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        sale_order_durations = self.env['sale.order.duration'].search([])
        ids = []
        for record in sale_order_durations:
            ids.append(record.id)

        last_id = max(ids)
        last_id_start_date = self.env['sale.order.duration'].browse(last_id).start_date
        last_id_end_date = self.env['sale.order.duration'].browse(last_id).end_date
        new_records = self.env['sale.order'].search([('create_date', '>=', last_id_start_date), ('create_date', '<=', last_id_end_date)])

        if not new_records:
            raise ValidationError(_('There are not sales orders in this period'))

        products = []
        products_with_counts = {}

        for record in new_records:
            for line in record.order_line:
                products.append(line.product_id)

        for product in products:
            if product not in products_with_counts.keys():
                products_with_counts[product] = products.count(product)

            # if product.name not in products_with_counts.keys():           # product.name not product => to check for names not ids (because i want unique names not unique ids)
                # products_with_counts[product.name] = products.count(product)    # add product.name also not product (id)

        products_with_counts_sorted = sorted(products_with_counts.items(), key=lambda x: x[1], reverse=True)

        return {
            'docs_ids': docids,
            'doc_model': 'sale.order',
            'docs': new_records,
            'data': data,
            'products': products_with_counts_sorted,
        }

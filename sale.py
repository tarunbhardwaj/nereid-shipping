# -*- coding: utf-8 -*-
"""
    sale

    :copyright: (c) 2015 by Fulfil.IO Inc.
    :license: see LICENSE for details.
"""
from trytond.pool import PoolMeta, Pool
from trytond.transaction import Transaction

__metaclass__ = PoolMeta


class Sale:
    __name__ = 'sale.sale'

    def apply_shipping(self):
        """
        Apply shipping for sale
        """
        Currency = Pool().get('currency.currency')

        if not self.carrier:
            return

        if self.carrier.carrier_cost_method == 'product':
            with Transaction().set_context(self._get_carrier_context()):
                shipment_cost, currency_id = self.carrier.get_sale_price()

            shipment_cost = Currency.compute(
                Currency(currency_id), shipment_cost, self.currency
            )
            self.add_shipping_line(
                shipment_cost,
                self.carrier.rec_name
            )
        else:
            getattr(
                self, 'apply_%s_shipping' % self.carrier.carrier_cost_method
            )()

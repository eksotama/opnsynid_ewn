# -*- encoding: utf-8 -*-
##############################################################################
#    Author : Andhitia Rama, Michael Viriyananda, Nurazmi
#    Copyright (C) 2015 OpenSynergy Indonesia
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import fields, models
from openerp import tools


class PosOrderQuery(models.Model):
    """Point of Sale send flag"""
    _name = 'pos.order_query'
    _description = 'POS Order Query'
    _auto = False
    
    name = fields.Char(
        string='# Order')
    id_resto = fields.Char(
        string='id_resto',
        )
    name_resto = fields.Char(
        string='name_resto',
        )
    id_bill = fields.Char(
        string='id_bill',
        )
    date_order = fields.Datetime(
        string='Date Order',
        )
    tgl_bill = fields.Char(
        string='tgl_bill',
        )
    jam_bill = fields.Char(
        string='jam_bill',
        )
    customer_id = fields.Many2one(
        string='Customer',
        comodel_name = 'res.partner',
        )
    customer = fields.Char(
        string='Customer',
        )
    total_bill = fields.Float(
        string='total_bill',
        )
    send_flag = fields.Boolean(
        string='send_flag',
        )
    
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'pos_order_query')
        cr.execute("""
            create or replace view pos_order_query as (
            SELECT  a.name AS name,
                    d.ref AS id_resto,
                    b.name AS name_resto,
                    a.name AS id_bill,
                    a.id AS id,
                    a.date_order AS date_order,
                    TO_CHAR(a.date_order, 'DD-MM-YYYY') AS tgl_bill,
                    TO_CHAR(a.date_order, 'HH24:MI:SS') AS jam_bill,
                    a.partner_id AS customer_id,
                    e.name AS customer,
                    c.amount_total AS total_bill,
                    a.send_flag AS send_flag
            FROM    pos_order AS a
            JOIN    res_company AS b ON a.company_id = b.id
            JOIN    (
                    SELECT  c1.order_id AS order_id,
                            SUM(c1.price_subtotal_incl) AS amount_total
                    FROM    pos_order_line AS c1
                    GROUP BY    order_id
                    ) AS c ON   a.id = c.order_id
            JOIN    res_partner AS d ON b.partner_id = d.id
            LEFT JOIN    res_partner AS e ON a.partner_id = e.id
            )
        """)

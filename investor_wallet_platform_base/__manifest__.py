# Copyright 2013-2018 Open Architects Consulting SPRL.
# Copyright 2018-Coop IT Easy SCRLfs (<http://www.coopiteasy.be>)
# - Houssine BAKKALI - <houssine@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).#


{
    "name": "Investor Wallet Platform Base",
    "version": "12.0.1.2.1",
    "depends": [
        "easy_my_coop",
        "easy_my_coop_loan",
    ],
    "author": "Houssine BAKKALI <houssine@coopiteasy.be>",
    "category": "Cooperative management",
    "website": "www.coopiteasy.be",
    "license": "AGPL-3",
    "description": """
    This module add a layer on top of easy my coop to allow handling several
    structures to rise capital through the easy my coop flow.
    """,
    'data': [
        'security/wallet_platform_security.xml',
        'security/ir.model.access.csv',
        'data/wallet_platform_data.xml',
        'data/sector_area_data.xml',
        'views/res_partner_view.xml',
        'views/subscription_request_view.xml',
        'views/invoice_view.xml',
        'views/res_users_view.xml',
        'views/product_view.xml',
        'views/activity_area_view.xml',
        'views/loan_issue_view.xml',
        'views/menus.xml',
        'views/res_company_view.xml',
        ],
    'demo': [
        'demo/structure.xml',
        'demo/coop.xml',
    ],
    'installable': True,
    'application': True,
}

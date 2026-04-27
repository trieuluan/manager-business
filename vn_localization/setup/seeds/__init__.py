"""Seed runners for vn_localization."""

import frappe

from vn_localization.setup.services.chart_of_accounts import sync_vn_chart_of_accounts
from vn_localization.setup.services.company_defaults import sync_vn_company_defaults
from vn_localization.setup.services.currency import sync_vnd_currency
from vn_localization.setup.services.language import sync_vietnamese_language
from vn_localization.setup.services.mode_of_payment import sync_vn_modes_of_payment
from vn_localization.setup.services.party_groups import sync_vn_party_groups
from vn_localization.setup.services.payment_terms import sync_vn_payment_terms
from vn_localization.setup.services.price_list import sync_vn_price_lists
from vn_localization.setup.services.print_formats import sync_vn_print_defaults
from vn_localization.setup.services.regional import sync_vn_regional_settings
from vn_localization.setup.services.tax_templates import sync_vn_tax_templates
from vn_localization.setup.services.territory import sync_vn_territories
from vn_localization.setup.services.uom import sync_vn_uoms
from vn_localization.setup.services.warehouse import sync_vn_warehouses


def apply_base_localization():
    logger = frappe.logger("vn_localization")
    logger.info("Applying vn_localization base setup")

    sync_vietnamese_language()
    sync_vn_regional_settings()
    sync_vnd_currency()
    sync_vn_uoms()
    sync_vn_payment_terms()
    sync_vn_price_lists()
    sync_vn_party_groups()
    sync_vn_territories()
    sync_vn_modes_of_payment()
    sync_vn_print_defaults()
    sync_vn_chart_of_accounts()
    sync_vn_tax_templates()
    sync_vn_warehouses()
    sync_vn_company_defaults()

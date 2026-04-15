"""Seed runners for vn_localization."""

import frappe

from vn_localization.setup.services.chart_of_accounts import sync_vn_chart_of_accounts
from vn_localization.setup.services.language import sync_vietnamese_language
from vn_localization.setup.services.print_formats import sync_vn_print_defaults
from vn_localization.setup.services.regional import sync_vn_regional_settings
from vn_localization.setup.services.workspaces import sync_vn_workspaces


def apply_base_localization():
    logger = frappe.logger("vn_localization")
    logger.info("Applying vn_localization base setup")

    sync_vietnamese_language()
    sync_vn_regional_settings()
    sync_vn_workspaces()
    sync_vn_print_defaults()
    sync_vn_chart_of_accounts()

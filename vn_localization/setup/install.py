"""Install orchestration for vn_localization."""

from vn_localization.setup.seeds import apply_base_localization


def after_install():
    apply_base_localization()

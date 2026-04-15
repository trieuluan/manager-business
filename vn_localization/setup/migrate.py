"""Migration orchestration for vn_localization."""

from vn_localization.setup.seeds import apply_base_localization


def after_migrate():
    apply_base_localization()

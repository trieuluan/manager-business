### Vn Localization

Vietnamese localization for ERPNext

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch version-16
bench install-app vn_localization
```

### App Structure

This app is organized as a localization package for Vietnamese ERPNext deployments:

- `vn_localization/locale/vi.po`: broad UI translations for Frappe / ERPNext
- `vn_localization/translations/vi.csv`: high-priority labels and workspace/menu translations
- `vn_localization/fixtures/`: exported customizations that must stay under version control
- `vn_localization/vn_localization/workspace/*/*.json`: workspace source of truth managed the Frappe way
- `vn_localization/setup/`: install / migrate orchestration, idempotent seeds and regional defaults

### Localization Lifecycle

- `after_install` enables Vietnamese, seeds print formats and SME account heads
- `after_migrate` re-syncs the same defaults so production does not rely on manual changes
- fixtures are whitelisted in `hooks.py` so future customizations can be exported back into the app

### Workspace Source of Truth

- Workspace layout, shortcuts, links and content should be maintained in `workspace/*.json`
- Do not rebuild workspace structure from Python on migrate, otherwise Frappe-generated workspace files become useless
- Python hooks may bootstrap localization defaults, but workspace UI should follow the checked-in JSON files

### Production Notes

- Prefer exporting customizations into the app instead of editing production by hand
- Prefer running seeds through install / migrate hooks instead of one-off scripts
- Build images in local / CI, then deploy by pulling the image and running migrate on the server

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/vn_localization
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit

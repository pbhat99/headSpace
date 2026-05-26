try:
    from PySide6.QtWidgets import (
        QCheckBox,
        QComboBox,
        QDialog,
        QDialogButtonBox,
        QFormLayout,
        QGroupBox,
        QMessageBox,
        QVBoxLayout,
    )
except ImportError:
    from PySide2.QtWidgets import (
        QCheckBox,
        QComboBox,
        QDialog,
        QDialogButtonBox,
        QFormLayout,
        QGroupBox,
        QMessageBox,
        QVBoxLayout,
    )

import tabtabtab_nuke
import tabtabtab_nuke_core
import tabtabtab_prefs


class TabtabtabPrefsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tabtabtab Preferences")
        self._build_ui()
        self._populate_from_prefs()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()
        main_layout.addLayout(form_layout)

        self.tabtabtab_enabled_checkbox = QCheckBox()
        self.tabtabtab_enabled_checkbox.setToolTip(
            "When unchecked, Tabtabtab is disabled entirely and Nuke's default "
            "Tab key behavior is restored. Takes effect immediately."
        )
        form_layout.addRow("Enable Tabtabtab:", self.tabtabtab_enabled_checkbox)

        # Space-prefix mode mapping
        mode_group = QGroupBox("Space-prefix search modes")
        mode_layout = QFormLayout()
        mode_group.setLayout(mode_layout)

        mode_labels = {
            tabtabtab_nuke_core.MODE_ANCHORED_FUZZY: "Anchored fuzzy",
            tabtabtab_nuke_core.MODE_NON_ANCHORED_FUZZY: "Non-anchored fuzzy",
            tabtabtab_nuke_core.MODE_CONSECUTIVE: "Consecutive substring",
        }
        all_modes = list(tabtabtab_nuke_core.DEFAULT_SPACE_MODE_ORDER)

        self._space_combos = []
        for space_label in ["No leading space:", "One leading space:", "Two leading spaces:"]:
            combo = QComboBox()
            for mode_id in all_modes:
                combo.addItem(mode_labels[mode_id], mode_id)
            mode_layout.addRow(space_label, combo)
            self._space_combos.append(combo)

        main_layout.addWidget(mode_group)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self._on_accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

    def _populate_from_prefs(self):
        prefs = tabtabtab_prefs.prefs_singleton
        self.tabtabtab_enabled_checkbox.setChecked(bool(prefs.get("tabtabtab_enabled")))

        space_mode_order = prefs.get("space_mode_order")
        for i, combo in enumerate(self._space_combos):
            idx = combo.findData(space_mode_order[i])
            if idx >= 0:
                combo.setCurrentIndex(idx)

    def _on_accept(self):
        prefs = tabtabtab_prefs.prefs_singleton

        space_mode_order = [combo.currentData() for combo in self._space_combos]
        if len(set(space_mode_order)) < 3:
            QMessageBox.warning(
                self,
                "Invalid configuration",
                "Each search mode must be assigned to exactly one space level.",
            )
            return

        enabled = self.tabtabtab_enabled_checkbox.isChecked()
        prefs.set("tabtabtab_enabled", enabled)
        prefs.set("space_mode_order", space_mode_order)
        prefs.save()
        if enabled:
            tabtabtab_nuke.registerNukeAction()
        else:
            tabtabtab_nuke.unregisterNukeAction()
        self.accept()


def show_prefs_dialog():
    dialog = TabtabtabPrefsDialog()
    dialog.exec()

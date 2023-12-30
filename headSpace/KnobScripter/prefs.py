# -*- coding: utf-8 -*-
""" KnobScripter Prefs: Preferences widget (PrefsWidget) and utility function to load all preferences.

The load_prefs function will load all preferences relative to the KnobScripter, both stored
as variables in the config.py module and saved in the KS preferences json file.

adrianpueyo.com

"""

import json
import os
import nuke

from KnobScripter.info import __version__, __author__, __date__
from KnobScripter import config, widgets, utils

try:
    if nuke.NUKE_VERSION_MAJOR < 11:
        from PySide import QtCore, QtGui, QtGui as QtWidgets
        from PySide.QtCore import Qt
    else:
        from PySide2 import QtWidgets, QtGui, QtCore
        from PySide2.QtCore import Qt
except ImportError:
    from Qt import QtCore, QtGui, QtWidgets


def load_prefs():
    """ Load prefs json file and overwrite config.prefs """
    # Setup paths
    config.ks_directory = os.path.join(os.path.expanduser("~"), ".nuke", config.prefs["ks_directory"])
    config.py_scripts_dir = os.path.join(config.ks_directory, config.prefs["ks_py_scripts_directory"])
    config.blink_dir = os.path.join(config.ks_directory, config.prefs["ks_blink_directory"])
    config.codegallery_user_txt_path = os.path.join(config.ks_directory, config.prefs["ks_codegallery_file"])
    config.snippets_txt_path = os.path.join(config.ks_directory, config.prefs["ks_snippets_file"])
    config.prefs_txt_path = os.path.join(config.ks_directory, config.prefs["ks_prefs_file"])
    config.py_state_txt_path = os.path.join(config.ks_directory, config.prefs["ks_py_state_file"])
    config.knob_state_txt_path = os.path.join(config.ks_directory, config.prefs["ks_knob_state_file"])

    # Setup config font
    config.script_editor_font = QtGui.QFont()
    config.script_editor_font.setStyleHint(QtGui.QFont.Monospace)
    config.script_editor_font.setFixedPitch(True)
    config.script_editor_font.setFamily("Monospace")
    config.script_editor_font.setPointSize(10)

    if not os.path.isfile(config.prefs_txt_path):
        return None
    else:
        with open(config.prefs_txt_path, "r") as f:
            prefs = json.load(f)
            for pref in prefs:
                config.prefs[pref] = prefs[pref]
            config.script_editor_font.setFamily(config.prefs["se_font_family"])
            config.script_editor_font.setPointSize(config.prefs["se_font_size"])
            return prefs

def clear_knob_state_history():
    if not nuke.ask("Are you sure you want to clear all history of knob states?"):
        return

    # Per instance? Probably not
    # for ks in config.all_knobscripters:
    #     if hasattr(ks, 'current_node_state_dict'):
    #         ks.current_node_state_dict = {}

    # In memory
    config.knob_state_dict = {}
    # In file
    with open(config.knob_state_txt_path, "w") as f:
        json.dump({}, f)

def clear_py_state_history():
    if not nuke.ask("Are you sure you want to clear all history of .py states?"):
        return
    # In memory
    config.py_state_dict = {}
    with open(config.py_state_txt_path, "w") as f:
        json.dump({}, f)

class PrefsWidget(QtWidgets.QWidget):
    def __init__(self, knob_scripter="", _parent=QtWidgets.QApplication.activeWindow()):
        super(PrefsWidget, self).__init__(_parent)
        self.knob_scripter = knob_scripter
        self.initUI()
        self.refresh_prefs()

    def initUI(self):
        self.layout = QtWidgets.QVBoxLayout()

        # 1. Title (name, version)
        self.title_widget = QtWidgets.QWidget()
        self.title_layout = QtWidgets.QHBoxLayout()
        self.title_layout.setMargin(0)
        title_label = QtWidgets.QLabel("KnobScripter v" + __version__)
        title_label.setStyleSheet("font-weight:bold;color:#CCCCCC;font-size:20px;")
        built_label = QtWidgets.QLabel('<i style="color:#777">Built {0}</i>'.format(__date__))
        built_label.setStyleSheet("color:#555;font-size:9px;padding-top:10px;")
        subtitle_label = QtWidgets.QLabel("Script editor for python and callback knobs")
        subtitle_label.setStyleSheet("color:#999")
        line1 = widgets.HLine()

        img_ap = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(os.path.join(config.ICONS_DIR, "ap_tools.png"))
        img_ap.setPixmap(pixmap)
        img_ap.resize(pixmap.width(), pixmap.height())
        img_ap.setStyleSheet("padding-top: 3px;")


        signature = QtWidgets.QLabel('<a href="http://www.adrianpueyo.com/" style="color:#888;text-decoration:none">'
                                     '<b>adrianpueyo.com</b></a>, 2016-{0}'.format(__date__.split(" ")[-1]))

        signature.setOpenExternalLinks(True)
        # signature.setStyleSheet('''color:#555;font-size:9px;padding-left: {}px;'''.format(pixmap.width()+4))
        signature.setStyleSheet('''color:#555;font-size:9px;''')
        signature.setAlignment(QtCore.Qt.AlignLeft)

        img_ks = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(os.path.join(config.ICONS_DIR, "knob_scripter.png"))
        img_ks.setPixmap(pixmap)
        img_ks.resize(pixmap.width(), pixmap.height())

        # self.title_layout.addWidget(img_ks)
        self.title_layout.addWidget(img_ap)
        self.title_layout.addSpacing(2)
        self.title_layout.addWidget(title_label)
        self.title_layout.addWidget(built_label)
        self.title_layout.addStretch()
        self.title_widget.setLayout(self.title_layout)

        self.layout.addWidget(self.title_widget)
        self.layout.addWidget(signature)
        self.layout.addWidget(line1)

        # 2. Scroll Area
        # 2.1. Inner scroll content
        self.scroll_content = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_layout.setMargin(0)

        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_content.setContentsMargins(0, 0, 8, 0)

        # 2.2. External Scroll Area
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.scroll_content)
        self.scroll.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)

        self.layout.addWidget(self.scroll)

        # 3. Build prefs inside scroll layout
        self.form_layout = QtWidgets.QFormLayout()
        self.scroll_layout.addLayout(self.form_layout)
        self.scroll_layout.addStretch()

        # 3.1. General
        self.form_layout.addRow("<b>General</b>", QtWidgets.QWidget())
        # Font
        self.font_box = QtWidgets.QFontComboBox()
        self.font_box.currentFontChanged.connect(self.font_changed)
        self.form_layout.addRow("Font:", self.font_box)

        # Font size
        self.font_size_box = QtWidgets.QSpinBox()
        self.font_size_box.setMinimum(6)
        self.font_size_box.setMaximum(100)
        self.font_size_box.setFixedHeight(24)
        self.font_size_box.valueChanged.connect(self.font_size_changed)
        self.form_layout.addRow("Font size:", self.font_size_box)

        # Window size
        self.window_size_box = QtWidgets.QFrame()
        self.window_size_box.setContentsMargins(0, 0, 0, 0)
        window_size_layout = QtWidgets.QHBoxLayout()
        window_size_layout.setMargin(0)
        self.window_size_w_box = QtWidgets.QSpinBox()
        self.window_size_w_box.setValue(config.prefs["ks_default_size"][0])
        self.window_size_w_box.setMinimum(200)
        self.window_size_w_box.setMaximum(4000)
        self.window_size_w_box.setFixedHeight(24)
        self.window_size_w_box.setToolTip("Default window width in pixels")
        window_size_layout.addWidget(self.window_size_w_box)
        window_size_layout.addWidget(QtWidgets.QLabel("x"))
        self.window_size_h_box = QtWidgets.QSpinBox()
        self.window_size_h_box.setValue(config.prefs["ks_default_size"][1])
        self.window_size_h_box.setMinimum(100)
        self.window_size_h_box.setMaximum(2000)
        self.window_size_h_box.setFixedHeight(24)
        self.window_size_h_box.setToolTip("Default window height in pixels")
        window_size_layout.addWidget(self.window_size_h_box)
        self.window_size_box.setLayout(window_size_layout)
        self.form_layout.addRow("Floating window:", self.window_size_box)

        self.grab_dimensions_button = QtWidgets.QPushButton("Grab current dimensions")
        self.grab_dimensions_button.clicked.connect(self.grab_dimensions)
        self.form_layout.addRow("", self.grab_dimensions_button)

        # Save knob editor state
        self.knob_editor_state_box = QtWidgets.QFrame()
        self.knob_editor_state_box.setContentsMargins(0, 0, 0, 0)
        knob_editor_state_layout = QtWidgets.QHBoxLayout()
        knob_editor_state_layout.setMargin(0)
        self.save_knob_editor_state_combobox = QtWidgets.QComboBox()
        self.save_knob_editor_state_combobox.setToolTip("Save script editor state on knobs? "
                                                        "(which knob is open in editor, cursor pos, scroll values)\n"
                                                        "  - Save in memory = active session only\n"
                                                        "  - Save to disk = active between sessions")
        self.save_knob_editor_state_combobox.addItem("Do not save", 0)
        self.save_knob_editor_state_combobox.addItem("Save in memory", 1)
        self.save_knob_editor_state_combobox.addItem("Save to disk", 2)
        knob_editor_state_layout.addWidget(self.save_knob_editor_state_combobox)
        self.clear_knob_history_button = QtWidgets.QPushButton("Clear history")
        self.clear_knob_history_button.clicked.connect(clear_knob_state_history)
        knob_editor_state_layout.addWidget(self.clear_knob_history_button)
        self.knob_editor_state_box.setLayout(knob_editor_state_layout)
        self.form_layout.addRow("Knob Editor State:", self.knob_editor_state_box)

        # Save .py editor state
        self.py_editor_state_box = QtWidgets.QFrame()
        self.py_editor_state_box.setContentsMargins(0, 0, 0, 0)
        py_editor_state_layout = QtWidgets.QHBoxLayout()
        py_editor_state_layout.setMargin(0)
        self.save_py_editor_state_combobox = QtWidgets.QComboBox()
        self.save_py_editor_state_combobox.setToolTip("Save script editor state on .py scripts? "
                                                        "(which script is open in editor, cursor pos, scroll values)\n"
                                                        "  - Save in memory = active session only\n"
                                                        "  - Save to disk = active between sessions")
        self.save_py_editor_state_combobox.addItem("Do not save", 0)
        self.save_py_editor_state_combobox.addItem("Save in memory", 1)
        self.save_py_editor_state_combobox.addItem("Save to disk", 2)
        py_editor_state_layout.addWidget(self.save_py_editor_state_combobox)
        self.clear_py_history_button = QtWidgets.QPushButton("Clear history")
        self.clear_py_history_button.clicked.connect(clear_py_state_history)
        py_editor_state_layout.addWidget(self.clear_py_history_button)
        self.py_editor_state_box.setLayout(py_editor_state_layout)
        self.form_layout.addRow(".py Editor State:", self.py_editor_state_box)


        # 3.2. Python
        self.form_layout.addRow(" ", None)
        self.form_layout.addRow("<b>Python</b>", QtWidgets.QWidget())

        # Tab spaces
        self.tab_spaces_combobox = QtWidgets.QComboBox()
        self.tab_spaces_combobox.addItem("2", 2)
        self.tab_spaces_combobox.addItem("4", 4)
        self.tab_spaces_combobox.currentIndexChanged.connect(self.tab_spaces_changed)
        self.form_layout.addRow("Tab spaces:", self.tab_spaces_combobox)

        # Color scheme
        self.python_color_scheme_combobox = QtWidgets.QComboBox()
        self.python_color_scheme_combobox.addItem("nuke", "nuke")
        self.python_color_scheme_combobox.addItem("monokai", "monokai")
        self.python_color_scheme_combobox.currentIndexChanged.connect(self.color_scheme_changed)
        self.form_layout.addRow("Color scheme:", self.python_color_scheme_combobox)

        # Run in context
        self.run_in_context_checkbox = QtWidgets.QCheckBox("Run in context")
        self.run_in_context_checkbox.setToolTip("Default mode for running code in context (when in node mode).")
        # self.run_in_context_checkbox.stateChanged.connect(self.run_in_context_changed)
        self.form_layout.addRow("", self.run_in_context_checkbox)

        # Show labels
        self.show_knob_labels_checkbox = QtWidgets.QCheckBox("Show knob labels")
        self.show_knob_labels_checkbox.setToolTip("Display knob labels on the knob dropdown\n"
                                                  "Otherwise, show the internal name only.")
        self.form_layout.addRow("", self.show_knob_labels_checkbox)

        # 3.3. Blink
        self.form_layout.addRow(" ", None)
        self.form_layout.addRow("<b>Blink</b>", QtWidgets.QWidget())

        # Color scheme
        # self.blink_color_scheme_combobox = QtWidgets.QComboBox()
        # self.blink_color_scheme_combobox.addItem("nuke default")
        # self.blink_color_scheme_combobox.addItem("adrians flavour")
        # self.form_layout.addRow("Tab spaces:", self.blink_color_scheme_combobox)
        self.autosave_on_compile_checkbox = QtWidgets.QCheckBox("Auto-save to disk on compile")
        self.autosave_on_compile_checkbox.setToolTip("Set the default value for <b>Auto-save to disk on compile</b>.")
        self.form_layout.addRow("", self.autosave_on_compile_checkbox)

        # 4. Lower buttons?
        self.lower_buttons_layout = QtWidgets.QHBoxLayout()
        self.lower_buttons_layout.addStretch()

        self.save_prefs_button = QtWidgets.QPushButton("Save")
        self.save_prefs_button.clicked.connect(self.save_prefs)
        self.lower_buttons_layout.addWidget(self.save_prefs_button)
        self.apply_prefs_button = QtWidgets.QPushButton("Apply")
        self.apply_prefs_button.clicked.connect(self.apply_prefs)
        self.lower_buttons_layout.addWidget(self.apply_prefs_button)
        self.cancel_prefs_button = QtWidgets.QPushButton("Cancel")
        self.cancel_prefs_button.clicked.connect(self.cancel_prefs)
        self.lower_buttons_layout.addWidget(self.cancel_prefs_button)

        self.layout.addLayout(self.lower_buttons_layout)
        self.setLayout(self.layout)

    def font_size_changed(self):
        config.script_editor_font.setPointSize(self.font_size_box.value())
        for ks in config.all_knobscripters:
            if hasattr(ks, 'script_editor'):
                ks.script_editor.setFont(config.script_editor_font)

    def font_changed(self):
        self.font = self.font_box.currentFont().family()
        config.script_editor_font.setFamily(self.font)
        for ks in config.all_knobscripters:
            if hasattr(ks, 'script_editor'):
                ks.script_editor.setFont(config.script_editor_font)

    def tab_spaces_changed(self):
        config.prefs["se_tab_spaces"] = self.tab_spaces_combobox.currentData()
        for ks in config.all_knobscripters:
            if hasattr(ks, 'highlighter'):
                ks.highlighter.rehighlight()
        return

    def color_scheme_changed(self):
        config.prefs["code_style_python"] = self.python_color_scheme_combobox.currentData()
        for ks in config.all_knobscripters:
            if hasattr(ks, 'script_editor'):
                if ks.script_editor.code_language == "python":
                    ks.script_editor.highlighter.setStyle(config.prefs["code_style_python"])
                ks.script_editor.highlighter.rehighlight()
        return

    def grab_dimensions(self):
        self.knob_scripter = utils.getKnobScripter(self.knob_scripter)
        self.window_size_w_box.setValue(self.knob_scripter.width())
        self.window_size_h_box.setValue(self.knob_scripter.height())

    def refresh_prefs(self):
        """ Reload the json prefs, apply them on config.prefs, and repopulate the knobs """
        load_prefs()

        self.font_box.setCurrentFont(QtGui.QFont(config.prefs["se_font_family"]))
        self.font_size_box.setValue(config.prefs["se_font_size"])

        self.window_size_w_box.setValue(config.prefs["ks_default_size"][0])
        self.window_size_h_box.setValue(config.prefs["ks_default_size"][1])

        self.show_knob_labels_checkbox.setChecked(config.prefs["ks_show_knob_labels"] is True)
        self.run_in_context_checkbox.setChecked(config.prefs["ks_run_in_context"] is True)

        self.save_knob_editor_state_combobox.setCurrentIndex(config.prefs["ks_save_knob_state"])
        self.save_py_editor_state_combobox.setCurrentIndex(config.prefs["ks_save_py_state"])

        i = self.python_color_scheme_combobox.findData(config.prefs["code_style_python"])
        if i != -1:
            self.python_color_scheme_combobox.setCurrentIndex(i)

        i = self.tab_spaces_combobox.findData(config.prefs["se_tab_spaces"])
        if i != -1:
            self.tab_spaces_combobox.setCurrentIndex(i)

        self.autosave_on_compile_checkbox.setChecked(config.prefs["ks_blink_autosave_on_compile"])

    def get_prefs_dict(self):
        """ Return a dictionary with the prefs from the current knob state """
        ks_prefs = {
            "ks_default_size": [self.window_size_w_box.value(), self.window_size_h_box.value()],
            "ks_run_in_context": self.run_in_context_checkbox.isChecked(),
            "ks_show_knob_labels": self.show_knob_labels_checkbox.isChecked(),
            "ks_blink_autosave_on_compile": self.autosave_on_compile_checkbox.isChecked(),
            "ks_save_knob_state": self.save_knob_editor_state_combobox.currentData(),
            "ks_save_py_state": self.save_py_editor_state_combobox.currentData(),
            "code_style_python": self.python_color_scheme_combobox.currentData(),
            "se_font_family": self.font_box.currentFont().family(),
            "se_font_size": self.font_size_box.value(),
            "se_tab_spaces": self.tab_spaces_combobox.currentData(),
        }
        return ks_prefs

    def save_config(self, prefs=None):
        """ Save the given prefs dict in config.prefs """
        if not prefs:
            prefs = self.get_prefs_dict()
        for pref in prefs:
            config.prefs[pref] = prefs[pref]
        config.script_editor_font.setFamily(config.prefs["se_font_family"])
        config.script_editor_font.setPointSize(config.prefs["se_font_size"])

    def save_prefs(self):
        """ Save current prefs on json, config, and apply on KnobScripters """
        # 1. Save json
        ks_prefs = self.get_prefs_dict()
        with open(config.prefs_txt_path, "w") as f:
            json.dump(ks_prefs, f, sort_keys=True, indent=4)
            nuke.message("Preferences saved!")

        # 2. Save config
        self.save_config(ks_prefs)

        # 3. Apply on KnobScripters
        self.apply_prefs()

    def apply_prefs(self):
        """ Apply the current knob values to the KnobScripters """
        self.save_config()
        for ks in config.all_knobscripters:
            ks.script_editor.setFont(config.script_editor_font)
            ks.script_editor.tab_spaces = config.prefs["se_tab_spaces"]
            ks.script_editor.highlighter.rehighlight()
            ks.runInContext = config.prefs["ks_run_in_context"]
            ks.runInContextAct.setChecked(config.prefs["ks_run_in_context"])
            ks.show_labels = config.prefs["ks_show_knob_labels"]
            ks.blink_autoSave_act.setChecked(config.prefs["ks_blink_autosave_on_compile"])
            # TODO Apply the "ks_save_py_state" and "ks_save_knob_state" here too
            if ks.nodeMode:
                ks.refreshClicked()

    def cancel_prefs(self):
        """ Revert to saved json prefs """
        # 1. Reload json and populate knobs
        self.refresh_prefs()
        # 2. Apply values to KnobScripters
        self.apply_prefs()
        # 3. If this is a floating panel, close it??

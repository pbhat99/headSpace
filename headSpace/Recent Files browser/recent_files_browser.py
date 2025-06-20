# -*- coding: utf-8 -*-
import nuke
import os
import sys
try:
    from PySide2 import QtWidgets, QtCore, QtGui
except:
    from PySide6 import QtWidgets, QtCore, QtGui

import datetime

class RecentFilesBrowser(QtWidgets.QDialog):
    def __init__(self):
        super(RecentFilesBrowser, self).__init__()
        self.setWindowTitle("Recent Files Browser")  # English title
        self.setMinimumSize(1220, 780)  # Increased window height to accommodate the footer

        # Set the window to be resizable and allow maximize/minimize
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowMinMaxButtonsHint)

        # Set a modern style similar to Nuke's theme with darker colors
        self.setStyleSheet("""
            QDialog {
                background-color: #2D2D2D;  /* Darker background color */
                color: #FFFFFF;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #3A3A3A;
                color: #FFFFFF;
                border: 1px solid #4A4A4A;
                border-radius: 3px;
                padding: 8px;
                font-size: 14px;
            }
            QTableWidget {
                background-color: #3A3A3A;
                color: #FFFFFF;
                border: 1px solid #4A4A4A;
                border-radius: 3px;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #5A5A5A;
                color: #FFFFFF;
                border: 1px solid #4A4A4A;
                border-radius: 3px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #6A6A6A;
            }
            QPushButton:pressed {
                background-color: #4A4A4A;
            }
            QLabel {
                color: #FFFFFF;
                font-size: 14px;
            }
            #titleLabel {
                font-size: 40px;  /* Increased font size by 100% */
                font-weight: bold;
                color: #FFFFFF;
            }
            #versionLabel {
                font-size: 14px;
                color: #AAAAAA;
            }
            #footerLabel {
                font-size: 12px;
                color: #AAAAAA;
                text-align: center;
            }
        """)

        # Main Layout
        self.main_layout = QtWidgets.QVBoxLayout(self)  # Vertical layout
        self.main_layout.setSpacing(10)  # Spacing between elements
        self.main_layout.setContentsMargins(15, 15, 15, 15)  # Margins

        # Header Layout (Logo and Title)
        self.header_layout = QtWidgets.QHBoxLayout()
        self.header_layout.setSpacing(20)  # Spacing between logo and title

        # Logo
        self.logo_label = QtWidgets.QLabel(self)
        self.logo_pixmap = QtGui.QPixmap("path_to_your_logo.png")  # Replace with your logo path
        self.logo_label.setPixmap(self.logo_pixmap.scaled(64, 64, QtCore.Qt.KeepAspectRatio))  # Resize logo
        self.header_layout.addWidget(self.logo_label)

        # Title Label (Centered)
        self.title_layout = QtWidgets.QHBoxLayout()
        self.title_layout.addStretch()  # Add stretch to push the title to the center
        self.title_label = QtWidgets.QLabel("Recent Files Browser ", self)
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)  # Center align the title
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addStretch()  # Add stretch to push the title to the center
        self.header_layout.addLayout(self.title_layout)

        # Add header layout to main layout
        self.main_layout.addLayout(self.header_layout)

        # Version Label (Centered)
        self.version_layout = QtWidgets.QHBoxLayout()
        self.version_layout.addStretch()  # Add stretch to push the label to the center
        self.version_label = QtWidgets.QLabel("Running on Nuke {}".format(nuke.NUKE_VERSION_STRING), self)
        self.version_label.setObjectName("versionLabel")
        self.version_label.setAlignment(QtCore.Qt.AlignCenter)  # Center align the version
        self.version_layout.addWidget(self.version_label)
        self.version_layout.addStretch()  # Add stretch to push the label to the center
        self.main_layout.addLayout(self.version_layout)

        # Horizontal Layout for Search, Table, and Buttons
        self.content_layout = QtWidgets.QHBoxLayout()
        self.content_layout.setSpacing(10)

        # Left Panel (Search and Table)
        self.left_panel = QtWidgets.QVBoxLayout()
        self.left_panel.setSpacing(10)

        # Search Bar Layout
        self.search_layout = QtWidgets.QHBoxLayout()
        self.search_layout.setSpacing(10)

        # Search Bar (No "Search" label)
        self.search_bar = QtWidgets.QLineEdit(self)
        self.search_bar.setPlaceholderText("Search recent files...")  # English placeholder
        self.search_bar.textChanged.connect(self.start_search_timer)  # Improved search performance
        self.search_bar.setFixedWidth(int(self.width() * 0.7))  # Reduce search bar width by 70%
        self.search_layout.addWidget(self.search_bar)  # Add search bar only

        # Snipping Tool Button (Small button next to the search bar)
        self.snipping_tool_button = QtWidgets.QPushButton("📷")  # Small button with camera emoji
        self.snipping_tool_button.setFixedSize(30, 30)  # Small size
        self.snipping_tool_button.setToolTip("Open Snipping Tool")  # Tooltip
        self.snipping_tool_button.clicked.connect(self.open_snipping_tool)
        self.search_layout.addWidget(self.snipping_tool_button)  # Add the button next to the search bar

        # Add search layout to left panel
        self.left_panel.addLayout(self.search_layout)

        # Table Widget to display recent files
        self.table_widget = QtWidgets.QTableWidget(self)
        self.table_widget.setColumnCount(4)  # 4 columns: Full Path, Date, Time, Nuke Version
        self.table_widget.setHorizontalHeaderLabels(["Full Path", "Date", "Time", "Nuke Version"])
        self.table_widget.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)  # Select entire row
        self.table_widget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)  # Disable editing
        self.table_widget.setIconSize(QtCore.QSize(130, 130))  # Increase icon size by 30%
        self.left_panel.addWidget(self.table_widget)

        # Add left panel to content layout
        self.content_layout.addLayout(self.left_panel)

        # Right Panel (Buttons)
        self.right_panel = QtWidgets.QVBoxLayout()
        self.right_panel.setSpacing(10)

        # Open New Comp Button
        self.open_new_comp_button = QtWidgets.QPushButton("Open New Comp")
        self.open_new_comp_button.clicked.connect(self.open_new_comp)
        self.right_panel.addWidget(self.open_new_comp_button)

        # Open Selected Comp Button
        self.open_selected_comp_button = QtWidgets.QPushButton("Open Selected Comp")
        self.open_selected_comp_button.clicked.connect(self.open_selected_comp)
        self.right_panel.addWidget(self.open_selected_comp_button)

        # Delete Selected File Button
        self.delete_button = QtWidgets.QPushButton("Delete Selected File")
        self.delete_button.clicked.connect(self.delete_selected_file)
        self.right_panel.addWidget(self.delete_button)

        # Open File Folder Button
        self.open_folder_button = QtWidgets.QPushButton("Open File Folder")
        self.open_folder_button.clicked.connect(self.open_file_folder)
        self.right_panel.addWidget(self.open_folder_button)

        # Copy File Path Button
        self.copy_path_button = QtWidgets.QPushButton("Copy File Path")
        self.copy_path_button.clicked.connect(self.copy_file_path)
        self.right_panel.addWidget(self.copy_path_button)

        # Refresh List Button
        self.refresh_button = QtWidgets.QPushButton("Refresh List")
        self.refresh_button.clicked.connect(self.refresh_list)
        self.right_panel.addWidget(self.refresh_button)

        # Close Button
        self.close_button = QtWidgets.QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        self.right_panel.addWidget(self.close_button)

        # Add right panel to content layout
        self.content_layout.addLayout(self.right_panel)

        # Add content layout to main layout
        self.main_layout.addLayout(self.content_layout)

        # Footer Layout
        self.footer_layout = QtWidgets.QHBoxLayout()
        self.footer_layout.addStretch()  # Add stretch to push the label to the center
        self.footer_label = QtWidgets.QLabel("Developed by: Mahmoud Farouk", self)
        self.footer_label.setObjectName("footerLabel")
        self.footer_label.setAlignment(QtCore.Qt.AlignCenter)  # Center align the footer text
        self.footer_layout.addWidget(self.footer_label)
        self.footer_layout.addStretch()  # Add stretch to push the label to the center
        self.main_layout.addLayout(self.footer_layout)

        # Keyboard Shortcuts
        self.open_selected_comp_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+O"), self)
        self.open_selected_comp_shortcut.activated.connect(self.open_selected_comp)

        # Search Timer for better performance
        self.search_timer = QtCore.QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.filter_list)

        # Populate the table with recent files and additional info
        self.populate_recent_files()

        # Enable mouse wheel event for scrolling
        self.table_widget.wheelEvent = self.scroll_table

    def open_snipping_tool(self):
        """Open the Snipping Tool on Windows."""
        if os.name == "nt":  # Windows
            os.system("SnippingTool")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Snipping Tool is only available on Windows.")

    def scroll_table(self, event):
        """Enable scrolling in the table."""
        scroll_bar = self.table_widget.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.value() - event.angleDelta().y())

    def get_thumbnail_icon(self, file_path, size=130):
        """Get a thumbnail icon based on file type."""
        # Get the directory of the file
        file_dir = os.path.dirname(file_path)
        
        # Check if the directory exists
        if os.path.exists(file_dir):
            # Search for any image file in the directory
            for file_name in os.listdir(file_dir):
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                    thumbnail_path = os.path.join(file_dir, file_name)
                    try:
                        # Load the image and scale it to the desired size
                        thumbnail = QtGui.QPixmap(thumbnail_path).scaled(size, size, QtCore.Qt.KeepAspectRatio)
                        return QtGui.QIcon(thumbnail)
                    except Exception as e:
                        print("Error loading thumbnail {}: {}".format(thumbnail_path, e))  # Replaced f-string with .format()
                        break  # Exit the loop if there's an error loading the image
        
        # If no image is found, return a default file icon
        return self.style().standardIcon(QtWidgets.QStyle.SP_FileIcon)

    def populate_recent_files(self):
        """Populate the table with Nuke's recent files and additional info."""
        recent_files = self.get_recent_files()
        self.table_widget.setRowCount(len(recent_files))  # Set number of rows

        for row, file_path in enumerate(recent_files):
            # Full Path
            item_file = QtWidgets.QTableWidgetItem(file_path)
            item_file.setIcon(self.get_thumbnail_icon(file_path, self.table_widget.iconSize().width()))  # File icon
            self.table_widget.setItem(row, 0, item_file)

            # Last Modified Date and Time
            if os.path.exists(file_path):
                mod_time = os.path.getmtime(file_path)
                mod_time_str = datetime.datetime.fromtimestamp(mod_time)
                date_str = mod_time_str.strftime('%Y-%m-%d')  
                time_str = mod_time_str.strftime('%I:%M:%S %p')  
            else:
                date_str = "N/A"
                time_str = "N/A"

            # Date Column
            item_date = QtWidgets.QTableWidgetItem(date_str)
            self.table_widget.setItem(row, 1, item_date)

            # Time Column
            item_time = QtWidgets.QTableWidgetItem(time_str)
            self.table_widget.setItem(row, 2, item_time)

            # Nuke Version (extracted from the file)
            nuke_version = self.get_nuke_version(file_path)
            item_version = QtWidgets.QTableWidgetItem(nuke_version)
            self.table_widget.setItem(row, 3, item_version)

        # Adjust column widths
        self.table_widget.setColumnWidth(0, 560)  # Full Path column width
        self.table_widget.setColumnWidth(1, 100)  # Date column width
        self.table_widget.setColumnWidth(2, 100)  # Time column width
        self.table_widget.setColumnWidth(3, 110)  # Nuke Version column width

        # Set row height to be 3 times the default height
        default_row_height = self.table_widget.rowHeight(0)
        self.table_widget.setRowHeight(0, default_row_height * 3)
        for row in range(self.table_widget.rowCount()):
            self.table_widget.setRowHeight(row, default_row_height * 3)

    def get_nuke_version(self, file_path):
        """Extract the full Nuke version from the .nk file."""
        if not os.path.exists(file_path):
            return "N/A"

        try:
            with open(file_path, "r") as file:
                for line in file:
                    if "version" in line:
                        # Extract the full version string
                        version_line = line.strip()
                        version = version_line.split("version ")[-1]  # Get everything after "version "
                        return "Nuke {}".format(version)
        except Exception as e:
            print("Error reading file {}: {}".format(file_path, e))  # Replaced f-string with .format()
        return "N/A"

    def start_search_timer(self):
        """Start the search timer to improve performance."""
        self.search_timer.start(300)  # Delay search by 300ms

    def filter_list(self):
        """Filter the list based on the search bar text."""
        search_text = self.search_bar.text().lower()
        for row in range(self.table_widget.rowCount()):
            item = self.table_widget.item(row, 0)  # Search in the Full Path column
            if item:
                item_text = item.text().lower()
                self.table_widget.setRowHidden(row, search_text not in item_text)

    def get_recent_files(self):
        """Get the list of recent files from Nuke's recent_files file."""
        recent_files = []
        home_directory = os.path.expanduser("~")
        nuke_directory = os.path.join(home_directory, ".nuke")
        recent_files_path = os.path.join(nuke_directory, "recent_files")

        if os.path.exists(recent_files_path):
            with open(recent_files_path, "r") as file:
                recent_files = file.read().splitlines()
        else:
            print("File not found: {}".format(recent_files_path))  # Replaced f-string with .format()

        return recent_files

    def save_recent_files(self, recent_files):
        """Save the updated list of recent files."""
        home_directory = os.path.expanduser("~")
        nuke_directory = os.path.join(home_directory, ".nuke")
        recent_files_path = os.path.join(nuke_directory, "recent_files")
        with open(recent_files_path, "w") as file:
            file.write("\n".join(recent_files))

    def open_new_comp(self):
        """Open a new comp in Nuke."""
        self.close()
        QtCore.QTimer.singleShot(100, nuke.scriptNew)

    def open_selected_comp(self):
        """Open the selected comp directly."""
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            file_path = self.table_widget.item(selected_row, 0).text()
            if os.path.exists(file_path):
                self.close()
                QtCore.QTimer.singleShot(100, lambda: nuke.scriptOpen(file_path))
                self.play_sound()  # Play a sound notification
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "File not found: {}".format(file_path))  # Replaced f-string with .format()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a comp!")

    def delete_selected_file(self):
        """Delete the selected file from the recent files list."""
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            file_path = self.table_widget.item(selected_row, 0).text()
            if os.path.exists(file_path):
                recent_files = self.get_recent_files()
                recent_files.remove(file_path)
                self.save_recent_files(recent_files)
                self.table_widget.removeRow(selected_row)
                QtWidgets.QMessageBox.information(self, "Success", "Deleted: {}".format(file_path))  # Replaced f-string with .format()
                self.play_sound()  # Play a sound notification
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "File not found: {}".format(file_path))  # Replaced f-string with .format()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a file to delete!")

    def open_file_folder(self):
        """Open the folder containing the selected file."""
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            file_path = self.table_widget.item(selected_row, 0).text()
            if os.path.exists(file_path):
                folder_path = os.path.dirname(file_path)
                if os.name == "nt":  # Windows
                    os.startfile(folder_path)
                elif os.name == "posix":  # macOS or Linux
                    os.system('open "{}"'.format(folder_path) if sys.platform == "darwin" else 'xdg-open "{}"'.format(folder_path))
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "File not found: {}".format(file_path))  # Replaced f-string with .format()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a file!")

    def copy_file_path(self):
        """Copy the selected file path to the clipboard."""
        selected_row = self.table_widget.currentRow()
        if selected_row >= 0:
            file_path = self.table_widget.item(selected_row, 0).text()
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText(file_path)
            QtWidgets.QMessageBox.information(self, "Success", "Copied: {}".format(file_path))  # Replaced f-string with .format()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a file!")

    def refresh_list(self):
        """Refresh the list of recent files."""
        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)
        self.populate_recent_files()

    def play_sound(self):
        """Play a sound notification."""
        if os.name == "nt":  # Windows
            import winsound
            winsound.Beep(1000, 200)  # Simple beep sound

def open_recent_files_browser():
    """Open the Recent Files Browser window as a popup."""
    global recent_files_browser
    try:
        recent_files_browser.close()  # Close the window if it's already open
    except:
        pass
    recent_files_browser = RecentFilesBrowser()
    recent_files_browser.show()

# Add the tool to Nuke's menu
#nuke.menu("Nuke").addCommand("Tools/Recent Files Browser", open_recent_files_browser)
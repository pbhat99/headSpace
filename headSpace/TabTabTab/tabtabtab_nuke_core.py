"""tabtabtab — app-agnostic command palette core

homepage: https://github.com/dbr/tabtabtab-nuke
license: http://unlicense.org/
"""

__version__ = "2.0"

import os
import re

try:
    from PySide6 import QtCore, QtGui, QtWidgets
    from PySide6.QtCore import Qt
except ImportError:
    from PySide2 import QtCore, QtGui, QtWidgets
    from PySide2.QtCore import Qt


# Search mode identifiers used by the space-prefix mapping preference.
MODE_ANCHORED_FUZZY = "anchored_fuzzy"
MODE_NON_ANCHORED_FUZZY = "non_anchored_fuzzy"
MODE_CONSECUTIVE = "consecutive"

VALID_MODES = {MODE_ANCHORED_FUZZY, MODE_NON_ANCHORED_FUZZY, MODE_CONSECUTIVE}

DEFAULT_SPACE_MODE_ORDER = [
    MODE_ANCHORED_FUZZY,       # 0 spaces (default)
    MODE_NON_ANCHORED_FUZZY,   # 1 space
    MODE_CONSECUTIVE,          # 2 spaces
]


class TabTabTabPlugin:
    def get_items(self):
        """Return list of {'menuobj': ..., 'menupath': str} dicts."""
        raise NotImplementedError

    def get_weights_file(self):
        """Return path to JSON weights file, or None to skip persistence."""
        raise NotImplementedError

    def invoke(self, thing):
        """Trigger the selected menu item."""
        raise NotImplementedError

    def get_icon(self, menuobj):
        """Return a QIcon for menuobj, or None.
        Default works for any Qt object whose .icon() returns a QIcon."""
        try:
            icon = menuobj.icon()
            if isinstance(icon, QtGui.QIcon) and not icon.isNull():
                return icon
        except Exception:
            pass
        return None

    def get_color(self, menuobj):
        """Return a (left_block_color, text_tint_color) tuple of QtGui.QColor or None.

        left_block_color: solid colour filling the icon-width column on the left.
          Use None when an icon is present (or when no left-block colour is wanted).
        text_tint_color: semi-transparent wash applied only behind the text area,
          also controls foreground text colour via luminance.
        Either element may be None to suppress that part of the colouring.
        """
        return (None, None)

    def invalidate_cache(self):
        """Optional hook called after the popup closes so the next get_items()
        and get_color() return fresh data.

        Override to drop any plugin-side caches (e.g., a recursive menu walk
        or per-class colour memoisation). Default is a no-op for plugins that
        don't cache.
        """
        pass


def _normalize_qt_item_name(item):
    item_name = item.text()
    item_name = item_name.replace("&", "")
    item_name = re.sub(r'^\s*\d+ \s*', '', item_name).strip()
    return item_name


def _traverse_qt_menu(menu, _path=None):
    """Recursively traverse a QMenu, returning list of {'menuobj', 'menupath'} dicts."""
    found = []

    if not menu.isEnabled():
        return []

    for item in menu.actions():
        if not (item.isVisible() and item.isEnabled()):
            continue

        item_name = _normalize_qt_item_name(item)
        submenu = item.menu()

        if submenu:
            subpath = "/".join(x for x in (_path, item_name) if x is not None)
            found.extend(_traverse_qt_menu(submenu, _path=subpath))
        else:
            if item.data() == "":
                # skip if no actual action
                continue
            if item.text() == "":
                # Skip dividers
                continue

            subpath = "/".join(x for x in (_path, item_name) if x is not None)
            found.append({'menuobj': item, 'menupath': subpath})

    return found


def find_qt_menu_items(menubar):
    """Traverse a QMenuBar and return all leaf menu items.

    Returns a list of {'menuobj': QAction, 'menupath': str} dicts.
    Usable by any Qt app plugin without importing anything app-specific.
    """
    items = []
    for action in menubar.actions():
        if action.menu():
            items.extend(_traverse_qt_menu(action.menu(), _path=action.text()))
    return items


def consec_find(needle, haystack, anchored=False):
    ''' searches for the "needle" string in the "haystack" string.
        added to tabtabtab as a way to prioritize more relevant results.
    '''

    if "[" not in needle:
        haystack = haystack.rpartition(" [")[0]

    stripped_haystack = haystack.replace(' ', '').replace('-', '').replace('_', '')

    if anchored:
        if haystack.startswith(needle) or stripped_haystack.startswith(needle):
            return True

    else:
        if needle in haystack or needle in stripped_haystack:
            return True
    return False


def nonconsec_find(needle, haystack, anchored=False):
    """checks if each character of "needle" can be found in order (but not
    necessarily consecutivly) in haystack.
    For example, "mm" can be found in "matchmove", but not "move2d"
    "m2" can be found in "move2d", but not "matchmove"

    >>> nonconsec_find("m2", "move2d")
    True
    >>> nonconsec_find("m2", "matchmove")
    False

    Anchored ensures the first letter matches

    >>> nonconsec_find("atch", "matchmove", anchored = False)
    True
    >>> nonconsec_find("atch", "matchmove", anchored = True)
    False
    >>> nonconsec_find("match", "matchmove", anchored = True)
    True

    If needle starts with a string, non-consecutive searching is disabled:

    >>> nonconsec_find(" mt", "matchmove", anchored = True)
    False
    >>> nonconsec_find(" ma", "matchmove", anchored = True)
    True
    >>> nonconsec_find(" oe", "matchmove", anchored = False)
    False
    >>> nonconsec_find(" ov", "matchmove", anchored = False)
    True
    """

    if "[" not in needle:
        haystack = haystack.rpartition(" [")[0]

    if len(haystack) == 0 and len(needle) > 0:
        # "a" is not in ""
        return False

    elif len(needle) == 0 and len(haystack) > 0:
        # "" is in "blah"
        return True

    elif len(needle) == 0 and len(haystack) == 0:
        # ..?
        return True

    # Turn haystack into list of characters (as strings are immutable)
    haystack = [hay for hay in str(haystack)]

    if needle.startswith(" "):
        # "[space]abc" does consecutive search for "abc" in "abcdef"
        if anchored:
            if "".join(haystack).startswith(needle.lstrip(" ")):
                return True
        else:
            if needle.lstrip(" ") in "".join(haystack):
                return True

    if anchored:
        if needle[0] != haystack[0]:
            return False
        else:
            # First letter matches, remove it for further matches
            needle = needle[1:]
            del haystack[0]

    for needle_atom in needle:
        try:
            needle_pos = haystack.index(needle_atom)
        except ValueError:
            return False
        else:
            # Dont find string in same pos or backwards again
            del haystack[:needle_pos + 1]
    return True


class NodeWeights(object):
    def __init__(self, fname=None):
        self.fname = fname
        self._weights = {}
        self._successful_load = False

    def load(self):
        if self.fname is None:
            return

        def _load_internal():
            import json
            if not os.path.isfile(self.fname):
                print("Weight file does not exist")
                return
            f = open(self.fname)
            self._weights = json.load(f)
            f.close()

        # Catch any errors, print traceback and continue
        try:
            _load_internal()
            self._successful_load = True
        except Exception:
            print("Error loading node weights.")
            import traceback
            traceback.print_exc()
            self._successful_load = False

    def save(self):
        if self.fname is None:
            print("Not saving node weights, no file specified")
            return

        if not self._successful_load:
            # Avoid clobbering existing weights file on load error
            print(("Not writing weights file because %r previously failed to load" % (
                self.fname)))
            return

        def _save_internal():
            import json
            ndir = os.path.dirname(self.fname)
            if not os.path.isdir(ndir):
                try:
                    os.makedirs(ndir)
                except OSError as e:
                    if e.errno != 17:  # errno 17 is "already exists"
                        raise

            f = open(self.fname, "w")
            # TODO: Limit number of saved items to some sane number
            json.dump(self._weights, fp=f)
            f.close()

        # Catch any errors, print traceback and continue
        try:
            _save_internal()
        except Exception:
            print("Error saving node weights")
            import traceback
            traceback.print_exc()

    def get(self, k, default=0):
        if len(list(self._weights.values())) == 0:
            maxval = 1.0
        else:
            maxval = max(self._weights.values())
            maxval = max(1, maxval)
            maxval = float(maxval)

        return self._weights.get(k, default) / maxval

    def increment(self, key):
        self._weights.setdefault(key, 0)
        self._weights[key] += 1


class NodeModel(QtCore.QAbstractListModel):
    def __init__(self, mlist, weights, num_items=18, filtertext="", icon_fn=None, color_fn=None, space_mode_order=None):
        super(NodeModel, self).__init__()

        self.weights = weights
        self.num_items = num_items

        self._all = mlist
        self._filtertext = filtertext
        self._icon_fn = icon_fn if icon_fn is not None else (lambda obj: None)
        self._color_fn = color_fn if color_fn is not None else (lambda obj: (None, None))

        if (space_mode_order is not None
                and len(space_mode_order) == len(DEFAULT_SPACE_MODE_ORDER)
                and all(m in VALID_MODES for m in space_mode_order)):
            self._space_mode_order = list(space_mode_order)
        else:
            self._space_mode_order = list(DEFAULT_SPACE_MODE_ORDER)

        # _items is the list of objects to be shown, update sets this
        self._items = []
        self.update()

    def set_filter(self, filtertext):
        self._filtertext = filtertext
        self.update()

    def refresh_items(self, mlist):
        self._all = mlist
        self.update()

    def update(self):
        filtertext = self._filtertext.lower()

        anchored = True
        force_non_anchored = False
        force_consecutive = False

        # Determine space-prefix level (0, 1, or 2 leading spaces)
        if filtertext.startswith('  '):
            space_level = 2
            filtertext = filtertext[2:]
        elif filtertext.startswith(' '):
            space_level = 1
            filtertext = filtertext[1:]
        # * or [ prefix: non-anchored fuzzy (legacy shortcuts, unchanged)
        elif filtertext.startswith('*') or filtertext.startswith('['):
            space_level = None
            anchored = False
            filtertext = filtertext.replace("*", "", 1)
            if filtertext.startswith('*'):
                force_non_anchored = True
            filtertext = filtertext.replace("*", "")
        else:
            space_level = 0

        # Apply mode from the configurable space-prefix mapping
        if space_level is not None:
            mode = self._space_mode_order[space_level]
            if mode == MODE_ANCHORED_FUZZY:
                anchored = True
            elif mode == MODE_NON_ANCHORED_FUZZY:
                anchored = False
            elif mode == MODE_CONSECUTIVE:
                anchored = False
                force_consecutive = True

        scored_a = []
        scored_b = []
        for n in self._all:
            # Turn "3D/Shader/Phong" into "Phong [3D/Shader]"
            menupath = n['menupath'].replace("&", "")
            uiname = "%s [%s]" % (menupath.rpartition("/")[2], menupath.rpartition("/")[0])
            search_string = uiname.lower()

            if force_non_anchored:
                search_string = search_string[1:]

            shortcut = n.get('shortcut')
            display_text = "%s (%s)" % (uiname, shortcut) if shortcut else uiname

            if consec_find(filtertext, search_string, anchored):
                # Matches, get weighting and add to list of stuff
                score = self.weights.get(n['menupath'])

                scored_a.append({
                    'text': uiname,
                    'display_text': display_text,
                    'menupath': n['menupath'],
                    'menuobj': n['menuobj'],
                    'score': score,
                    'color': self._color_fn(n['menuobj'])})

            elif not force_consecutive and nonconsec_find(filtertext, search_string, anchored):
                # Matches, get weighting and add to list of stuff
                score = self.weights.get(n['menupath'])

                scored_b.append({
                    'text': uiname,
                    'display_text': display_text,
                    'menupath': n['menupath'],
                    'menuobj': n['menuobj'],
                    'score': score,
                    'color': self._color_fn(n['menuobj'])})

        # Sort based on scores (descending), then alphabetically
        sort_a = sorted(scored_a, key=lambda k: (-k['score'], k['text']))
        sort_b = sorted(scored_b, key=lambda k: (-k['score'], k['text']))
        s = sort_a + sort_b

        self._items = s
        self.modelReset.emit()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return min(self.num_items, len(self._items))

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            item = self._items[index.row()]
            return item.get('display_text', item['text'])

        elif role == Qt.DecorationRole:
            icon = self._icon_fn(self._items[index.row()]['menuobj'])
            if isinstance(icon, QtGui.QIcon) and not icon.isNull():
                return icon
            return None

        elif role == Qt.BackgroundRole:
            left_block_color, text_tint_color = self._items[index.row()]['color']
            if text_tint_color is None:
                return None
            tinted = QtGui.QColor(text_tint_color.red(), text_tint_color.green(), text_tint_color.blue(), 80)  # 31% opacity
            return QtGui.QBrush(tinted)

        elif role == Qt.ForegroundRole:
            _, text_tint_color = self._items[index.row()]['color']
            if text_tint_color is None:
                return None
            luminance = 0.299 * text_tint_color.red() + 0.587 * text_tint_color.green() + 0.114 * text_tint_color.blue()
            if luminance > 160:
                return QtGui.QBrush(QtGui.QColor(40, 40, 40))
            else:
                return QtGui.QBrush(QtGui.QColor(220, 220, 220))

        elif role == Qt.UserRole:
            left_block_color, _ = self._items[index.row()]['color']
            return left_block_color

        else:
            return None

    def getorig(self, selected):
        # TODO: Is there a way to get this via data()? There's no
        # Qt.DataRole or something (only DisplayRole)

        if len(selected) > 0:
            # Get first selected index
            selected = selected[0]

        else:
            # Nothing selected, get first index
            selected = self.index(0)

        # TODO: Maybe check for IndexError?
        selected_data = self._items[selected.row()]
        return selected_data


class TabyLineEdit(QtWidgets.QLineEdit):
    pressed_arrow = QtCore.Signal(str)
    cancelled = QtCore.Signal()

    def event(self, event):
        """Make tab trigger returnPressed

        Also emit signals for the up/down arrows, and escape.
        """

        is_keypress = event.type() == QtCore.QEvent.KeyPress

        if is_keypress and event.key() == QtCore.Qt.Key_Tab:
            # Can't access tab key in keyPressedEvent
            self.returnPressed.emit()
            return True

        elif is_keypress and event.key() == QtCore.Qt.Key_Up:
            # These could be done in keyPressedEvent, but.. this is already here
            self.pressed_arrow.emit("up")
            return True

        elif is_keypress and event.key() == QtCore.Qt.Key_Down:
            self.pressed_arrow.emit("down")
            return True

        elif is_keypress and event.key() == QtCore.Qt.Key_Escape:
            self.cancelled.emit()
            return True

        else:
            return super(TabyLineEdit, self).event(event)


class _ItemDelegate(QtWidgets.QStyledItemDelegate):
    """Custom delegate: fixed row height, full-width tinted background,
    solid colour icon block, and outline-only selection highlight."""

    def __init__(self, height, icon_w, parent=None):
        super(_ItemDelegate, self).__init__(parent)
        self._height = height
        self._icon_w = icon_w

    def sizeHint(self, option, index):
        sh = super(_ItemDelegate, self).sizeHint(option, index)
        return QtCore.QSize(sh.width(), self._height)

    def paint(self, painter, option, index):
        painter.save()
        rect = option.rect

        # Determine what occupies the left icon column so we can compute the
        # text rect before drawing anything (the background wash uses it).
        left_block_color = index.data(Qt.UserRole)  # solid colour block, or None
        icon = index.data(Qt.DecorationRole)
        has_icon = isinstance(icon, QtGui.QIcon) and not icon.isNull()

        # Always reserve the left block space — text is always indented the same amount.
        text_left = rect.left() + self._icon_w + 6
        text_rect = QtCore.QRect(text_left, rect.top(), rect.right() - text_left, rect.height())

        # 1. Tinted background wash — from the right edge of the left block to
        # the end of the row, so there is no uncoloured gap before the text.
        bg_brush = index.data(Qt.BackgroundRole)
        if bg_brush is not None:
            bg_left = rect.left() + self._icon_w
            bg_rect = QtCore.QRect(bg_left, rect.top(), rect.right() - bg_left, rect.height())
            painter.fillRect(bg_rect, bg_brush)

        # 2. Left icon column: solid colour block as background (neutral grey when no colour),
        # then QIcon on top.
        icon_rect = QtCore.QRect(rect.left(), rect.top(), self._icon_w, rect.height())
        block_fill = left_block_color if left_block_color is not None else QtGui.QColor(50, 50, 50)
        painter.fillRect(icon_rect, block_fill)
        if has_icon:
            icon_size = min(self._icon_w, rect.height()) - 4
            icon_x = rect.left() + (self._icon_w - icon_size) // 2
            icon_y = rect.top() + (rect.height() - icon_size) // 2
            icon.paint(painter, icon_x, icon_y, icon_size, icon_size)

        # 3. Selection as outline only (1px border, highlight colour)
        if option.state & QtWidgets.QStyle.State_Selected:
            pen = QtGui.QPen(option.palette.highlight().color(), 1)
            painter.setPen(pen)
            painter.drawRect(rect.adjusted(0, 0, -1, -1))

        # 4. Text
        fg = index.data(Qt.ForegroundRole)
        painter.setPen(fg.color() if fg else option.palette.text().color())
        text = index.data(Qt.DisplayRole) or ""
        painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, text)

        painter.restore()


class TabTabTabWidget(QtWidgets.QDialog):
    def __init__(self, plugin, parent=None, winflags=None, space_mode_order=None):
        super(TabTabTabWidget, self).__init__(parent=parent)
        if winflags is not None:
            self.setWindowFlags(winflags)

        self.plugin = plugin

        # Input box
        self.input = TabyLineEdit()

        # Node weighting
        self.weights = NodeWeights(plugin.get_weights_file())
        self.weights.load()  # weights.save() called in close method

        items = plugin.get_items()

        # List of stuff, and associated model
        self.things_model = NodeModel(items, weights=self.weights, icon_fn=plugin.get_icon, color_fn=plugin.get_color, space_mode_order=space_mode_order)
        self.things = QtWidgets.QListView()
        self.things.setModel(self.things_model)
        self.things.setUniformItemSizes(True)
        self.input.setFont(self.things.font())

        _font_h = self.things.fontMetrics().height()
        _row_h = _font_h * 2
        self.things.setItemDelegate(_ItemDelegate(_row_h, _row_h, self.things))
        self.things.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.input.setTextMargins(2, _font_h // 2, 2, _font_h // 2)

        # Add input and items to layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.things)

        self.setLayout(layout)

        # Update on text change
        self.input.textChanged.connect(self.update)

        # Reset selection on text change
        self.input.textChanged.connect(lambda: self.move_selection(where="first"))
        self.move_selection(where="first")  # Set initial selection

        # Create node when enter/tab is pressed, or item is clicked
        self.input.returnPressed.connect(self.create)
        self.things.clicked.connect(self.create)

        # When esc pressed, close
        self.input.cancelled.connect(self.close)

        # Up and down arrow handling
        self.input.pressed_arrow.connect(self.move_selection)

        self._resize_list_to_contents()

        self.adjustSize()
        self.setMinimumWidth(self.width() * 2)

    def _resize_list_to_contents(self):
        """Set list height to always show num_items rows, giving a fixed popup size."""
        num_rows = self.things_model.num_items

        row_h = self.things.sizeHintForRow(0)
        if row_h <= 0:
            row_h = 20  # fallback row height in pixels

        try:
            fw = self.things.frameWidth()
        except Exception:
            fw = 0

        total_h = row_h * num_rows + self.things.spacing() * max(0, num_rows - 1) + 2 * fw
        self.things.setFixedHeight(total_h)

    def under_cursor(self):
        def clamp(val, mi, ma):
            return max(min(val, ma), mi)

        # Get cursor position, and screen dimensions on active screen
        cursor = QtGui.QCursor().pos()
        screen_obj = None
        if hasattr(QtWidgets.QApplication, 'screenAt'):
            screen_obj = QtWidgets.QApplication.screenAt(cursor)
        if screen_obj is None:
            screen_obj = self.screen()
        screen = screen_obj.geometry()

        # Get window position so cursor is just over text input
        xpos = cursor.x() - (self.width() / 2)
        ypos = cursor.y() - 13

        # Clamp window location to prevent it going offscreen
        xpos = clamp(xpos, screen.left(), screen.right() - self.width())
        ypos = clamp(ypos, screen.top(), screen.bottom() - (self.height() - 13))

        # Move window
        self.move(xpos, ypos)

    def move_selection(self, where):
        if where not in ["first", "up", "down"]:
            raise ValueError("where should be either 'first', 'up', 'down', not %r" % (
                where))

        first = where == "first"
        up = where == "up"
        down = where == "down"

        if first:
            self.things.setCurrentIndex(self.things_model.index(0))
            return

        cur = self.things.currentIndex()
        if up:
            new = cur.row() - 1
            if new < 0:
                new = self.things_model.rowCount() - 1
        elif down:
            new = cur.row() + 1
            count = self.things_model.rowCount()
            if new > count - 1:
                new = 0

        self.things.setCurrentIndex(self.things_model.index(new))

    def event(self, event):
        """Close when window becomes inactive (click outside of window)"""
        if event.type() == QtCore.QEvent.WindowDeactivate:
            self.close()
            return True
        else:
            return super(TabTabTabWidget, self).event(event)

    def update(self, text):
        """On text change, selects first item and updates filter text"""
        self.things.setCurrentIndex(self.things_model.index(0))
        self.things_model.set_filter(text)

    def show(self):
        """Select all the text in the input (which persists between
        show()'s)

        Allows typing over previously created text, and [tab][tab] to
        create previously created node (instead of the most popular)
        """

        # Show the widget and focus the input *before* doing any heavy work.
        # Reloading weights from disk and re-walking the host application's
        # menus can take 100-400ms; if those run synchronously here, queued
        # KeyPress events arrive before the line-edit is ready and the user's
        # first character or two get lost (issue #3). Deferring via
        # singleShot(0) lets Qt drain pending input events into the now-
        # focused line-edit before the refresh blocks the GUI thread again.
        self.input.selectAll()
        super(TabTabTabWidget, self).show()
        self.input.setFocus()

        QtCore.QTimer.singleShot(0, self._refresh_after_show)

    def _refresh_after_show(self):
        """Reload weights and refresh items from the plugin.

        Runs on the next event-loop tick after show() so the user's first
        keystrokes land in the line-edit even though this work is slow.
        """
        # Load the weights everytime the panel is shown, to prevent
        # overwritting weights from other instances
        self.weights.load()

        # Refresh items from the plugin so additions/removals are reflected
        self.things_model.refresh_items(self.plugin.get_items())

        # Restore selection to the first item, since modelReset clears it
        self.move_selection(where="first")

    def close(self):
        """Save weights, close the dialog, and schedule a belt-and-suspenders
        cache invalidation + refresh.

        The refresh on show() is the primary freshness mechanism — it walks
        the plugin's items every open via _refresh_after_show, using the
        plugin's own cache to skip the walk when nothing has changed. That's
        adequate for hosts whose indexed items rarely change at runtime
        (e.g. Nuke's node menus). For hosts where the indexed set changes
        often during a session (e.g. tabtabtab_anchors indexing live nodes
        in the script), or where the plugin's cache-validity check might
        miss something (e.g. a deeply nested submenu install that a shallow
        fingerprint doesn't sample), this hook ensures the cache is forcibly
        invalidated and rewalked between every close and the next open.
        """
        self.weights.save()
        super(TabTabTabWidget, self).close()
        QtCore.QTimer.singleShot(0, self._refresh_after_close)

    def _refresh_after_close(self):
        """Force a cache invalidation and a fresh walk in the background
        after the popup closes. No-op if the user has already reopened the
        popup before this fires — the show-time refresh will handle it.
        """
        if self.isVisible():
            return
        self.plugin.invalidate_cache()
        self.things_model.refresh_items(self.plugin.get_items())

    def create(self):
        # Get selected item
        selected = self.things.selectedIndexes()
        if len(selected) == 0:
            return

        thing = self.things_model.getorig(selected)

        # Store the full UI name of the created node, so it is the
        # active node on the next [tab]. Prefix it with space,
        # to disable substring matching
        if thing['text'].startswith(" "):
            prev_string = thing['text']
        else:
            prev_string = " %s" % thing['text']

        self.input.setText(prev_string)

        # Invoke item, increment weight and close
        self.plugin.invoke(thing)
        self.weights.increment(thing['menupath'])
        self.close()


_tabtabtab_instance = None
# Strong reference to a preloaded but never-yet-shown widget. Released
# either on first show() (Qt's window registry takes over) or on
# QApplication.aboutToQuit (whichever comes first), so the original
# weakref-only lifetime pattern that avoids the on-exit segfault from
# https://github.com/dbr/tabtabtab-nuke/issues/4 is restored before
# host-application shutdown even if the user never opens the popup.
_preloaded_instance = None


def launch(plugin, space_mode_order=None):
    global _tabtabtab_instance, _preloaded_instance

    if _tabtabtab_instance is not None:
        # TODO: Is there a better way of doing this? If a
        # TabTabTabWidget is instanced, it goes out of scope at end of
        # function and disappers instantly. This seems like a
        # reasonable "workaround"
        try:
            # Update space mode order on reuse so pref changes take
            # effect without restarting the host application.
            if (space_mode_order is not None
                    and len(space_mode_order) == len(DEFAULT_SPACE_MODE_ORDER)
                    and all(m in VALID_MODES for m in space_mode_order)):
                _tabtabtab_instance.things_model._space_mode_order = list(space_mode_order)
            _tabtabtab_instance.under_cursor()
            _tabtabtab_instance.show()
            _tabtabtab_instance.raise_()
            # Once the widget has been shown, Qt holds it alive via its
            # window registry. Drop the preload strong reference so we
            # match the original lifetime model from here on.
            _preloaded_instance = None
            return
        except ReferenceError:
            _tabtabtab_instance = None
            _preloaded_instance = None

    t = TabTabTabWidget(plugin, winflags=Qt.FramelessWindowHint, space_mode_order=space_mode_order)

    # Make dialog appear under cursor, as Nuke's builtin one does
    t.under_cursor()

    # Show, and make front-most window (mostly for OS X)
    t.show()
    t.raise_()

    # Keep the TabTabTabWidget alive, but don't keep an extra
    # reference to it, otherwise Nuke segfaults on exit. Hacky.
    # https://github.com/dbr/tabtabtab-nuke/issues/4
    import weakref
    _tabtabtab_instance = weakref.proxy(t)


def preload(plugin, space_mode_order=None):
    """Eagerly construct the popup widget so the first user invocation hits
    the warm reuse path inside launch().

    Idempotent: returns immediately if an instance already exists (either
    from a previous preload or because the user invoked the popup before
    the deferred preload ran).

    Construction is ~30-50ms (menu walk + initial NodeModel build). Running
    that at host-plugin-load time blocks startup and may also race with
    the host's own menu population, so prefer schedule_preload() which
    defers via QTimer.singleShot(0, ...).
    """
    global _tabtabtab_instance, _preloaded_instance
    if _tabtabtab_instance is not None:
        return

    t = TabTabTabWidget(plugin, winflags=Qt.FramelessWindowHint, space_mode_order=space_mode_order)
    # Hold a strong reference until first show(); without this the proxy
    # below would dangle the moment this function returns because Qt's
    # window registry only tracks widgets that have been shown.
    _preloaded_instance = t

    # Defensively release the strong reference before the host application
    # quits, even if the user never opens the popup. Holding an extra ref
    # to the widget through Qt shutdown has caused segfaults historically
    # (dbr/tabtabtab-nuke#4); aboutToQuit fires before Qt's cleanup pass,
    # so dropping the ref here puts us back into the original weakref-
    # only model in time.
    app = QtWidgets.QApplication.instance()
    if app is not None:
        app.aboutToQuit.connect(_release_preloaded_instance)

    import weakref
    _tabtabtab_instance = weakref.proxy(t)


def _release_preloaded_instance():
    """aboutToQuit handler: drop strong + weak references to the preloaded
    widget so Qt can tear it down without an extra Python reference
    holding the wrapper alive past the C++ object's destruction.
    """
    global _preloaded_instance, _tabtabtab_instance
    _preloaded_instance = None
    _tabtabtab_instance = None


def schedule_preload(plugin, space_mode_order=None):
    """Defer preload() to the next event-loop tick.

    Use this from the host's plugin entry point. Deferring guarantees
    (a) that startup isn't blocked by widget construction and (b) that
    the host's own menu population is complete before we walk it.
    """
    QtCore.QTimer.singleShot(
        0,
        lambda: preload(plugin, space_mode_order=space_mode_order),
    )

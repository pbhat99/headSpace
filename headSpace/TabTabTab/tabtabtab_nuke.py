import os
import re
import nuke

try:
    from PySide6 import QtGui
except ImportError:
    from PySide2 import QtGui

from tabtabtab_nuke_core import TabTabTabPlugin, launch, schedule_preload
import tabtabtab_prefs


def _extract_node_class_from_script(script_text):
    """Parse a menu item's command string for the actual node class name."""
    if not script_text:
        return None
    # Python form: any module calling createNode or createNodeLocal
    # e.g. nuke.createNode("ScanlineRender2") or nukescripts.createNodeLocal("ScanlineRender2")
    match = re.search(r'createNode(?:Local)?\s*\(\s*["\'](\w+)["\']', script_text)
    if match:
        return match.group(1)
    # Tcl form: bare class name as the entire command
    match = re.match(r'^(\w+)$', script_text.strip())
    if match:
        return match.group(1)
    return None


def _menu_fingerprint(menu, depth=2):
    """Cheap fingerprint of a Nuke menu using only item names.

    Used to detect whether a full re-walk via _find_nuke_menu_items is
    needed. Calling .name() on items is essentially free; .script() and
    .shortcut() (the expensive calls) are deliberately avoided here.

    Recurses `depth` levels so common gizmo / menu installs are detected
    without paying for a full traversal. Deep additions buried below the
    fingerprint depth (e.g. a new ToolSet several levels in) are missed
    by this fast-path check, but the belt-and-suspenders refresh in
    TabTabTabWidget._refresh_after_close calls invalidate_cache() on
    every popup close, so deep changes are still picked up — at most
    one stale popup behind any given mid-session change.
    """
    parts = []
    try:
        for item in menu.items():
            name = item.name()
            if isinstance(item, nuke.Menu):
                if depth > 1:
                    parts.append(("M", name, _menu_fingerprint(item, depth - 1)))
                else:
                    parts.append(("M", name))
            else:
                parts.append(("I", name))
    except Exception:
        return None
    return tuple(parts)


def _find_nuke_menu_items(menu, _path=None, is_node=True):
    """Extracts items from a given Nuke menu

    Returns a list of {'menuobj': ..., 'menupath': str, 'is_node': bool,
    'actual_class': str or None, 'shortcut': str or None} dicts.

    Ignores divider lines and hidden items (ones like "@;&CopyBranch" for shift+k)
    """
    found = []

    mi = list(menu.items())
    for i in mi:
        if isinstance(i, nuke.Menu):
            # Sub-menu, recurse
            mname = i.name().replace("&", "")
            subpath = "/".join(x for x in (_path, mname) if x is not None)

            if "ToolSets/Delete" in subpath:
                # Remove all ToolSets delete commands
                continue

            sub_found = _find_nuke_menu_items(menu=i, _path=subpath, is_node=is_node)
            found.extend(sub_found)
        elif isinstance(i, nuke.MenuItem):
            if i.name() == "":
                # Skip dividers
                continue
            if i.name().startswith("@;"):
                # Skip hidden items
                continue

            # Extract the actual node class from the command script
            actual_class = None
            try:
                script_text = i.script()
                actual_class = _extract_node_class_from_script(script_text)
            except Exception:
                pass
            if actual_class is None:
                actual_class = i.name()

            # Extract keyboard shortcut if available
            shortcut = None
            try:
                shortcut_str = i.shortcut()
                if shortcut_str:
                    shortcut = shortcut_str
            except Exception:
                pass

            subpath = "/".join(x for x in (_path, i.name()) if x is not None)
            found.append({
                'menuobj': i,
                'menupath': subpath,
                'is_node': is_node,
                'actual_class': actual_class,
                'shortcut': shortcut,
            })

    return found


class NukePlugin(TabTabTabPlugin):
    def __init__(self):
        self._menuobj_metadata = {}  # id(menuobj) -> {is_node, actual_class}
        self._cached_items = None
        self._cached_menu_fingerprint = None
        # actual_class -> (left_color, text_color) tuple
        self._color_cache = {}

    def get_items(self):
        """Return all menu items, using a cached result if menus haven't
        changed since the last walk.

        Walks both Nodes and Nuke menus only when a cheap fingerprint of
        those menus differs from the last walk, or when invalidate_cache()
        has been called. The expensive part of the walk is the .script()
        and .shortcut() calls inside _find_nuke_menu_items; the fingerprint
        avoids them entirely so the staleness check is essentially free.

        Belt-and-suspenders against fingerprint blind spots: TabTabTabWidget
        calls invalidate_cache() after every popup close, so deeply nested
        menu changes that the shallow fingerprint can't sample are still
        picked up at most one popup later.
        """
        fingerprint = (
            _menu_fingerprint(nuke.menu("Nodes")),
            _menu_fingerprint(nuke.menu("Nuke")),
        )
        if (self._cached_items is not None
                and self._cached_menu_fingerprint == fingerprint):
            return self._cached_items

        self._menuobj_metadata = {}
        node_items = _find_nuke_menu_items(nuke.menu("Nodes"), is_node=True)
        menu_items = _find_nuke_menu_items(nuke.menu("Nuke"), is_node=False)
        all_items = node_items + menu_items
        for item in all_items:
            self._menuobj_metadata[id(item['menuobj'])] = {
                'is_node': item['is_node'],
                'actual_class': item['actual_class'],
            }
        self._cached_items = all_items
        self._cached_menu_fingerprint = fingerprint
        # Menu set changed (or first walk) — drop colour cache too in case
        # new node classes appeared. Independent invalidation of the colour
        # cache for default-colour preference edits happens via
        # invalidate_cache() called from TabTabTabWidget._refresh_after_close.
        self._color_cache = {}
        return all_items

    def invalidate_cache(self):
        """Drop the items + fingerprint cache and the per-class colour
        cache. Called by TabTabTabWidget._refresh_after_close after every
        popup close so the next get_items() walks fresh data, regardless
        of whether the shallow menu fingerprint would have caught the
        change. Also clears colour memoisation so default-node-colour
        preference edits show up on the next open."""
        self._cached_items = None
        self._cached_menu_fingerprint = None
        self._color_cache = {}

    def get_weights_file(self):
        return os.path.expanduser("~/.nuke/tabtabtab_weights.json")

    def invoke(self, thing):
        thing['menuobj'].invoke()

    def get_icon(self, menuobj):
        icon_str = menuobj.icon()
        if not icon_str:
            return None
        # Search Nuke's plugin paths for the icon file
        for search_path in nuke.pluginPath():
            candidate = os.path.join(search_path, icon_str)
            if os.path.exists(candidate):
                return QtGui.QIcon(candidate)
        return None

    def get_color(self, menuobj):
        metadata = self._menuobj_metadata.get(id(menuobj), {})
        if not metadata.get('is_node', False):
            return (None, None)
        actual_class = metadata.get('actual_class', menuobj.name())
        cached = self._color_cache.get(actual_class)
        if cached is not None:
            return cached
        try:
            packed_color = nuke.defaultNodeColor(actual_class)
            if packed_color == 0:
                result = (None, None)
            else:
                # Skip nodes whose colour comes from the global preference default
                # rather than a class-specific setting.  We detect this by comparing
                # against what Nuke returns for a class name that cannot exist.
                global_default_color = nuke.defaultNodeColor("__tabtabtab_sentinel__")
                if packed_color == global_default_color:
                    result = (None, None)
                else:
                    r = (packed_color >> 24) & 0xFF
                    g = (packed_color >> 16) & 0xFF
                    b = (packed_color >> 8) & 0xFF
                    # Use the un-dimmed tile colour as the left-block background
                    # (drawn behind the icon) and as the text-area tint.
                    tile_color = QtGui.QColor(r, g, b)
                    result = (tile_color, tile_color)
        except Exception:
            result = (None, None)
        self._color_cache[actual_class] = result
        return result


_plugin = NukePlugin()

if nuke.NUKE_VERSION_MAJOR >= 9:
    _getParentMenu = lambda: nuke.menu("Node Graph")
else:
    _getParentMenu = lambda: nuke.menu("Nuke").findItem("Edit")


def registerNukeAction():
    menu = _getParentMenu()
    if menu.findItem("Tabtabtab") is None:
        menu.addCommand(
            "Tabtabtab",
            lambda: launch(
                _plugin,
                space_mode_order=tabtabtab_prefs.prefs_singleton.get("space_mode_order"),
            ),
            "^Tab",
        )

    # Eagerly construct the popup widget so the first user invocation hits
    # the warm reuse path inside launch() instead of paying ~30-50ms of
    # __init__ work (menu walk + initial NodeModel build). Deferred via
    # singleShot(0) so Nuke finishes populating its menus first.
    try:
        startup_space_mode_order = tabtabtab_prefs.prefs_singleton.get("space_mode_order")
    except Exception:
        startup_space_mode_order = None
    schedule_preload(_plugin, space_mode_order=startup_space_mode_order)


def unregisterNukeAction():
    _getParentMenu().removeItem("Tabtabtab")

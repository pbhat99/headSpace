# -*- coding: utf-8 -*-
""" Base script editor class for KnobScripter.

The KSScriptEditor is a QPlainTextEdit adapted for scripting: it provides a line number area,
and extended functionality for duplicating or moving lines.
Wouter Gilsing built an incredibly useful python script editor for his Hotbox Manager (v1.5).
Credit to him: http://www.woutergilsing.com/
Starting from his code, I changed the style and added extra functionality.

adrianpueyo.com

"""

import nuke
import re
import logging

try:
    if nuke.NUKE_VERSION_MAJOR < 11:
        from PySide import QtCore, QtGui, QtGui as QtWidgets
        from PySide.QtCore import Qt
    else:
        from PySide2 import QtWidgets, QtGui, QtCore
        from PySide2.QtCore import Qt
except ImportError:
    from Qt import QtCore, QtGui, QtWidgets

from KnobScripter import config, blinkhighlighter, pythonhighlighter


class KSScriptEditor(QtWidgets.QPlainTextEdit):
    """ Base Script Editor Widget

    Wouter Gilsing built an incredibly useful python script editor for his Hotbox Manager (v1.5).
    Credit to him: http://www.woutergilsing.com/
    Starting from his code, I changed the style and added extra functionality.
    """

    def __init__(self, knob_scripter=""):
        super(KSScriptEditor, self).__init__()

        self.knobScripter = knob_scripter
        self.selected_text = ""

        self.highlighter = None
        self.code_language = None

        # Setup line numbers
        self.tab_spaces = config.prefs["se_tab_spaces"]

        self.lineColor = None
        self.lineNumberAreaColor = None
        self.lineNumberColor = None
        self.currentLineNumberColor = None
        self.setColorStyle()
        self.setFont(config.script_editor_font)

        self.lineNumberArea = KSLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.updateLineNumberAreaWidth()

        # Highlight line
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

    def lineNumberAreaWidth(self):
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num /= 10
            digits += 1

        space = 7 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):

        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth()

    def resizeEvent(self, event):
        QtWidgets.QPlainTextEdit.resizeEvent(self, event)

        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QtCore.QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    # def toPlainText(self):
    #     return utils.string(QtWidgets.QPlainTextEdit.toPlainText(self))

    def lineNumberAreaPaintEvent(self, event):

        if self.isReadOnly():
            return

        painter = QtGui.QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), self.lineNumberAreaColor)  # Number bg

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())
        current_line = self.document().findBlock(self.textCursor().position()).blockNumber()

        painter.setPen(self.palette().color(QtGui.QPalette.Text))

        painter_font = config.script_editor_font
        if self.knobScripter != "":
            painter_font.setPointSize(config.prefs["se_font_size"])
        painter.setFont(painter_font)

        while block.isValid() and top <= event.rect().bottom():

            text_color = self.lineNumberColor  # Numbers

            if block_number == current_line and self.hasFocus():
                text_color = self.currentLineNumberColor  # Number highlighted

            painter.setPen(text_color)

            number = "%s" % str(block_number + 1)
            painter.drawText(-3, top, self.lineNumberArea.width(), self.fontMetrics().height(), QtCore.Qt.AlignRight,
                             number)

            # Move to the next block
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def keyPressEvent(self, event):
        """
        Custom actions for specific keystrokes
        """
        key = event.key()
        ctrl = bool(event.modifiers() & Qt.ControlModifier)
        # alt = bool(event.modifiers() & Qt.AltModifier)
        shift = bool(event.modifiers() & Qt.ShiftModifier)
        pre_scroll = self.verticalScrollBar().value()
        # modifiers = QtWidgets.QApplication.keyboardModifiers()
        # ctrl = (modifiers == Qt.ControlModifier)
        # shift = (modifiers == Qt.ShiftModifier)

        up_arrow = 16777235
        down_arrow = 16777237

        # if Tab convert to Space
        if key == 16777217:
            self.indentation('indent')

        # if Shift+Tab remove indent
        elif key == 16777218:
            self.indentation('unindent')

        # if BackSpace try to snap to previous indent level
        elif key == 16777219:
            if not self.unindentBackspace():
                QtWidgets.QPlainTextEdit.keyPressEvent(self, event)
        else:
            # COOL BEHAVIORS SIMILAR TO SUBLIME GO NEXT!
            cursor = self.textCursor()
            cpos = cursor.position()
            apos = cursor.anchor()
            text_before_cursor = self.toPlainText()[:min(cpos, apos)]
            text_after_cursor = self.toPlainText()[max(cpos, apos):]
            text_all = self.toPlainText()
            to_line_start = text_before_cursor[::-1].find("\n")
            if to_line_start == -1:
                linestart_pos = 0  # Position of the start of the line that includes the cursor selection start
            else:
                linestart_pos = len(text_before_cursor) - to_line_start

            to_line_end = text_after_cursor.find("\n")
            if to_line_end == -1:
                lineend_pos = len(text_all)  # Position of the end of the line that includes the cursor selection end
            else:
                lineend_pos = max(cpos, apos) + to_line_end

            text_before_lines = text_all[:linestart_pos]
            text_after_lines = text_all[lineend_pos:]
            if len(text_after_lines) and text_after_lines.startswith("\n"):
                text_after_lines = text_after_lines[1:]
            text_lines = text_all[linestart_pos:lineend_pos]

            if cursor.hasSelection():
                selection = cursor.selection().toPlainText()
            else:
                selection = ""
            if key == Qt.Key_ParenLeft and (len(selection) > 0 or re.match(r"[\s)}\];]+", text_after_cursor) or not len(
                    text_after_cursor)):  # (
                cursor.insertText("(" + selection + ")")
                cursor.setPosition(apos + 1, QtGui.QTextCursor.MoveAnchor)
                cursor.setPosition(cpos + 1, QtGui.QTextCursor.KeepAnchor)
                self.setTextCursor(cursor)
            elif key == Qt.Key_ParenRight and text_after_cursor.startswith(")"):  # )
                cursor.movePosition(QtGui.QTextCursor.NextCharacter)
                self.setTextCursor(cursor)
            elif key in [94, Qt.Key_BracketLeft] \
                    and (len(selection) > 0 or re.match(r"[\s)}\];]+", text_after_cursor)
                         or not len(text_after_cursor)):  # [
                cursor.insertText("[" + selection + "]")
                cursor.setPosition(apos + 1, QtGui.QTextCursor.MoveAnchor)
                cursor.setPosition(cpos + 1, QtGui.QTextCursor.KeepAnchor)
                self.setTextCursor(cursor)
            elif key in [Qt.Key_BracketRight, 43, 93] and text_after_cursor.startswith("]"):  # ]
                cursor.movePosition(QtGui.QTextCursor.NextCharacter)
                self.setTextCursor(cursor)
            elif key == Qt.Key_BraceLeft and (len(selection) > 0 or re.match(r"[\s)}\];]+", text_after_cursor)
                                              or not len(text_after_cursor)):  # {
                cursor.insertText("{" + selection + "}")
                cursor.setPosition(apos + 1, QtGui.QTextCursor.MoveAnchor)
                cursor.setPosition(cpos + 1, QtGui.QTextCursor.KeepAnchor)
                self.setTextCursor(cursor)
            elif key in [199, Qt.Key_BraceRight] and text_after_cursor.startswith("}"):  # }
                cursor.movePosition(QtGui.QTextCursor.NextCharacter)
                self.setTextCursor(cursor)
            elif key == 34:  # "
                if len(selection) > 0:
                    cursor.insertText('"' + selection + '"')
                    cursor.setPosition(apos + 1, QtGui.QTextCursor.MoveAnchor)
                    cursor.setPosition(cpos + 1, QtGui.QTextCursor.KeepAnchor)
                elif text_after_cursor.startswith('"') and '"' in text_before_cursor.split("\n")[-1]:
                    cursor.movePosition(QtGui.QTextCursor.NextCharacter)
                elif not re.match(r"(?:[\s)\]]+|$)", text_after_cursor):  # If chars after cursor, act normal
                    QtWidgets.QPlainTextEdit.keyPressEvent(self, event)
                elif not re.search(r"[\s.({\[,]$",
                                   text_before_cursor) and text_before_cursor != "":  # Chars before cursor: act normal
                    QtWidgets.QPlainTextEdit.keyPressEvent(self, event)
                else:
                    cursor.insertText('"' + selection + '"')
                    cursor.setPosition(apos + 1, QtGui.QTextCursor.MoveAnchor)
                    cursor.setPosition(cpos + 1, QtGui.QTextCursor.KeepAnchor)
                self.setTextCursor(cursor)
            elif key == 39:  # '
                if len(selection) > 0:
                    cursor.insertText("'" + selection + "'")
                    cursor.setPosition(apos + 1, QtGui.QTextCursor.MoveAnchor)
                    cursor.setPosition(cpos + 1, QtGui.QTextCursor.KeepAnchor)
                elif text_after_cursor.startswith("'") and "'" in text_before_cursor.split("\n")[-1]:
                    cursor.movePosition(QtGui.QTextCursor.NextCharacter)
                elif not re.match(r"(?:[\s)\]]+|$)", text_after_cursor):  # If chars after cursor, act normal
                    QtWidgets.QPlainTextEdit.keyPressEvent(self, event)
                elif not re.search(r"[\s.({\[,]$",
                                   text_before_cursor) and text_before_cursor != "":  # Chars before cursor: act normal
                    QtWidgets.QPlainTextEdit.keyPressEvent(self, event)
                else:
                    cursor.insertText("'" + selection + "'")
                    cursor.setPosition(apos + 1, QtGui.QTextCursor.MoveAnchor)
                    cursor.setPosition(cpos + 1, QtGui.QTextCursor.KeepAnchor)
                self.setTextCursor(cursor)
            elif key == 35 and len(selection):  # # (yes, a hash)
                # If there's a selection, insert a hash at the start of each line.. how?
                if selection != "":
                    selection_split = selection.split("\n")
                    if all(i.startswith("#") for i in selection_split):
                        selection_commented = "\n".join([s[1:] for s in selection_split])  # Uncommented
                    else:
                        selection_commented = "#" + "\n#".join(selection_split)
                    cursor.insertText(selection_commented)
                    if apos > cpos:
                        cursor.setPosition(apos + len(selection_commented) - len(selection),
                                           QtGui.QTextCursor.MoveAnchor)
                        cursor.setPosition(cpos, QtGui.QTextCursor.KeepAnchor)
                    else:
                        cursor.setPosition(apos, QtGui.QTextCursor.MoveAnchor)
                        cursor.setPosition(cpos + len(selection_commented) - len(selection),
                                           QtGui.QTextCursor.KeepAnchor)
                    self.setTextCursor(cursor)

            elif key == 68 and ctrl and shift:  # Ctrl+Shift+D, to duplicate text or line/s

                if not len(selection):
                    self.setPlainText(text_before_lines + text_lines + "\n" + text_lines + "\n" + text_after_lines)
                    cursor.setPosition(apos + len(text_lines) + 1, QtGui.QTextCursor.MoveAnchor)
                    cursor.setPosition(cpos + len(text_lines) + 1, QtGui.QTextCursor.KeepAnchor)
                    self.setTextCursor(cursor)
                    self.verticalScrollBar().setValue(pre_scroll)
                    self.scrollToCursor()
                else:
                    if text_before_cursor.endswith("\n") and not selection.startswith("\n"):
                        cursor.insertText(selection + "\n" + selection)
                        cursor.setPosition(apos + len(selection) + 1, QtGui.QTextCursor.MoveAnchor)
                        cursor.setPosition(cpos + len(selection) + 1, QtGui.QTextCursor.KeepAnchor)
                    else:
                        cursor.insertText(selection + selection)
                        cursor.setPosition(apos + len(selection), QtGui.QTextCursor.MoveAnchor)
                        cursor.setPosition(cpos + len(selection), QtGui.QTextCursor.KeepAnchor)
                    self.setTextCursor(cursor)

            elif key == up_arrow and ctrl and shift and len(
                    text_before_lines):  # Ctrl+Shift+Up, to move the selected line/s up
                prev_line_start_distance = text_before_lines[:-1][::-1].find("\n")
                if prev_line_start_distance == -1:
                    prev_line_start_pos = 0  # Position of the start of the previous line
                else:
                    prev_line_start_pos = len(text_before_lines) - 1 - prev_line_start_distance
                prev_line = text_before_lines[prev_line_start_pos:]

                text_before_prev_line = text_before_lines[:prev_line_start_pos]

                if prev_line.endswith("\n"):
                    prev_line = prev_line[:-1]

                if len(text_after_lines):
                    text_after_lines = "\n" + text_after_lines

                self.setPlainText(text_before_prev_line + text_lines + "\n" + prev_line + text_after_lines)
                cursor.setPosition(apos - len(prev_line) - 1, QtGui.QTextCursor.MoveAnchor)
                cursor.setPosition(cpos - len(prev_line) - 1, QtGui.QTextCursor.KeepAnchor)
                self.setTextCursor(cursor)
                self.verticalScrollBar().setValue(pre_scroll)
                self.scrollToCursor()
                return

            elif key == down_arrow and ctrl and shift:  # Ctrl+Shift+Up, to move the selected line/s up
                if not len(text_after_lines):
                    text_after_lines = ""
                next_line_end_distance = text_after_lines.find("\n")
                if next_line_end_distance == -1:
                    next_line_end_pos = len(text_all)
                else:
                    next_line_end_pos = next_line_end_distance
                next_line = text_after_lines[:next_line_end_pos]
                text_after_next_line = text_after_lines[next_line_end_pos:]

                self.setPlainText(text_before_lines + next_line + "\n" + text_lines + text_after_next_line)
                cursor.setPosition(apos + len(next_line) + 1, QtGui.QTextCursor.MoveAnchor)
                cursor.setPosition(cpos + len(next_line) + 1, QtGui.QTextCursor.KeepAnchor)
                self.setTextCursor(cursor)
                self.verticalScrollBar().setValue(pre_scroll)
                self.scrollToCursor()
                return

            elif key == up_arrow and not len(text_before_lines):  # If up key and nothing happens, go to start
                if not shift:
                    cursor.setPosition(0, QtGui.QTextCursor.MoveAnchor)
                    self.setTextCursor(cursor)
                else:
                    cursor.setPosition(0, QtGui.QTextCursor.KeepAnchor)
                    self.setTextCursor(cursor)

            elif key == down_arrow and not len(text_after_lines):  # If up key and nothing happens, go to start
                if not shift:
                    cursor.setPosition(len(text_all), QtGui.QTextCursor.MoveAnchor)
                    self.setTextCursor(cursor)
                else:
                    cursor.setPosition(len(text_all), QtGui.QTextCursor.KeepAnchor)
                    self.setTextCursor(cursor)

            # if enter or return, match indent level
            elif key in [16777220, 16777221]:
                self.indentNewLine()

            # If ctrl + +, increase font size
            elif ctrl and key == Qt.Key_Plus:
                font = self.font()
                font.setPointSize(-(-font.pointSize() // 0.9))
                self.setFont(font)
            # If ctrl + -, decrease font size
            elif ctrl and key == Qt.Key_Minus:
                font = self.font()
                font.setPointSize(font.pointSize() // 1.1)
                self.setFont(font)

            else:
                QtWidgets.QPlainTextEdit.keyPressEvent(self, event)

        self.scrollToCursor()

    def scrollToCursor(self):
        self.cursor = self.textCursor()
        self.cursor.movePosition(
            QtGui.QTextCursor.NoMove)  # Does nothing, but makes the scroll go to the right place...
        self.setTextCursor(self.cursor)

    def getCursorInfo(self):

        self.cursor = self.textCursor()

        self.firstChar = self.cursor.selectionStart()
        self.lastChar = self.cursor.selectionEnd()

        self.noSelection = False
        if self.firstChar == self.lastChar:
            self.noSelection = True

        self.originalPosition = self.cursor.position()
        self.cursorBlockPos = self.cursor.positionInBlock()

    def unindentBackspace(self):
        """
        #snap to previous indent level
        """
        self.getCursorInfo()

        if not self.noSelection or self.cursorBlockPos == 0:
            return False

        # check text in front of cursor
        text_in_front = self.document().findBlock(self.firstChar).text()[:self.cursorBlockPos]

        # check whether solely spaces
        if text_in_front != ' ' * self.cursorBlockPos:
            return False

        # snap to previous indent level
        spaces = len(text_in_front)

        for space in range(int(spaces - int(float(spaces - 1) / self.tab_spaces) * self.tab_spaces - 1)):
            self.cursor.deletePreviousChar()

    def indentNewLine(self):
        # In case selection covers multiple line, make it one line first
        self.insertPlainText('')
        self.getCursorInfo()

        # Check how many spaces after cursor
        text = self.document().findBlock(self.firstChar).text()
        text_in_front = text[:self.cursorBlockPos]

        if len(text_in_front) == 0:
            self.insertPlainText('\n')
            return

        indent_level = 0
        for i in text_in_front:
            if i == ' ':
                indent_level += 1
            else:
                break

        indent_level /= self.tab_spaces

        # find out whether text_in_front's last character was a ':'
        # if that's the case add another indent.
        # ignore any spaces at the end, however also
        # make sure text_in_front is not just an indent
        if text_in_front.count(' ') != len(text_in_front):
            while text_in_front[-1] == ' ':
                text_in_front = text_in_front[:-1]

        if text_in_front[-1] == ':':
            indent_level += 1

        # new line
        self.insertPlainText('\n')
        # match indent
        self.insertPlainText(' ' * int(self.tab_spaces * indent_level))

    def indentation(self, mode):

        pre_scroll = self.verticalScrollBar().value()
        self.getCursorInfo()

        # if nothing is selected and mode is set to indent, simply insert as many
        # space as needed to reach the next indentation level.
        if self.noSelection and mode == 'indent':
            remaining_spaces = self.tab_spaces - (self.cursorBlockPos % self.tab_spaces)
            self.insertPlainText(' ' * remaining_spaces)
            return

        selected_blocks = self.findBlocks(self.firstChar, self.lastChar)
        before_blocks = self.findBlocks(last=self.firstChar - 1, exclude=selected_blocks)
        after_blocks = self.findBlocks(first=self.lastChar + 1, exclude=selected_blocks)

        before_blocks_text = self.blocks2list(before_blocks)
        selected_blocks_text = self.blocks2list(selected_blocks, mode)
        after_blocks_text = self.blocks2list(after_blocks)

        combined_text = '\n'.join(before_blocks_text + selected_blocks_text + after_blocks_text)

        # make sure the line count stays the same
        original_block_count = len(self.toPlainText().split('\n'))
        combined_text = '\n'.join(combined_text.split('\n')[:original_block_count])

        self.clear()
        self.setPlainText(combined_text)

        if self.noSelection:
            self.cursor.setPosition(self.lastChar)

        # check whether the the orignal selection was from top to bottom or vice versa
        else:
            if self.originalPosition == self.firstChar:
                first = self.lastChar
                last = self.firstChar
                first_block_snap = QtGui.QTextCursor.EndOfBlock
                last_block_snap = QtGui.QTextCursor.StartOfBlock
            else:
                first = self.firstChar
                last = self.lastChar
                first_block_snap = QtGui.QTextCursor.StartOfBlock
                last_block_snap = QtGui.QTextCursor.EndOfBlock

            self.cursor.setPosition(first)
            self.cursor.movePosition(first_block_snap, QtGui.QTextCursor.MoveAnchor)
            self.cursor.setPosition(last, QtGui.QTextCursor.KeepAnchor)
            self.cursor.movePosition(last_block_snap, QtGui.QTextCursor.KeepAnchor)

        self.setTextCursor(self.cursor)
        self.verticalScrollBar().setValue(pre_scroll)

    def findBlocks(self, first=0, last=None, exclude=None):
        exclude = exclude or []
        blocks = []
        if last is None:
            last = self.document().characterCount()
        for pos in range(first, last + 1):
            block = self.document().findBlock(pos)
            if block not in blocks and block not in exclude:
                blocks.append(block)
        return blocks

    def blocks2list(self, blocks, mode=None):
        text = []
        for block in blocks:
            block_text = block.text()
            if mode == 'unindent':
                if block_text.startswith(' ' * self.tab_spaces):
                    block_text = block_text[self.tab_spaces:]
                    self.lastChar -= self.tab_spaces
                elif block_text.startswith(' '):
                    block_text = block_text[1:]
                    self.lastChar -= 1

            elif mode == 'indent':
                block_text = ' ' * self.tab_spaces + block_text
                self.lastChar += self.tab_spaces

            text.append(block_text)

        return text

    def highlightCurrentLine(self):
        """
        Highlight currently selected line
        """
        extra_selections = []

        selection = QtWidgets.QTextEdit.ExtraSelection()

        selection.format.setBackground(self.lineColor)
        selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()

        extra_selections.append(selection)

        self.setExtraSelections(extra_selections)
        self.scrollToCursor()

    @staticmethod
    def format(rgb, style=''):
        """
        Return a QtWidgets.QTextCharFormat with the given attributes.
        """
        color = QtGui.QColor(*rgb)
        text_format = QtGui.QTextCharFormat()
        text_format.setForeground(color)

        if 'bold' in style:
            text_format.setFontWeight(QtGui.QFont.Bold)
        if 'italic' in style:
            text_format.setFontItalic(True)
        if 'underline' in style:
            text_format.setUnderlineStyle(QtGui.QTextCharFormat.SingleUnderline)

        return text_format

    def setColorStyle(self, style=None):
        """
        Change bg and text color configurations regarding the editor style. This doesn't change the syntax highlighter
        """
        styles = config.script_editor_styles

        if not style:
            style = config.prefs["se_style"]

        if style not in styles:
            return False

        self.setStyleSheet(styles[style]["stylesheet"])
        self.lineColor = QtGui.QColor(*styles[style]["selected_line_color"])
        self.lineNumberAreaColor = QtGui.QColor(*styles[style]["lineNumberAreaColor"])
        self.lineNumberColor = QtGui.QColor(*styles[style]["lineNumberColor"])
        self.currentLineNumberColor = QtGui.QColor(*styles[style]["currentLineNumberColor"])
        self.highlightCurrentLine()
        self.scrollToCursor()
        return True

    def set_code_language(self, lang="python"):
        """ Sets the appropriate highlighter and styles """

        if lang is None and self.highlighter:
            self.highlighter.setDocument(None)
            self.highlighter = None
            self.code_language = None

        if isinstance(lang, str):
            if lang != self.code_language:
                lang = lang.lower()
                if self.highlighter:
                    self.highlighter.setDocument(None)
                    self.highlighter = None
                if lang == "blink":
                    self.highlighter = blinkhighlighter.KSBlinkHighlighter(self.document())
                    self.highlighter.setStyle(config.prefs["code_style_blink"])
                    self.setColorStyle("blink_default")
                elif lang == "python":
                    self.highlighter = pythonhighlighter.KSPythonHighlighter(self.document())
                    self.highlighter.setStyle(config.prefs["code_style_python"])
                    self.setColorStyle("default")
                else:
                    self.setColorStyle("default")
                    self.code_language = None
                    return
            self.code_language = lang
        else:
            logging.debug("Lang type not valid: " + str(type(lang)))


class KSLineNumberArea(QtWidgets.QWidget):
    def __init__(self, script_editor):
        super(KSLineNumberArea, self).__init__(script_editor)

        self.scriptEditor = script_editor
        self.setStyleSheet("text-align: center;")

    def paintEvent(self, event):
        self.scriptEditor.lineNumberAreaPaintEvent(event)
        return

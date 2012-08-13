#!/usr/bin/python2 -B
# -*- coding: utf-8 -*-
#
# Webcamod, webcam capture plasmoid.
# Copyright (C) 2011-2012  Gonzalo Exequiel Pedone
#
# Webcamod is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Webcamod is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Webcamod. If not, see <http://www.gnu.org/licenses/>.
#
# Email     : hipersayan DOT x AT gmail DOT com
# Web-Site 1: http://github.com/hipersayanX/Webcamoid
# Web-Site 2: http://kde-apps.org/content/show.php/Webcamoid?content=144796

import os
import sys

from PyQt4 import uic, QtGui, QtCore
from PyKDE4 import kdeui, plasmascript


class Effects(QtGui.QWidget):
    def __init__(self, parent=None, tools=None):
        QtGui.QWidget.__init__(self)

        if isinstance(parent, plasmascript.Applet):
            uic.loadUi(parent.package().filePath('ui', 'effects.ui'), self)
        else:
            uic.loadUi(self.resolvePath('../ui/effects.ui'), self)

        self.btnUp.setIcon(kdeui.KIcon('arrow-up'))
        self.btnAdd.setIcon(kdeui.KIcon('arrow-right'))
        self.btnDown.setIcon(kdeui.KIcon('arrow-down'))
        self.btnRemove.setIcon(kdeui.KIcon('arrow-left'))
        self.btnReset.setIcon(kdeui.KIcon('edit-undo'))

        self.tools = tools

        if not self.tools:
            return

        for effect in self.tools.currentEffects():
            items = self.lswEffects.findItems(effect, QtCore.Qt.MatchExactly)

            if len(items) > 0:
                self.lswApply.addItem(self.lswEffects.\
                                        takeItem(self.lswEffects.row(items[0])))

        self.tools.recordingStateChanged.connect(self.recordingStateChanged)
        self.recordingStateChanged(self.tools.isRecording())

    def resolvePath(self, relpath=''):
        return os.path.normpath(os.path.join(os.path.\
                                dirname(os.path.realpath(__file__)), relpath))

    @QtCore.pyqtSlot(bool)
    def recordingStateChanged(self, recording):
        self.lswEffects.setEnabled(not recording)
        self.lswApply.setEnabled(not recording)

    @QtCore.pyqtSlot()
    def on_btnAdd_clicked(self):
        for item in self.lswEffects.selectedItems():
            self.lswApply.addItem(self.lswEffects.\
                                            takeItem(self.lswEffects.row(item)))

        self.update()

    @QtCore.pyqtSlot()
    def on_btnRemove_clicked(self):
        for item in self.lswApply.selectedItems():
            self.lswEffects.addItem(self.lswApply.\
                                            takeItem(self.lswApply.row(item)))

        self.lswEffects.sortItems()
        self.update()

    @QtCore.pyqtSlot()
    def on_btnUp_clicked(self):
        for item in self.lswApply.selectedItems():
            row = self.lswApply.row(item)
            row_ = row - 1 if row >= 1 else 0
            item_ = self.lswApply.takeItem(row)
            self.lswApply.insertItem(row_, item_)
            item_.setSelected(True)

        self.update()

    @QtCore.pyqtSlot()
    def on_btnDown_clicked(self):
        for item in self.lswApply.selectedItems():
            row = self.lswApply.row(item)
            row_ = row + 1 if row < self.lswApply.count() - 1 \
                                                else self.lswApply.count() - 1
            item_ = self.lswApply.takeItem(row)
            self.lswApply.insertItem(row_, item_)
            item_.setSelected(True)

        self.update()

    @QtCore.pyqtSlot()
    def on_btnReset_clicked(self):
        while self.lswApply.count() > 0:
            self.lswEffects.addItem(self.lswApply.takeItem(0))

        self.lswEffects.sortItems()
        self.update()

    def update(self):
        if not self.tools:
            return

        effects = []

        for i in range(self.lswApply.count()):
            effects.append(self.lswApply.item(i).text())

        self.tools.setEffects(effects)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    effects = Effects()
    effects.show()
    app.exec_()

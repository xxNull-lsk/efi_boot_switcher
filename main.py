import os
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QPushButton, QHBoxLayout, \
    QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QMessageBox

from bootmgr import Bootmgr


class MyWindow(QWidget):
    bootmgr = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.boot_items = QListWidget()
        self.btn_up = QPushButton("↑")
        self.btn_up.clicked.connect(lambda: self.on_changed_index(1))
        self.btn_down = QPushButton("↓")
        self.btn_down.clicked.connect(lambda: self.on_changed_index(-1))
        self.btn_add = QPushButton("+")
        self.btn_remove = QPushButton("-")
        self.btn_remove.clicked.connect(self.on_remove)
        self.btn_backup = QPushButton("备份")
        self.btn_restore = QPushButton("恢复")
        self.btn_refresh = QPushButton("Reset")
        self.btn_refresh.clicked.connect(self.init_data)
        self.btn_save = QPushButton("保存修改")
        self.btn_save.clicked.connect(self.on_save)
        self.btn_reboot = QPushButton("重启进入")
        self.btn_reboot.clicked.connect(self.on_reboot)

        self.setMinimumWidth(480)
        self.setMinimumHeight(360)
        self.init_ui()
        self.init_data()

    def init_data(self):
        self.bootmgr = Bootmgr()
        self.boot_items.clear()
        for index in self.bootmgr.get_boot_orders():
            item = self.bootmgr.get_boot_item(index)
            list_item = QListWidgetItem(item['name'])
            list_item.setData(QtCore.Qt.UserRole, index)
            self.boot_items.addItem(list_item)

    def init_ui(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(8)
        vbox.addWidget(self.btn_up)
        vbox.addWidget(self.btn_down)
        # vbox.addWidget(self.btn_add)
        vbox.addWidget(self.btn_remove)
        # vbox.addWidget(self.btn_backup)
        # vbox.addWidget(self.btn_restore)
        vbox.addWidget(self.btn_refresh)
        vbox.addStretch(1)

        hbox1 = QHBoxLayout()
        hbox1.setSpacing(8)
        hbox1.addWidget(self.boot_items)
        hbox1.addItem(vbox)

        hbox3 = QHBoxLayout()
        hbox3.setSpacing(8)
        hbox3.addWidget(self.btn_save)
        hbox3.addWidget(self.btn_reboot)

        vbox_root = QVBoxLayout()
        vbox_root.setSpacing(8)
        vbox_root.addItem(hbox1)
        vbox_root.addItem(hbox3)

        self.setLayout(vbox_root)

    def on_reboot(self):
        item = self.boot_items.currentItem()
        if item is None:
            QMessageBox.critical(self, "错误", "请先选择引导项")
            return
        ret = QMessageBox.warning(self, "提示", "确认要立即重启进入“{}” 吗？".format(item.text()),
                                  QMessageBox.Yes | QMessageBox.No)
        if ret != QMessageBox.Yes:
            return
        boot_index = item.data(QtCore.Qt.UserRole)
        err = self.bootmgr.set_next_boot(boot_index)
        if err != 0:
            QMessageBox.critical(self, "错误", "设置失败, 错误号：{}".format(err))
            return
        os.system('reboot')

    def on_save(self):
        orders = []
        for index in range(0, self.boot_items.count()):
            boot_index = self.boot_items.item(index).data(QtCore.Qt.UserRole)
            orders.append(boot_index)
        err = self.bootmgr.set_boot_orders(orders)
        if err != 0:
            QMessageBox.critical(self, "错误", "设置失败, 错误号：{}".format(err))
            return
        self.init_data()

    def on_remove(self):
        item = self.boot_items.currentItem()
        if item is None:
            QMessageBox.critical(self, "错误", "请先选择引导项")
            return
        ret = QMessageBox.warning(self, "提示", "确认要立即删除“{}” 吗？".format(item.text()),
                                  QMessageBox.Yes | QMessageBox.No)
        if ret != QMessageBox.Yes:
            return

        boot_index = item.data(QtCore.Qt.UserRole)
        err = self.bootmgr.delete_item(boot_index)
        if err != 0:
            QMessageBox.critical(self, "错误", "设置失败, 错误号：{}".format(err))
            return
        self.init_data()

    def on_changed_index(self, inc):
        index = self.boot_items.currentIndex().row()
        item = self.boot_items.takeItem(index)
        self.boot_items.insertItem(index - inc, item)
        self.boot_items.setCurrentItem(item)


def main():
    app = QApplication(sys.argv)
    main_window = MyWindow()
    rect = app.screenAt(main_window.pos()).geometry()
    main_window.move(
        (rect.width() - main_window.width()) / 2,
        (rect.height() - main_window.height()) / 2
    )
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

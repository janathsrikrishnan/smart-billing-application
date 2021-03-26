# imported the required the packages

####### Notes ########
""" color can be changed for individually """



# unfinished work
# 1. self.Print
# 2. self.Close
# 3. self.Font
# 4. self.Save
# 5. Icons need to to be set
# 6. color action unfinished
# 7. want to add clear button for all entry
# 8. analysis tab is not added in tab menu
# 9. need to put password for enter in items and bill book
# 10. password can be enable

import sys, webbrowser

from PyQt5.QtWidgets import (QApplication, QWidget, QFormLayout, QVBoxLayout, QSpinBox,
                             QHBoxLayout, QAction, QPushButton, QTabWidget,
                             QGroupBox, QLineEdit, QTextEdit, QMessageBox,
                             QMainWindow, QTableView, QFontDialog, QColorDialog,
                             QLabel, QSizePolicy, QHeaderView, QGridLayout, QComboBox)

from PyQt5.QtSql import (QSqlQuery, QSqlDatabase, QSqlRelationalDelegate,
                         QSqlRelationalTableModel, QSqlRelation, QSqlTableModel)

from PyQt5.QtGui import QFont, QIcon, QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt, QSize

class bill(QMainWindow, QWidget):
    def __init__(self):

        super().__init__()
        self.initialize()



    def initialize(self):
        # set geometry, window title
        self.setMinimumSize(1350, 600)
        self.setWindowTitle("Smart Billing")
        self.Connection()
        self.createTable()

        # show menu bar
        self.MenuBar()
        self.Tab()
        self.show()

    def Connection(self):
        """ create the connection to the sqlite3 and open the database"""

        # setup the connection to sqlite3 and open the billing database
        # if database not present create one
        database = QSqlDatabase.addDatabase("QSQLITE")
        database.setDatabaseName("billing.db")

        if not database.open():
            print("Unable to connect")
            sys.exit(1) # fail to connect to the database

        # tables needed for billing application
        table_need = {'items', 'billBook'}

        # table that are not found
        table_not_found = table_need - set(database.tables())

        # if tables are not found it give a critical message and exits
        if table_not_found:
            QMessageBox.critical(None, "Error", f'Following database tables are not found:{table_not_found}')
            sys.exit(1)

    def MenuBar(self):
        """ this create the main menu"""

        # create print action
        print_act = QAction("print", self)
        print_act.setShortcut("Ctrl+P")
        print_act.setIcon(QIcon("icons/018-printer.png"))
        print_act.setEnabled(False)
        print_act.triggered.connect(self.Print)


        # create exit action
        exit_act = QAction("exit", self)
        exit_act.setShortcut("Ctrl+Q")
        exit_act.setIcon(QIcon("icons/008-logout.png"))
        exit_act.triggered.connect(self.closeEvent)

        # create save action
        save_act = QAction("save", self)
        save_act.setShortcut("Ctrl+S")
        save_act.setIcon(QIcon("icons/004-folder.png"))
        save_act.triggered.connect(self.Save)


        # create search_bill_act action
        search_bill_act = QAction("Search Bill", self)
        search_bill_act.setShortcut("Ctrl+F")
        search_bill_act.setIcon(QIcon("icons/015-magnifier.png"))
        search_bill_act.triggered.connect(self.Find_Bill)

        # create insert item action and set the current tab index to 1 because Items index is 1
        insert_act = QAction("Insert item", self)
        insert_act.setShortcut("Ctrl+I")
        insert_act.setIcon(QIcon("icons/007-download.png"))
        insert_act.triggered.connect(self.Change_to_item)

        # create bill book action and set the current tab index to 2 because bill book index is 2
        billBook_act = QAction("Bill Book", self)
        billBook_act.setShortcut("Ctrl+B")
        billBook_act.setIcon(QIcon("icons/open-book.png"))
        billBook_act.triggered.connect(self.Change_to_billBook)



    # create color_act action
        color_act = QAction("color", self)
        color_act.setShortcut("Ctrl+Shift+C")
        color_act.setIcon(QIcon("icons/001-painter-palette.png"))
        color_act.triggered.connect(self.Color)

        # create font action
        font_act = QAction("font", self)
        font_act.setShortcut("Ctrl+Shift+F")
        font_act.setIcon(QIcon("icons/006-font.png"))
        font_act.triggered.connect(self.Font)

    # create help menu
        # create About action
        about_act = QAction("About", self)
        about_act.setIcon(QIcon("icons/023-information-button.png"))
        about_act.triggered.connect(self.About)
        # feedback action
        feedback_act = QAction("Feedback", self)
        feedback_act.setIcon(QIcon("icons/022-feedback.png"))
        feedback_act.triggered.connect(self.FeedBack)

    # create main menu and add sub menu and action
        # create menu
        menu = self.menuBar()
        menu.setNativeMenuBar(False)
        # create file menu
        file = menu.addMenu("File")
        file.addAction(print_act)
        file.addAction(save_act)
        file.addAction(exit_act)

    # create tools menu
        tools = menu.addMenu("Tools")
        # insert search bill action
        tools.addAction(search_bill_act)

        # insert insert item
        tools.addAction(insert_act)

        # insert bill book action
        tools.addAction(billBook_act)

    # create format
        Format = menu.addMenu("Format")

        # add font to format menu
        Format.addAction(font_act)
        Format.addAction(color_act)

    # create help menu
        help_menu = menu.addMenu("help")
        # add about_act to help
        help_menu.addAction(about_act)
        help_menu.addAction(feedback_act)



    def Tab(self):
        """ create the tab for bill, insert, analysis"""
        # create the tab
        self.tab = QTabWidget(self)

        # create the tab object bill, insert_item, analysis
        self.bill_tab = QWidget()
        self.insert_tab = QWidget()
        self.billBook_tab = QWidget()

        # add the tab objects to tab
        self.tab.addTab(self.bill_tab, "Bill")
        self.tab.addTab(self.insert_tab, "Items")
        self.tab.addTab(self.billBook_tab, "Bill Book")

        # call the the tabs
        self.billwidget()
        self.insertwidget()
        self.billBook()

        # create the main
        self.main_layout = QWidget()
        self.setCentralWidget(self.main_layout)

        self.tab_layout = QHBoxLayout()
        self.tab_layout.addWidget(self.tab)

        self.main_layout.setLayout(self.tab_layout)

    def billwidget(self):

    # buyer information
        # buyers name
        self.buyer_name = QLineEdit()
        self.buyer_name.resize(100, 100)
        self.buyer_name.setPlaceholderText("Janath Jsk")
        # customizing the line edit
        self.buyer_name.setStyleSheet("color: rgb(120, 60, 5)")
        # buyer_name clear button
        buyer_name_clear = QPushButton()
        buyer_name_clear.setIcon(QIcon("icons/005-cancel.png"))
        buyer_name_clear.setIconSize(QSize(19, 19))
        buyer_name_clear.clicked.connect(self.buyer_name.clear)



        # buyers mobile number
        self.buyer_mobile = QLineEdit()
        self.buyer_mobile.resize(100, 100)
        self.buyer_mobile.setInputMask("000-000-0000")

        # buyer mobile clear
        buyer_mobile_clear = QPushButton()
        buyer_mobile_clear.setIcon(QIcon("icons/005-cancel.png"))
        buyer_mobile_clear.setIconSize(QSize(19, 19))
        buyer_mobile_clear.clicked.connect(self.buyer_mobile.clear)
        buyer_mobile_clear.setObjectName("clear")

        # buyers address
        self.buyers_address = QTextEdit()

        # buyer address clear
        address_clear_bt = QPushButton()
        address_clear_bt.setIcon(QIcon("icons/005-cancel.png"))
        address_clear_bt.setIconSize(QSize(19, 19))
        address_clear_bt.clicked.connect(self.buyers_address.clear)

        # create main layout and set as central widget
        bill_layout = QVBoxLayout()

        # create layout and add to main layout
        form_layout = QFormLayout()
        form_layout.setSpacing(0)


        # horizontal layout for buyer name and clear
        name_h_layout = QHBoxLayout()
        name_h_layout.addWidget(self.buyer_name)
        name_h_layout.addWidget(buyer_name_clear)
        # add name horizontal to form layout
        form_layout.addRow("Name", name_h_layout)

        # create horizontal layout for mobile number and clear button
        mobile_h_layout = QHBoxLayout()
        mobile_h_layout.addWidget(self.buyer_mobile)
        mobile_h_layout.addWidget(buyer_mobile_clear)
        # add mobile horizontal layout in form layout
        form_layout.addRow("Mobile Number", mobile_h_layout)

        # add address and clear button
        address_layout = QHBoxLayout()
        address_layout.addWidget(self.buyers_address)
        address_layout.addWidget(address_clear_bt)

        # add address and address clear button to form layout
        form_layout.addRow("Address", address_layout)

        # create buyer information box
        buyer_information_gp = QGroupBox("Buyer Information")
        # set the form layout as buyer information layout
        buyer_information_gp.setLayout(form_layout)

        # add buyer information box to bill_layout
        bill_layout.addWidget(buyer_information_gp)
        bill_layout.addStretch()

    # create the combo box for selecting the item from the sqlite3 table items
        # create item_dict and store the quantity and price in item_dict
        self.items_dict = {}

        # create the item query for getting data from items table
        items_query = QSqlQuery()
        items_query.exec_("SELECT name, quantity, price FROM items")
        # store the selected data in items_dict
        while items_query.next():
            self.items_dict[items_query.value(0)] = (items_query.value(1), items_query.value(2))

        # create item list and store the items_dict keys
        items_list = list(self.items_dict.keys())
        # create the combo for selecting the item and when index was changed connect to Quantity to enable the quantity
        # box and set the range
        self.items_combo = QComboBox()
        self.items_combo.addItems(items_list)
        self.items_combo.currentIndexChanged.connect(self.Quantity)


        # create the spin box to enter the quatity
        self.item_quantity = QSpinBox()
        self.item_quantity.setEnabled(False)

        # create the form layout item and quantity information
        item_form = QFormLayout()
        item_form.addRow("Item Name: ", self.items_combo)
        item_form.addRow("Quantity: ", self.item_quantity)

        # create the add push button to add the item in bill
        add_bt = QPushButton("Add to Bill")
        add_bt.clicked.connect(self.AddToBill)

        # create horizontal layout for button
        bt_h_l = QHBoxLayout()
        bt_h_l.addStretch()
        bt_h_l.addWidget(add_bt)
        bt_h_l.addStretch()

        # create the vertical layout for item information box
        item_v_l = QVBoxLayout()
        item_v_l.addLayout(item_form)
        item_v_l.addLayout(bt_h_l)

        # create the group box for item information
        items_inf = QGroupBox("Add items")
        items_inf.setLayout(item_v_l)


        # add item information group to bill_layout
        bill_layout.addWidget(items_inf)


        # items buyed
        self.bill_model = QStandardItemModel()
        self.bill_table = QTableView()
        self.bill_table.SelectionMode(3)
        self.bill_table.setModel(self.bill_model)

        # set the column count for bill_model
        self.bill_model.setColumnCount(4)

        # strech the column of bill_table
        self.bill_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # set the horizontal header labels
        header = ["ITEMS", "QUANTITY", "PRICE", "TOTAL"]
        self.bill_model.setHorizontalHeaderLabels(header)

        # create grid layout
        bill1_layout = QGridLayout()
        bill1_layout.addLayout(bill_layout, 0, 0)
        bill1_layout.addWidget(self.bill_table, 0, 1)
        # set bill_tab layout as bill_layout

        self.bill_tab.setLayout(bill1_layout)

    def Quantity(self, text):
        """ after enter the item it first set the range of quantity box and set enable"""
        self.item_quantity.setRange(1, self.items_dict[text][0])
        self.item_quantity.setEnabled(True)


    def AddToBill(self):
        pass

    def createTable(self):

    # create the sql item table model
        # create item model
        self.itemTable = QSqlRelationalTableModel()
        # set items table as table for item table mode
        self.itemTable.setTable('items')

        # set header names
        self.itemTable.setHeaderData(self.itemTable.fieldIndex('id'), Qt.Horizontal, "ITEM ID")
        self.itemTable.setHeaderData(self.itemTable.fieldIndex('name'), Qt.Horizontal, "ITEM NAME")
        self.itemTable.setHeaderData(self.itemTable.fieldIndex('quantity'), Qt.Horizontal, "STOCK")
        self.itemTable.setHeaderData(self.itemTable.fieldIndex('price'), Qt.Horizontal, "PRICE")

        self.itemTable.select()

        # create bill book model
        self.billBookTable = QSqlRelationalTableModel()
        # set billbook table as table for bill book model
        self.billBookTable.setTable('billBook')

        # set the header name
        self.billBookTable.setHeaderData(self.billBookTable.fieldIndex('id'), Qt.Horizontal, 'BILL NO')
        self.billBookTable.setHeaderData(self.billBookTable.fieldIndex('name'), Qt.Horizontal, "NAME")
        self.billBookTable.setHeaderData(self.billBookTable.fieldIndex('number'), Qt.Horizontal, "MOBILE NO")
        self.billBookTable.setHeaderData(self.billBookTable.fieldIndex('items'), Qt.Horizontal, "ITEMS")
        self.billBookTable.setHeaderData(self.billBookTable.fieldIndex('amount'), Qt.Horizontal, "AMOUNT")

        self.billBookTable.select()

    def insertwidget(self):
        """ create table """
        # table view and create sql model and set sql mode has table view mode
        title = QLabel("Items")
        title.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        title.setStyleSheet("font: bold 24px")

        self.items_view = QTableView()
        self.items_view.setModel(self.itemTable)

        self.items_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        # set the selection mode and behavior for item_view
        self.items_view.setSelectionMode(QTableView.SingleSelection)
        self.items_view.setSelectionBehavior(QTableView.SelectRows)

        # create delegate for item_view
        delegate = QSqlRelationalDelegate(self.items_view)
        self.items_view.setItemDelegate(delegate)

    # push button
        # add row button
        additem_button = QPushButton("Add item")
        additem_button.setIcon(QIcon("icons/007-download.png"))
        additem_button.setIconSize(QSize(10, 10))
        additem_button.clicked.connect(self.additem)

        # delete row push button
        deleteitem_bt = QPushButton("delete item")
        deleteitem_bt.setIcon(QIcon("icons/005-cancel.png"))
        deleteitem_bt.setIconSize(QSize(10, 10))

        deleteitem_bt.clicked.connect(self.deleteitem)

        # create vertical layout for push button
        push_layout = QHBoxLayout()
        push_layout.addWidget(additem_button)
        push_layout.addStretch()
        push_layout.addWidget(deleteitem_bt)


        # create horizontal layout for table and push button
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(title, Qt.AlignCenter)
        push_w = QWidget()
        push_w.setLayout(push_layout)
        tab_layout.addWidget(push_w)
        tab_layout.addWidget(self.items_view)
        # set tab layout as tab widget layout
        self.insert_tab.setLayout(tab_layout)


    def billBook(self):
        """ show the bills """
        title = QLabel("Bill Book")
        title.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        title.setStyleSheet("font: bold 24px")
        self.Book_view = QTableView()
        self.Book_view.setModel(self.billBookTable)

        # strech the horizontal header only
        self.Book_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # set selection behavior to select the entire row
        self.Book_view.setSelectionBehavior(QTableView.SelectRows)


        bill_V_l = QVBoxLayout()
        bill_V_l.addWidget(title)
        bill_V_l.addWidget(self.Book_view)

        self.billBook_tab.setLayout(bill_V_l)

    def Change_to_billBook(self):
        self.tab.setCurrentIndex(2)


    def Print(self):
        pass

    def closeEvent(self, event):
        """ exit the application"""
        quit_msg = QMessageBox.question(self, "Quit", "You are sure to exit?",
                                        QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.Yes)
        if quit_msg == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def Font(self):
        """ open the font dialog box and user able to select font """
        font, ok = QFontDialog.getFont()
        if ok:
            self.setFont(font)


    def Save(self):
        pass

    def Find_Bill(self):
        pass

    def Change_to_item(self):
        """ change to items tab"""
        self.tab.setCurrentIndex(1)

    def Color(self):
        pass

    def About(self):
        QMessageBox.about(self, "About", "Smart Billing created by Janath Jsk")

    def additem(self):
        print(1)
        last = self.itemTable.rowCount()
        print(last)
        print(2)
        self.itemTable.insertRow(last)

        print(3)
        id = 0
        query = QSqlQuery()
        query.exec_("SELECT MAX (id) FROM items")
        print(4)
        if query.next():
            id = int(query.value(0))
        print(5)

    def deleteitem(self):
        current = self.items_view.selectedIndexes()
        for index in current:
            self.itemTable.removeRow(index.row())
        self.itemTable.select()

    def FeedBack(self):
        url = "https://ut4vq9uuz4l.typeform.com/to/SjBbjdId"
        webbrowser.open_new_tab(url)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = bill()
    sys.exit(app.exec_())


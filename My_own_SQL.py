# -*- coding: utf-8 -*-
# from curses.ascii import NUL
# from sqlite3 import connect
from pickle import FALSE
# import select
import psycopg2
from PyQt5 import QtSql, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5.QtSql import QSqlTableModel

from main_window import Ui_MainWindow
from insert_dialog_window import Ui_add_second_name as Insert_window
from fam_dialog_window import Ui_Dialog as parent_window
from update_dialog_window import Ui_Dialog as Update_window
import sys

DB_HOST = "127.0.0.1"
DB_NAME = "pl_first"
DB_USER = "postgres"
DB_PASS = "2005"


def command(cmd): #Функция, которая выполняет SQL-запрос, и возвращает строки из таблицы
    connection = psycopg2.connect(host = DB_HOST,
                                 user = DB_USER,
                                 password = DB_PASS,
                                 database = DB_NAME)
    cursor = connection.cursor()
    cursor.execute(cmd)
    try:
        rows = cursor.fetchall()
    except:
        connection.commit()
        connection.close()
        cursor.close()
        return True
    connection.commit()
    connection.close()
    cursor.close()
    return rows if rows else []

def parent_table(table, value, operation, item = None, item_2 = None): #Функция выполняющая запросы для родительских таблиц
    result = ""
    match operation:
        case 'INSERT':
            result = f"INSERT INTO {table} ({value}) VALUES ('{item_2}')"
        case 'DELETE':
            result = f"DELETE FROM {table} WHERE {value} = '{item}'"
        case 'UPDATE':
            result = f"UPDATE {table} SET {value} = '{item_2}' WHERE {value} = '{item}'"
        case 'SELECT':
            if item != None:
                result = f"SELECT {value} FROM {table} WHERE {value} = '{item}'"
            else:
                result = f"SELECT {value} FROM {table}"
    if (result != ""):
        try:
            return(command(result))
        except:
            return (f"Error, [{table}] or [{value}] do not exist - probably")

#Функция выполняющая запросы для таблицы main
def main(operation,
        fam = "Not stated",
        name = "Not stated", 
        second_name = "Not stated", 
        street = "Not stated", 
        bldng = "Not stated", 
        bldng_k = "Not stated", 
        appr = "Not stated", 
        telef = "Not stated",
        new_values = dict()): #new_values передаём только для операции UPDATE; ма

    usable = [fam, name, second_name, street, bldng, bldng_k, appr, telef]
    columns = ['fam', 'names', 'second_name', 'street', 'bldng', 'bldng_k', 'appr', 'telef']
    integer = ['fam', 'names', 'second_name', 'street', 'appr']
    result = ""
    #kyes = [i for i in [0, 1, 2, 3] if usable[i] != "Not stated" and usable[i] != ""]
    kyes = []
    match operation:
        case 'INSERT':
            usable = ['NULL' if i == "Not stated" or i == "" else i for i in usable]
            for i in range(len(columns)):
                if columns[i] in integer:
                    kyes.append(i)
            for i in range(len(usable)):
                if i not in kyes:
                    usable[i] = f"'{usable[i]}'"
            usable = ', '.join(usable)
            columns = ', '.join(columns)
            result = f"""INSERT INTO main ({columns})
                        VALUES ({usable})"""
        case 'UPDATE': #Правь эту функцию
            #print(new_values)
            columns = [columns[i] for i in range(len(usable)) if usable[i] != 'Not stated' and usable[i] != ""] #Выбираем столбцы, значение которых будет обновляться 
            #print(columns)
            usable = [i for i in usable if i != 'Not stated' and i != ""]
            #print(usable)
            for i in range(len(columns)):
                if columns[i] in integer:
                    kyes.append(i)
            for i in range(len(usable)):
                if i not in kyes:
                    usable[i] = f"'{usable[i]}'"
            statement = [] #Выражение, которое будет стоять после WHERE
            for i in range(len(usable)):
                if usable[i] != 'NULL' and usable[i] != "Not stated":
                    statement.append(f"{columns[i]} = {usable[i]}")
                else:
                    statement.append(f"{columns[i]} IS NULL")
            statement = ' AND '.join(statement)
            values = [] #Выражение, которое будет стоять до WHERE
            for i in new_values.keys():
                if not(new_values[i] == "" or new_values[i] == "Not stated"):
                    #print(f"{i} >>> {new_values[i]}")
                    if i in ["fam", "names", "second_name", "street", "appr"]:
                        values.append(f"{i} = {new_values[i]}")
                    else:
                        values.append(f"{i} = '{new_values[i]}'")
            values = ', '.join(values)
            #print(values)
            result = f"UPDATE main SET {values} WHERE {statement}"
        case 'DELETE':
            columns = [columns[i] for i in range(len(usable)) if usable[i] != 'Not stated' and usable[i] != ""] #Выбираем столбцы, по которым будет удаление
            usable = [i for i in usable if i != 'Not stated' and i != ""]
            for i in range(len(columns)):
                if columns[i] in integer:
                    kyes.append(i)
            statement = []
            for i in range(len(usable)):
                if i not in kyes:
                    statement.append(f"{columns[i]} = '{usable[i]}'")
                else:
                    if usable[i] in ['Null', 'None', 'null']:
                        statement.append(f"{columns[i]} IS {usable[i]}")
                    else:
                        statement.append(f"{columns[i]} = {usable[i]}")
            statement = ' AND '.join(statement)
            result = f"DELETE FROM main WHERE {statement}"
        case 'SELECT': #Она же функция фильтрации
            columns = [columns[i] for i in range(len(usable)) if usable[i] != 'Not stated' and usable[i] != ""] #Выбираем столбцы для выборки
            usable = [i for i in usable if i != 'Not stated' and i != ""]
            
            for i in range(len(columns)):
                if columns[i] in integer:
                    kyes.append(i)
            statement = []
            for i in range(len(usable)):
                if i not in kyes:
                    statement.append(f"{columns[i]} = '{usable[i]}'")
                else:
                    statement.append(f"{columns[i]} = {usable[i]}")
            statement = ' AND '.join(statement)
            result = """ 
            SELECT  main.u_id,
		            fam.f_value,
		            names.n_value,
		            second_name.sn_value,
		            street.s_value,
		            bldng,
		            bldng_k,
		            appr,
		            telef
            FROM main 
            JOIN fam ON main.fam = fam.f_id
            JOIN names ON main.names = names.n_id
            JOIN second_name ON main.second_name = second_name.sn_id
            JOIN street ON main.street = street.s_id """
            statement = 'WHERE ' + statement
            if (len(statement) > 6):
                result += statement

    #print (result)
    #result = ""
    if (result != ""):
        try:
            return(command(result))
        except:
            print(result, "here we are")
            return ("Something went wrong")
    else:
        return ("void statement") 


def get_table(item = ['' for i in range(8)]):
    table = []
    query = ["SELECT"] + item
    table = main(query[0], query[1], query[2], query[3], query[4], query[5], query[6], query[7], query[8])
    # for i in table:
    #     print(i)
    output_table = []
    for i in range(len(table)):
        element = []
        for j in range(len(table[i])):
            if isinstance(table[i][j],str):
                element.append(table[i][j].strip())
            else:
                element.append(table[i][j])
        output_table.append(element)
    # for i in output_table:
    #     print(i)
    return output_table



def get_combo(cmd):
    rows = command(cmd)
    rows = [row[0].strip() for row in rows]
    return rows

#print(['Not stated'] + get_combo("SELECT f_value FROM fam"))

class main_window(QMainWindow):
    def __init__(self):
        super(main_window, self).__init__()
        self.ui = Ui_MainWindow()
        self.clicked_row = False
        self.ui.setupUi(self)
        self.table_buffer_queary = ['' for i in range(8)]
        self.table_buffer = get_table()
        self.ui.default_button.clicked.connect(self.default_table)
        self.ui.pushButton.clicked.connect(self.open_dialog_window)
        
        self.ui.pushButton_3.clicked.connect(self.open_dialog_window)
        self.ui.pushButton_2.clicked.connect(self.open_update_window)
        self.ui.pushButton_4.clicked.connect(self.open_dialog_window)
        self.ui.tableWidget.cellClicked.connect(self.action_cell)
        self.show_data_base()

    def action_cell(self):
        row = self.ui.tableWidget.currentRow()
        #column = self.ui.tableWidget.currentColumn()
        #cell_text = self.ui.tableWidget.item(row, column).text()
        #print(row, column)
        #print(cell_text)
        self.clicked_row = []
        for column in range(8):
            cell_text = self.ui.tableWidget.item(row, column).text()
            self.clicked_row.append(cell_text)
        print(self.clicked_row)

    def delete_clicked_row(self):
        fam = command(f" SELECT f_id FROM fam WHERE f_value = '{self.clicked_row[0]}'")[0][0]
        name = command(f" SELECT n_id FROM names WHERE n_value = '{self.clicked_row[1]}'")[0][0]
        second_name = command(f" SELECT sn_id FROM second_name WHERE sn_value = '{self.clicked_row[2]}'")[0][0]
        street = command(f" SELECT s_id FROM street WHERE s_value = '{self.clicked_row[3]}'")[0][0]
        print(fam, name, second_name, street)
        query = f"""DELETE FROM main 
                    WHERE fam = {fam} AND
                    names = {name} AND
                    second_name = {second_name} AND
                    street = {street} AND
                    bldng = '{self.clicked_row[4]}' AND
                    bldng_k = '{self.clicked_row[5]}' AND
                    appr = {self.clicked_row[6]} AND
                    telef = '{self.clicked_row[7]}'"""
        command(query)
        self.clicked_row = False
        self.table_buffer = get_table(self.table_buffer_queary)
        self.show_data_base()


    def open_dialog_window(self):
        self.operation_buf = self.sender()
        if self.operation_buf.text() == 'DELETE' and self.clicked_row:
            self.delete_clicked_row()
            return 0
        self.new_window = QtWidgets.QDialog()
        self.second_window = Insert_window()
        
        self.second_window.setupUi(self.new_window)

        self.second_window.fam_comboBox.addItems(["Not stated"] + get_combo("SELECT f_value FROM fam"))
        self.second_window.name_comboBox.addItems(["Not stated"] + get_combo("SELECT n_value FROM names"))
        self.second_window.second_name_comboBox.addItems(["Not stated"] + get_combo("SELECT sn_value FROM second_name"))
        self.second_window.street_comboBox.addItems(["Not stated"] + get_combo("SELECT s_value FROM street"))
        self.second_window.add_fam.clicked.connect(self.open_fam_window)
        self.second_window.add_name.clicked.connect(self.open_name_window)
        self.second_window.add_second_street.clicked.connect(self.open_second_name_window)
        self.second_window.add_street.clicked.connect(self.open_street_window)
        self.second_window.Ok_button.clicked.connect(self.main_manipulate) #Dont forget about sender
        self.new_window.show()

    def default_table(self):
        self.table_buffer_queary = ['' for i in range(8)]
        self.table_buffer = get_table()
        self.show_data_base()

    def show_data_base(self):
        #print(datas)
        self.ui.tableWidget.setRowCount(0)
        for i in range(len(self.table_buffer)):
            self.ui.tableWidget.insertRow(i)
            for j in range(len(self.table_buffer[i])):
                self.ui.tableWidget.setItem(i,j-1,QTableWidgetItem(str(self.table_buffer[i][j])) )



    def open_update_window(self):
        self.operation_buf = self.sender()
        self.new_window = QtWidgets.QDialog()
        self.second_window = Update_window()
        self.second_window.setupUi(self.new_window)
        self.second_window.fam_comboBox.addItems(["Not stated"] + get_combo("SELECT f_value FROM fam"))
        self.second_window.fam_comboBox_2.addItems(["Not stated"] + get_combo("SELECT f_value FROM fam"))
        self.second_window.name_comboBox.addItems(["Not stated"] + get_combo("SELECT n_value FROM names"))
        self.second_window.name_comboBox_2.addItems(["Not stated"] + get_combo("SELECT n_value FROM names"))
        self.second_window.second_name_comboBox.addItems(["Not stated"] + get_combo("SELECT sn_value FROM second_name"))
        self.second_window.second_name_comboBox_2.addItems(["Not stated"] + get_combo("SELECT sn_value FROM second_name"))
        self.second_window.street_comboBox.addItems(["Not stated"] + get_combo("SELECT s_value FROM street"))
        self.second_window.street_comboBox_2.addItems(["Not stated"] + get_combo("SELECT s_value FROM street"))
        self.second_window.Ok_button.clicked.connect(self.main_manipulate)
        self.new_window.show()

    def open_fam_window(self):
        self.FAM_window = QtWidgets.QDialog()
        self.f_window = parent_window()
        self.f_window.setupUi(self.FAM_window)
        self.f_window.where_comboBox.addItems(get_combo("SELECT f_value FROM fam"))
        self.f_window.update_button.clicked.connect(self.fam_manipulate)
        self.f_window.delete_button.clicked.connect(self.fam_manipulate)
        self.f_window.insert_button.clicked.connect(self.fam_manipulate)
        self.FAM_window.show()

    def open_name_window(self):
        self.NAME_window = QtWidgets.QDialog()
        self.n_window = parent_window()
        self.n_window.setupUi(self.NAME_window)
        self.n_window.where_comboBox.addItems(get_combo("SELECT n_value FROM names"))
        self.n_window.update_button.clicked.connect(self.name_manipulate)
        self.n_window.delete_button.clicked.connect(self.name_manipulate)
        self.n_window.insert_button.clicked.connect(self.name_manipulate)
        self.NAME_window.show()

    def open_second_name_window(self):
        self.SNAME_window = QtWidgets.QDialog()
        self.sn_window = parent_window()
        self.sn_window.setupUi(self.SNAME_window)
        self.sn_window.where_comboBox.addItems(get_combo("SELECT sn_value FROM second_name"))
        self.sn_window.update_button.clicked.connect(self.second_name_manipulate)
        self.sn_window.delete_button.clicked.connect(self.second_name_manipulate)
        self.sn_window.insert_button.clicked.connect(self.second_name_manipulate)
        self.SNAME_window.show()

    def open_street_window(self):
        self.S_window = QtWidgets.QDialog()
        self.s_window = parent_window()
        self.s_window.setupUi(self.S_window)
        self.s_window.where_comboBox.addItems(get_combo("SELECT s_value FROM street"))
        self.s_window.update_button.clicked.connect(self.street_manipulate)
        self.s_window.delete_button.clicked.connect(self.street_manipulate)
        self.s_window.insert_button.clicked.connect(self.street_manipulate)
        self.S_window.show()
        

    def main_manipulate(self):
        operation = self.operation_buf.text()
        #print(operation)
        query_items = list()
        query_items.append(self.second_window.fam_comboBox.currentText())
        query_items.append(self.second_window.name_comboBox.currentText())
        query_items.append(self.second_window.second_name_comboBox.currentText())
        query_items.append(self.second_window.street_comboBox.currentText())
        query_items.append(self.second_window.bldng_lineEdit.text())
        query_items.append(self.second_window.bldng_k_lineEdit.text())
        query_items.append(self.second_window.appr_lineEdit.text())
        query_items.append(self.second_window.telef_lineEdit.text())
        new_data = dict()
        if query_items[0] != "Not stated":
            fam = str(command(f"SELECT f_id FROM fam WHERE f_value = '{query_items[0]}'")[0][0])
        else:
            fam = "Not stated"
        if query_items[1] != "Not stated":
            name = str(command(f"SELECT n_id FROM names WHERE n_value = '{query_items[1]}'")[0][0])
        else:
            name = "Not stated"
        if query_items[2] != "Not stated":
            second_name = str(command(f"SELECT sn_id FROM second_name WHERE sn_value = '{query_items[2]}'")[0][0])
        else:
            second_name = "Not stated"
        if query_items[3] != "Not stated":
            street = str(command(f"SELECT s_id FROM street WHERE s_value = '{query_items[3]}'")[0][0])
        else:
            street = "Not stated"
        if operation == "UPDATE":
            #Не предусмотрено значение Not stated
            if self.second_window.fam_comboBox_2.currentText() !=  "Not stated":
                new_fam = str(command(f"SELECT f_id FROM fam WHERE f_value = '{self.second_window.fam_comboBox_2.currentText()}'")[0][0])
            else:
                new_fam = "Not stated"
            new_data["fam"] = new_fam
            if self.second_window.name_comboBox_2.currentText() != "Not stated":
                new_name = str(command(f"SELECT n_id FROM names WHERE n_value = '{self.second_window.name_comboBox_2.currentText()}'")[0][0])
            else:
                new_name = "Not stated"
            new_data["names"] = new_name
            if self.second_window.second_name_comboBox_2.currentText() != "Not stated":
                new_sn = str(command(f"SELECT sn_id FROM second_name WHERE sn_value = '{self.second_window.second_name_comboBox_2.currentText()}'")[0][0])
            else:
                new_sn = "Not stated"
            new_data["second_name"] = new_sn
            if self.second_window.street_comboBox_2.currentText() != "Not stated": 
                new_street = str(command(f"SELECT s_id FROM street WHERE s_value = '{self.second_window.street_comboBox_2.currentText()}'")[0][0])
            else:
                new_street =  "Not stated"
            new_data["street"] = new_street
            new_data["bldng"] = self.second_window.bldng_lineEdit_2.text() #Добавь данные для обновления
            new_data["bldng_k"] = self.second_window.bldng_k_lineEdit_2.text()
            new_data["appr"] = self.second_window.appr_lineEdit_2.text()
            new_data["telef"] = self.second_window.telef_lineEdit_2.text()

        try:
            #print(query_items)
            if operation == "SELECT":
                self.table_buffer_queary = [fam, name, second_name, street, query_items[4], query_items[5], query_items[6], query_items[7]]
                #print(query_items)
                self.table_buffer = get_table([fam, name, second_name, street, query_items[4], query_items[5], query_items[6], query_items[7]])
            else:
                
                main(operation, fam, name, second_name, street, query_items[4], query_items[5], query_items[6], query_items[7], new_data)
                self.table_buffer = get_table(self.table_buffer_queary) # Стоит не получать заново всю таблицу, а добавлять новую запись

            self.show_data_base()
            #print("")
        except:
            print("There must be error-window")
        #main(operation, fam, name, second_name, street, query_items[4], query_items[5], query_items[6], query_items[7], new_data)

    def fam_manipulate(self):
        operation = self.sender()
        f_value = self.f_window.new_value_lineEdit.text()
        where = self.f_window.where_comboBox.currentText()
        parent_table('fam', 'f_value', operation.text(), where, f_value)

    def name_manipulate(self):
        operation = self.sender()
        n_value = self.n_window.new_value_lineEdit.text()
        where = self.n_window.where_comboBox.currentText()
        parent_table("names", 'n_value', operation.text(), where, n_value)
      
    def street_manipulate(self):
        operation = self.sender()
        s_value = self.s_window.new_value_lineEdit.text()
        where = self.s_window.where_comboBox.currentText()
        parent_table("street", 's_value', operation.text(), where, s_value)

    def second_name_manipulate(self):
        operation = self.sender()
        sn_value = self.sn_window.new_value_lineEdit.text()
        where = self.sn_window.where_comboBox.currentText()
        parent_table("second_name", "sn_value", operation.text(), where, sn_value)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main_window()
    window.show()
    sys.exit(app.exec_())
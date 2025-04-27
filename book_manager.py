import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt

class BookManagerApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(BookManagerApp, self).__init__()
        uic.loadUi('book_manager.ui', self)
        
        self.label_student_info.setText("NIM: F1D022102 | Nama: Yusril Ibtida Ramdhani | Kelas: D | Mini Project")
        self.label_student_info.setStyleSheet("font-weight: bold; color: #2c3e50; background-color: #ecf0f1; padding: 5px;")
        self.label_student_info.setAlignment(Qt.AlignCenter)
        
        self.button_add_book.clicked.connect(self.add_book)
        self.button_clear.clicked.connect(self.clear_form)
        self.button_edit_book.clicked.connect(self.edit_book)
        self.button_remove_book.clicked.connect(self.remove_book)
        self.actionAbout.triggered.connect(self.show_about_dialog)
        
        self.table_books.setColumnCount(5)
        self.table_books.setHorizontalHeaderLabels(['Title', 'Author', 'Year', 'Genre', 'Rating'])
        self.table_books.horizontalHeader().setStretchLastSection(True)
        self.table_books.setAlternatingRowColors(True)

        button_style = """
            QPushButton {
                background-color: %s;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: %s;
            }
        """
        self.button_add_book.setStyleSheet(button_style % ("#3498db", "#2980b9"))
        self.button_clear.setStyleSheet(button_style % ("#e74c3c", "#c0392b"))
        self.button_edit_book.setStyleSheet(button_style % ("#2ecc71", "#27ae60"))
        self.button_remove_book.setStyleSheet(button_style % ("#f1c40f", "#e67e22"))

        self.combo_genre.addItems(['Fiction', 'Non-Fiction', 'Sci-Fi', 'Fantasy', 'Mystery', 'Biography'])

        self.editing_row = None

    def add_book(self):
        title = self.lineedit_title.text().strip()
        author = self.lineedit_author.text().strip()
        year = self.spinbox_year.value()
        genre = self.combo_genre.currentText()
        rating = self.spinbox_rating.value()
        
        if not title or not author:
            QMessageBox.warning(self, "Input Error", "Please complete all fields!")
            return
        
        if self.editing_row is not None:
            self.update_table_row(self.editing_row, title, author, year, genre, rating)
            self.editing_row = None
            QMessageBox.information(self, "Success", "Book updated successfully!")
        else:
            row_count = self.table_books.rowCount()
            self.table_books.insertRow(row_count)
            self.update_table_row(row_count, title, author, year, genre, rating)
            QMessageBox.information(self, "Success", "Book added successfully!")
        
        self.clear_form()

    def update_table_row(self, row, title, author, year, genre, rating):
        self.table_books.setItem(row, 0, QTableWidgetItem(title))
        self.table_books.setItem(row, 1, QTableWidgetItem(author))
        self.table_books.setItem(row, 2, QTableWidgetItem(str(year)))
        self.table_books.setItem(row, 3, QTableWidgetItem(genre))
        self.table_books.setItem(row, 4, QTableWidgetItem(str(rating)))

    def edit_book(self):
        selected_rows = self.table_books.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Editing Error", "Please select a book to edit!")
            return
        
        row = selected_rows[0].row()
        self.editing_row = row
        
        self.lineedit_title.setText(self.table_books.item(row, 0).text())
        self.lineedit_author.setText(self.table_books.item(row, 1).text())
        self.spinbox_year.setValue(int(self.table_books.item(row, 2).text()))
        self.combo_genre.setCurrentText(self.table_books.item(row, 3).text())
        self.spinbox_rating.setValue(int(self.table_books.item(row, 4).text()))

        QMessageBox.information(self, "Edit Mode", "Form populated with selected book's details. Modify and click 'Add Book' to update.")

    def remove_book(self):
        selected_rows = self.table_books.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Removing Error", "Please select a book to remove!")
            return
        
        row = selected_rows[0].row()
        reply = QMessageBox.question(self, "Confirm Delete", 
                                   "Are you sure that you want to remove this book?",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.table_books.removeRow(row)
            self.clear_form()
            QMessageBox.information(self, "Success", "Book removed successfully!")

    def clear_form(self):
        self.lineedit_title.clear()
        self.lineedit_author.clear()
        self.spinbox_year.setValue(2025)
        self.combo_genre.setCurrentIndex(0)
        self.spinbox_rating.setValue(1)
        self.editing_row = None

    def show_about_dialog(self):
        QMessageBox.about(self, "About Book Manager", 
                         "Mini Project\nPemrograman Visual\nF1D022102\nYusril Ibtida Ramdhani\nKelas D")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = BookManagerApp()
    window.show()
    sys.exit(app.exec_())

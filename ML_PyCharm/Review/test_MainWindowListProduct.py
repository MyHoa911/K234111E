from PyQt6.QtWidgets import QApplication, QMainWindow

from Review.MainWindowListProductExt import MainWindowListProductExt

app=QApplication([])
qmain=QMainWindow()
my_window=MainWindowListProductExt()
my_window.setupUi(qmain)

lp.ListProduct()
lp.add_product(Product())

my_window.showWindow()
app.exec()

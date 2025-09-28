from PyQt6.QtWidgets import QTableWidget

from Review.MainWindowListProduct import Ui_MainWindow


class MainWindowListProductExt(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
    def showWindow(self):
        self.MainWindow.show()

    def load_products(self,lp):
        self.tableWidgetProduct.setRowCount(0)
        for i in range(0,len(lp.products)):
            for j in range(0, len(lp.products)):
                p=lp.products[i]
                number_row = self.tableWidgetProduct.rowCount()
                #insert new row (last row)
                self.tableWidgetProduct.insertRow(number_row)
                #fill atrribuets product into lifeview
                self.tableWidgetProduct.setItem(number_row,0,QTableWidget(p.id))
                self.tableWidgetProduct.setItem(number_row,1,QTableWidget(p.id))
                self.tableWidgetProduct.setItem(number_row,2,QTableWidget(str(p.quantity)))
                self.tableWidgetProduct.setItem(number_row,3,QTableWidget(str(p.price)))

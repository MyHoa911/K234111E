class Product:
#local: khai báo trong đối số của hàm
#global: khai báo ngoài hàm
    def __init__(self, id=None, name=None, quantity=None, price=None): #tự động khởi tạo gtri khi đc cấp ô nhớ
        self.id=id
        self.name=name    #self: đây là thuộc tính của product
        self.quantity=quantity
        self.price=price
    def __str__(self): #tự động xuất dữ liệu ra màn hình
        infor="{}\t{}\t{}\t{}".format(self.id, self.name,
                                      self.quantity, self.price)
        return infor

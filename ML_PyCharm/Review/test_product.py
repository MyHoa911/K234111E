from Review.product import Product

p1=Product("p1", "Coca", 15, 34)
print(p1) #auto invoke __str__

p2=Product() #lúc này các thuộc tính không đưuọc gán giá trị
                # nên bị None --> k sài đưuọc
#bắt buộc ta phải làm thủ công:
p2.id="p2"
p2.name="Pepsi"
print(p2)
from Review.product import Product
from Review.products import ListProduct

lp=ListProduct()
lp.add_product(Product("p1","coca",15,38))
lp.add_product(Product("p2","pepsi",14,45))
lp.add_product(Product("p3","sting",13,76))
lp.add_product(Product("p4","redbull",19,45))
lp.print_products()
lp.descending_price()
print("--List Products - Sort Desc Price:----")
lp.print_products()
print("--List Products - Sort Asc Price:----")

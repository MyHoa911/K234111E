class ListProduct:
    def __init__(self):
        self.products=[]
    def add_product(self,p):
        self.products.append(p)
    def print_products(self):
        for p in self.products:
            print(p)
    def descending_price(self):
        for i in range(0,len(self.products)):
            for j in range(i+1,len(self.products)):
                pi=self.products[i] #số lượng phần tử trong i
                pj=self.products[j]
                if pi.price < pj.price:
                    self.products[i]=pj
                    self.products[j]=pi

    def ascending_price(self):
        for i in range(0,len(self.products)):
            for j in range(i+1,len(self.products)):
                pi=self.products[i] #số lượng phần tử trong i
                pj=self.products[j]
                if pi.price > pj.price:
                    self.products[i]=pj
                    self.products[j]=pi


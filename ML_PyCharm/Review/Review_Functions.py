def digit_separator(n):
    a=n%10
    b=(n//10)%10
    c=n//100
    return a,b,c
a,b,c=digit_separator(789)
print("a=",a)
print("b=",b)
print("c=",c)
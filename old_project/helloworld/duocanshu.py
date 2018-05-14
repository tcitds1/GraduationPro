def total(a = 5,*numbers, **phonebook):
    print('a', a)
    for values in numbers:
        print('value = ',values)
    for name,value in phonebook.items():
        print('name = ',name,'value = ',value)
        
total(10,1,2,3,Jack=1123,John=2231,Inge=1560)
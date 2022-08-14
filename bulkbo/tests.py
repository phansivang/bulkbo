def print_kwargs(**kwargs):
    for key in kwargs:
        print("The key {} holds {} value".format(key, kwargs[key]))

print_kwargs(a=1, b=2, c="Some Text")

def hello(**kwargs):
  for i in kwargs:
    print(i)


hello(a=1,b=2)
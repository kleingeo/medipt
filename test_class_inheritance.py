

class Parent:
    def __init__(self, name, options
                 ):
        self.name = name

        self.options = options


    def print(self):
        print(self.name)
        print(self.options)


class Child(Parent):
    def do_this(self,
                a: str):

        print(a)
        self.print()


if __name__ == '__main__':

    Child(name='name', options='fucl').do_this(a='a')
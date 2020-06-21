from codestatlib import stat_complexity, stat_object

@stat_object
@stat_complexity
def foo():
    print("hello")


if __name__ == "__main__":
    foo()
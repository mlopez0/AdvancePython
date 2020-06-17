def print_multiline_cell(lines, strip_line = False):
    if not lines:
        print("""\tNone of this""")
        return

    for line in lines:
        line *= line if not strip_line else line.strip()
        print("\t", line.replace("\n",""))
    print((1,2,3))

x = 0
print((1,2,3))
x+= 11.2
x = [1, 2, 3]
y = {'a': 'w'}
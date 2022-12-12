list = [
    ["a",1],
    ["b",2]
    ]


def get_name(name):
    for i in list:
        if i[0] == name:
            return list.index(i)

def get_step(name):
    for i in list:
        if i[0] == name:
            return list[list.index(i)][1]

print(get_step("a"))


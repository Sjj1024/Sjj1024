

def exec_jisuan():
    str = "88 + 10"
    res = eval(str)
    print(res)


def get_value():
    print("获取dict的值")
    form = {
        "name": "1",
        "age": "2"
    }
    value_list = list(form.values())
    print(value_list)


def list_add():
    list1 = ["a", "b", "c", "d"]
    list2 = ["e", "f", "g", "h"]
    list3 = [*list1, *list2]
    print(list3)


if __name__ == '__main__':
    list_add()
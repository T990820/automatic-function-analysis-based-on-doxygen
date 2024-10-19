from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.contents = []
        self.content  = ""

    def handle_starttag(self, tag, attrs):
        if tag == "div":
            self.content = ""

    def handle_endtag(self, tag):
        if tag == "div":
            self.contents.append(self.content)

    def handle_data(self, data):
        self.content = self.content + data

class function:
    def __init__(self):
        self.flag_brief    = False
        self.flag_details  = False
        self.flag_paramin  = False
        self.flag_paramout = False
        self.name          = None
        self.paramin       = []
    def __str__(self):
        return f"函数名: {self.name}, 输入参数列表: {self.paramin}"

class parameter:
    def __init__(self):
        self.type = None
        self.name = None
    def __str__(self):
        return f"\t类型: {self.type}，参数名: {self.name}"

def is_all_blank_or_num(variable):
    res = True
    for i in variable:
        if not (i == ' ' or (i >= '0' and i <= '9')):
            res = False
    return res

def test_function_list(function_list):
    for func in function_list:
        print(func)
        for param in func.paramin:
            print(param)
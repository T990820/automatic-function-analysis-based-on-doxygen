import utils
import chardet

passwd = "没人能想到这个密码"
html_filename = r'E:\航天二院23所\自动生成软件报告\学生信息管理系统\doc\html\_student_information_management_system_8h_source.html'
# 检测文件编码
with open(html_filename, 'rb') as f:
    raw_data = f.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']
contents_flag     = -1 # <div class="contents">所在的行数
contents_end_flag = -1 # </div><!-- contents -->所在的行数
row_idx           = 0  # 当前遍历到的行号
html_contents     = [] # <div class="contents">和</div><!-- contents -->之间的内容
with open(html_filename, 'r', encoding=encoding) as file:
    line = file.readline()
    while line:
        row_idx = row_idx + 1
        if "<div class=\"contents\">" in line:
            contents_flag = row_idx
            line = file.readline()
            continue
        if "<div class=\"ttc\"" in line:
            contents_end_flag = row_idx
            break
        if contents_flag > 0:
            html_contents.append(line)
        line = file.readline()
# 解析<div class="contents">和</div><!-- contents -->之间的每条内容
parser = utils.MyHTMLParser()
for html_content in html_contents:
    parser.feed(html_content)
# 删除每条解析结果前面的空格和数字
i = 0
while i < len(parser.contents):
    if len(parser.contents[i].strip(' ')) == 0 or len(parser.contents[i]) == 0 or utils.is_all_blank_or_num(parser.contents[i]):
        del parser.contents[i]
        continue
    # print(parser.contents[i])
    # print(len(parser.contents[i]))
    while parser.contents[i][0] == ' ' or (parser.contents[i][0] >= '0' and parser.contents[i][0] <= '9'):
        parser.contents[i] = parser.contents[i][1:]
    i = i + 1
# 记录函数定义范围
i = 0
brace_level = 0
brace_row   = [] # 由各函数起始位置和中止位置构成的行向量组
brace_start = 0  # 函数定义起始位置
brace_end   = 0  # 函数定义中止位置
while i < len(parser.contents):
    for j in range(len(parser.contents[i])):
        if parser.contents[i][j] == '{':
            brace_level = brace_level + 1
            if brace_level == 1:
                brace_start = i
        if parser.contents[i][j] == '}':
            brace_level = brace_level - 1
            if brace_level == 0:
                brace_end = i
                brace_row.append([brace_start,brace_end])
    i = i + 1
# 替换掉函数定义
for i in brace_row:
    for j in range(i[0],i[1]+1):
        parser.contents[j] = passwd
# 删除函数定义
i = 0
while i < len(parser.contents):
    if parser.contents[i] == passwd:
        del parser.contents[i]
        continue
    i = i + 1
# 记录小括号定义范围
i = 0
brace_level = 0
brace_start = 0  # 函数定义起始位置
brace_end   = 0  # 函数定义中止位置
while i < len(parser.contents):
    if "(" in parser.contents[i] and ")" in parser.contents[i]:
        i = i + 1
        continue
    elif "(" in parser.contents[i]:
        brace_start = i
    else:
        parser.contents[brace_start] = parser.contents[brace_start] + parser.contents[i]
    i = i + 1
# 删除不合法的函数声明
i = 0
while i < len(parser.contents):
    if "(" not in parser.contents[i] or ")" not in parser.contents[i] or ";" not in parser.contents[i]:
        del parser.contents[i]
        continue
    i = i + 1
for i in range(len(parser.contents)):
    print(parser.contents[i])
print("==============================")
# 获取html_filename中的函数列表
function_list = []
for content in parser.contents:
    func = utils.function()
    func.name = content.split(' ')[1].split('(')[0]
    # 获取当前函数的所有输入参数
    brace_level = 0
    params = ''
    for c in content:
        if c == '(':
            brace_level = brace_level + 1
        elif c == ')':
            brace_level = brace_level - 1
        else:
            if brace_level > 0:
                params = params + c
    # params 一般为 char* name,int age,int mom
    for param in params.split(','):
        if len(param) == 0:
            continue
        param = param.strip(' ') # 删除参数字符串开头和结尾的空格
        param = param.split(' ') # 分割成若干独立的变量
        i = 0
        while i < len(param): # 删除参数字符串中间多余的空格
            if param[i] == ' ':
                del param[i]
                continue
            i = i + 1
        assert len(param) == 2, "参数错误！"
        parameter_inst = utils.parameter()
        parameter_inst.type = param[0]
        parameter_inst.name = param[1]
        func.paramin.append(parameter_inst)
    function_list.append(func)
utils.test_function_list(function_list)
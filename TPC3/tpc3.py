import re

title_regex = re.compile(r'(#+) (.*)')
bold_regex = re.compile(r'\*\*(.*)\*\*')
italic_regex = re.compile(r'\*(.*)\*')
list_regex = re.compile(r'([1-9])\d*\.\s*(.*)')
link_regex = re.compile(r'\[(.*?)\]\((.*?)\)')
img_regex = re.compile(r'\!\[(.*?)\]\((.*?)\)')

def convert_title(title):
    match = title_regex.search(title)
    if match:
        level = len(match.group(1))
        content = match.group(2)
        return f'<h{level}>{content}</h{level}>'
    return title

def convert_bold(bold):
    text = bold_regex.sub(r'<b>\1</b>', bold)
    return text

def convert_italic(italic):
    match = italic_regex.sub(r'<i>\1</i>', italic)
    return match

def convert_list(list):
    res = ""
    first = True
    in_list = False
    lines = list.split('\n')
    for line in lines:
        match = list_regex.match(line)
        if first:
            res += '<ol>\n'
            first = False
            in_list = True
        elif match.group(1) == '1' and in_list:
            res += '</ol>\n'
            res += '<ol>\n'
        if match:
            res += f'<li>{match.group(2)}</li>\n'
        else:
            res += '</ol>\n'
            return res
    return res + '</ol>'

def convert_link(link):
    match = link_regex.sub(r'<a href="\2">\1</a>', link)
    return match

def convert_img(img):
    match = img_regex.sub(r'<img src="\2" alt="\1">', img)
    return match

def convert_markdown(markdown_text):
    lines = markdown_text.split('\n')
    res = ""
    list_buffer = []
    in_list = False
    for i, line in enumerate(lines):
        line = convert_title(line)
        line = convert_bold(line)
        line = convert_italic(line)
        line = convert_img(line)
        line = convert_link(line)
        if re.search(r'[1-9]\d*\.\s*.*', line):
            list_buffer.append(line)
            in_list = True
            continue
        else:
            if in_list:
                res += (convert_list('\n'.join(list_buffer)))
                list_buffer = []
                in_list = False
        if i == len(lines) - 1:
            res += line
        else:
            res += line + '\n'
    return res

def main():
    markdown_text = """ # ** *Título Principal* **
## Subtítulo
### Subsubtítulo

Este é um **exemplo** de *Markdown*.

Como pode ser consultado em [página da UC](http://www.uc.pt)
[página de PL](http://www.pl.pt) [página de SSI](http://www.ssi.pt)![imagem de um cão](http://www.cao.com)
Como se vê na imagem seguinte: ![imagem dum coelho](http://www.coellho.com) ![imagem de um gato](http://www.gatoo.com) [página de BD](http://www.bd.pt)

1.*Primeiro item*
2. Segundo item
3. Terceiro item
1. Quarto item
1. Quinto item
"""
    html_text = convert_markdown(markdown_text)
    print(html_text)
    
main()
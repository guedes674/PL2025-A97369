import re

def convert_title(title):
    match = re.search(r'(#+) (.*)', title)
    if match:
        level = len(match.group(1))
        content = match.group(2)
        return f'<h{level}>{content}</h{level}>'
    return title

def convert_bold(bold):
    text = re.sub(r'\*\*(.*)\*\*', r'<b>\1</b>', bold)
    return text

def convert_italic(italic):
    match = re.sub(r'\*(.*)\*', r'<i>\1</i>', italic)
    return match

def convert_list(list):
    res = ""
    first = True
    lines = list.split('\n')
    for line in lines:
        if first:
            res += '<ol>\n'
            first = False
        match = re.search(r'\d+\.\s*(.*)', line)
        if match:
            res += f'<li>{match.group(1)}</li>\n'
        else:
            res += '</ol>\n'
            return res
    return res + '</ol>'

def convert_link(link):
    match = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', link)
    return match

def convert_img(img):
    match = re.sub(r'\!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1">', img)
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
        if re.search(r'\d+\.\s*.*', line):
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
    markdown_text = """# **Título Principal**
## Subtítulo
### Subsubtítulo

Este é um **exemplo** de *Markdown*.

1.*Primeiro item*
2. Segundo item
3. Terceiro item

Como pode ser consultado em [página da UC](http://www.uc.pt)
[página de PL](http://www.pl.pt) [página de SSI](http://www.ssi.pt)![imagem de um cão](http://www.cao.com)
Como se vê na imagem seguinte: ![imagem dum coelho](http://www.coellho.com) ![imagem de um gato](http://www.gatoo.com) [página de BD](http://www.bd.pt)
"""
    html_text = convert_markdown(markdown_text)
    print(html_text)
    
main()
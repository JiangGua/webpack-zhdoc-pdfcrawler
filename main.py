import requests
from bs4 import BeautifulSoup
import pdfkit

def load_css(html):
    with open('style.css', 'r') as f:
        style = f.read()
    html_css = html.format(style = style)
    return html_css

# 传入任意页面的URL即可，返回一个迭代器，包含所有页面的链接
def get_url_list(url):
    root = 'https://webpack.docschina.org'
    homepage = requests.get(url)
    soup = BeautifulSoup(homepage.content, 'lxml')
    chapters = soup.find_all(class_='navigation__child')
    pages = []
    for chapter in chapters:
        page_html = requests.get(root + chapter.get('href'))
        page_soup = BeautifulSoup(page_html.content, 'lxml')
        pages.extend(page_soup.find_all(class_='sidebar-item__title'))

    pages = map(lambda x: root + str(x.get('href')), pages)
    return pages

# 传入每一个页面的URL和已有html，返回新的html
def get_content(url, html):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    content = soup.find(class_='page__content')
    content = content.find_all('div')[1]
    new_html = html + '<h1>{title}</h1>\n'.format(title = soup.title.string) + str(content)
    #html = html_template.format(style = style, content = str(content), title = soup.title.string)
    #file_name = soup.title.string + '.html'
    #with open(file_name, 'w', encoding = 'utf-8') as file_obj:
    #    file_obj.write(html)
    return new_html

def save_pdf(file_name):
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ], 
    }
    pdfkit.from_file(file_name + '.html', file_name + '.pdf', options=options)

# main
html = """ 
<!DOCTYPE html> 
<html lang="en"> 
<head> 
    <meta charset="UTF-8"> 
    <style>
        {style}
    </style>
</head> 
<body> 
"""  

html = load_css(html)
urls = get_url_list('https://webpack.docschina.org/concepts/')
i = 0
for url in urls:
    html = html + get_content(url, html) + '\n<br/>'
    print(url + " completed")

html = html + '</body>\n</html>'
with open('book.html', 'w', encoding='utf-8') as f:
    f.write(html)
save_pdf('book')
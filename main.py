import requests
from bs4 import BeautifulSoup
import pdfkit

# 传入每一个页面的URL，将正文写入 title.html 的文件中，并返回 title (title 即页面大标题)
def load_content(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    content = soup.find(class_='page__content')
    html = str(content)
    file_name = soup.title.string + '.html'
    with open(file_name, 'w', encoding = 'utf-8') as file_obj:
        file_obj.write(html)
    return soup.title.string

# 传入任意页面的URL即可，返回一个迭代器，包含本章节所有页面的链接
def load_url_list(url):
    root = 'https://webpack.docschina.org'
    homepage = requests.get(url)
    soup = BeautifulSoup(homepage.content, 'lxml')
    pages = soup.find_all(class_='sidebar-item__title')
    pages = map(lambda x: root + str(x.get('href')), pages)
    return pages

#TODO:输出的格式太丑了, CSS貌似没套上?
def save_pdf(file_name):
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ], 
    }
    pdfkit.from_file(file_name + '.html', file_name + '.pdf', options=options, css='style.css')

save_pdf(load_content("https://webpack.docschina.org/concepts/"))

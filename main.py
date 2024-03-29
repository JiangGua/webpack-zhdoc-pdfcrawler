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

# 传入每一个页面的URL, 返回该页面html
def get_content(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    content = soup.find(class_='page__content')
    content = content.find_all('div')[1]
    new_html = '<h1>{title}</h1>\n'.format(title = soup.title.string) + str(content)
    return new_html

def save_pdf(file_name):
    options = {
        'page-size': 'A4',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ], 
    }
    pdfkit.from_file(file_name + '.html', file_name + '.pdf', options=options)

def rm_avatars(html):
    """
    删除'维护人员'部分
    """
    if html.find('<span class="text">维护人员</span>') != -1:
        index = html.find('<a aria-hidden="true" class="anchor" href="#维护人员" id="维护人员"></a>')
        index -= 20
        html = html[:index] + '</div>'
    return html

# main
if __name__ == '__main__':
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
    with open('book.html', 'w', encoding='utf-8') as f:
        f.write(html)

    urls = get_url_list('https://webpack.docschina.org/concepts/')
    for url in urls:
        html = get_content(url) + '\n<div class="break-after"></div>'
        html = rm_avatars(html)
        with open('book.html', 'a', encoding='utf-8') as f:
            f.write(html)
        print(url + " completed")

    with open('book.html', 'a', encoding='utf-8') as f:
        f.write('</body>\n</html>')

    save_pdf('book')
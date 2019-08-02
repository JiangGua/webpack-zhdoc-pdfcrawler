# webpack-zhdoc-pdfcrawler

爬取Webpack中文文档，并导出为PDF

## 依赖

- requests
- bs4
- pdfkit
- wkhtmltopdf

## 用法

直接执行 `python main.py` 即可，会在当前目录输出 book.html 和 book.pdf 俩文件。

貌似执行到最后那个 wkhtmltopdf 会报错，但输出出来的 PDF 看了看也没啥问题。

## 参考

[Python 爬虫：把廖雪峰教程转换成 PDF 电子书](https://foofish.net/python-crawler-html2pdf.html)

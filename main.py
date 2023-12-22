from bs4 import BeautifulSoup
import requests
import numpy as np
import xlsxwriter


def chitai_gorod():
    excel_book = []
    j = "2"
    url_page = ""
    workbook = xlsxwriter.Workbook("chitai-gorod.xlsx")
    worksheet = workbook.add_worksheet()
    row = 0
    excel_book.append(["Название книги", "Имя автора", "Стоимость"])
    while True:
        page = requests.get('https://www.chitai-gorod.ru/search?phrase=Python' + str(url_page))
        soup = BeautifulSoup(page.content, "html.parser")
        cards = soup.find_all("article", "product-card product-card product")
        if (len(cards)):
            for card in cards:
                book = card.find("div", "product-title__head")
                author = card.find("div", 'product-title__author')
                if card.find("div", "product-price__value product-price__value--discount"):
                    price = card.find("div", "product-price__value product-price__value--discount")
                    excel_book.append([book.text.strip(), author.text.strip(), price.text.strip()])
                elif card.find("div", "product-price__value"):
                    price = card.find("div", "product-price__value")
                    excel_book.append([book.text.strip(), author.text.strip(), price.text.strip()])
                else:
                    excel_book.append([book.text.strip(), author.text.strip(), "Отсутствует в продаже"])
            url_page = "&page=" + j
            jj = int(j)
            jj += 1
            j = str(jj)
        else:
            break
    res_book = np.array(excel_book)
    worksheet.set_column(0, 0, 40)
    worksheet.set_column(1, 1, 20)
    worksheet.set_column(2, 2, 13)
    worksheet.set_default_row(60)
    worksheet.set_row(0, 20)
    text_format = workbook.add_format({"text_wrap": True, "valign": "vcenter", "align": "center"})
    for col, data in enumerate(res_book.T):
        worksheet.write_column(row, col, data, text_format)
    workbook.close()


chitai_gorod()

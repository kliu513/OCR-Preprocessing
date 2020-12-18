import pdfplumber
import re
import os

path = 'test.pdf'
pdf = pdfplumber.open(path)
xml = open('results.xml', 'w', encoding='utf-8')
xml.write("<?xml version='1.0' encoding='utf-8'?>\n")
xml.write("<invoice>\n")


for page in pdf.pages:
    width = page.width
    height = page.height
    table1 = page.extract_tables()[0][0]
    table2 = page.extract_tables()[0][1]
    table3 = page.extract_tables()[0][2]
    table4 = page.extract_tables()[0][3]
    print(table1)
    print(table2)
    print(table3)
    print(table4)
    text = []
    for elem in page.extract_words():
        if elem['x0'] > width/3 and elem['bottom'] < height/5:
            text.append(elem['text'])
    for i in range(len(text)):
        text[i] = re.sub('\D', '', text[i])
    text = list(filter(lambda x: len(x) != 0, text))
    #print(text)
    xml.write("\t<invoiceCode>" + text[0] + "</invoiceCode>\n")
    xml.write("\t<invoiceNo.>" + text[1] + "</invoiceNo.>\n")
    xml.write("\t<date>" + text[2] + '-' + text[3] + '-' + text[4] + "</date>\n")
    xml.write("\t<checkCode>" + text[5] + text[6] + text[7] + text[8] + "</checkCode>\n")
    
    xml.write("\t<buyer>\n")
    xml.write("\t\t<name>" + table1[1].split('\n')[0].split(':')[1] + "</name>\n")
    xml.write("\t\t<id>" + table1[1].split('\n')[1] + "</id>\n")
    xml.write("\t</buyer>\n")

    xml.write("\t<services>\n")
    for i in range(1, len(table2[3].split('\n'))):
        xml.write("\t\t<service num=" + str(i) + ">\n")
        xml.write("\t\t\t<name>" + table2[0].split('\n')[i] + "</name>\n")
        xml.write("\t\t\t<unit>" + table2[3].split('\n')[i] + "</unit>\n")
        xml.write("\t\t\t<quantity>" + table2[4].split('\n')[i] + "</quantity>\n")
        xml.write("\t\t\t<unitPrice>" + table2[5].split('\n')[i] + "</unitPrice>\n")
        xml.write("\t\t\t<total>" + table2[8].split('\n')[i] + "</total>\n")
        xml.write("\t\t</service>\n")
    xml.write("\t</services>\n")

    xml.write("\t<seller>\n")
    xml.write("\t\t<name>" + table4[1].split('\n')[0].split(':')[1] + "</name>\n")
    xml.write("\t\t<id>" + table4[1].split('\n')[1] + "</id>\n")
    xml.write("\t\t<address>" + table4[1].split('\n')[3].split(':')[1].split(' ')[0] + "</address>\n")
    xml.write("\t\t<tel>" + table4[1].split('\n')[3].split(':')[1].split(' ')[1] + "</tel>\n")
    xml.write("\t\t<bank>" + table4[1].split('\n')[4].split(':')[1].split(' ')[0] + "</bank>\n")
    xml.write("\t\t<account>" + table4[1].split('\n')[4].split(':')[1].split(' ')[1] + "</account>\n")
    xml.write("\t</seller>\n")
    xml.write("</invoice>")
      
    """
    for pdf_table in page.extract_tables():
        table = []
        cells = []
        for row in pdf_table: 
            if not any(row):   #??
                # 如果一行全为空，则视为一条记录结束
                if any(cells):
                    table.append(cells)
                    cells = []
            elif all(row):
                # 如果一行全不为空，则本条为新行，上一条结束
                if any(cells):
                    table.append(cells)
                    cells = []
                table.append(row)
            else:
                if len(cells) == 0:
                    cells = row
                else:
                    for i in range(len(row)):
                        if row[i] is not None:
                            cells[i] = row[i] if cells[i] is None else cells[i] + row[i]
    """
    print('--------------------------')

pdf.close()
xml.close()
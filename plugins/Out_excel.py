import xlsxwriter
import os

class Out_excel(object):
    def __init__(self):
        pass

    def out_excel(self, file_name, info_list, headers):
        try:
            if len(info_list) == 0:
                return
            row = 0  # 行
            # 生成一个xlsxwriter.Workbook对象
            xls = xlsxwriter.Workbook(r'{}\{}.xlsx'.format(os.getcwd(), file_name))
            # 调用对象的add_worksheet方法
            sheet = xls.add_worksheet(''.format(file_name))
            column = 0  # 列
            for header in headers:
                sheet.write(row, column, header)
                column += 1
            row += 1
            for infos in info_list:
                column = 0
                if isinstance(infos, list):
                    for info in infos:
                        sheet.write(row, column, info)
                        column += 1
                    row += 1
                else:
                    sheet.write(row, column, infos)
                    column += 1
                    row += 1
            xls.close()
        except Exception as e:
            pass
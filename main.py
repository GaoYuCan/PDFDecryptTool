import os
import base64
import PyPDF2
import re

PATH = r"C:\Users\Sink\Downloads\50MB__软件工程实用案例教程_1665579110"

print(f"[>] scanning for html files.")

filename_list = os.listdir(PATH)
reg = re.compile(r'var PDFData = "(.+?)";')

tmp_files = []
i = 0

for file_name in filename_list:
    if not file_name.endswith('.html'):
        continue
    html_file = open(PATH + os.sep + file_name, 'rb')
    line_bytes = html_file.readline()
    while line_bytes:
        try:
            line = line_bytes.decode()
            match_res = reg.match(line)
            if match_res:
                print(f"[>] found target line, decrypting now.")
                pdf_data = match_res.group(1)
                pdf_data = base64.b64decode(pdf_data)
                print(f"[>] {file_name} decryption success.")
                t_path = f'{PATH}{os.sep}temp_{i}'
                tmp_files.append(t_path)
                tf = open(t_path, 'wb')
                tf.write(pdf_data)
                tf.close()
                break
        except:
            pass
        line_bytes = html_file.readline()
    html_file.close()
    i += 1
print(f'[>] pdf success done, merging pdf file.')
# 合并 PDF
pdf_merger = PyPDF2.PdfFileMerger()
for pdf in tmp_files:
    pdf_merger.append(pdf)
pdf_merger.write(PATH + os.sep + "merged.pdf")
pdf_merger.close()
# 移除临时文件
for pdf in tmp_files:
    os.remove(pdf)

print(f'[>] merger success, write to {PATH}{os.sep}merged.pdf.')
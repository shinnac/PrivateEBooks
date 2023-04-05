#複数PNGファイルを結合して単一PDFファイルを作るスクリプト
#マンガの自炊用(OCR処理なし)

import os
from PIL import Image
from PyPDF4 import PdfFileReader, PdfFileWriter
import tkinter as tk
from tkinter import filedialog, simpledialog

def convert_png_to_pdf(input_folder, output_folder):
    # フォルダが存在しない場合、作成する
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # inputフォルダ内のPNGファイルをPDFに変換してoutputフォルダに保存
    for file in os.listdir(input_folder):
        if file.endswith(".png"):
            png_path = os.path.join(input_folder, file)
            pdf_path = os.path.join(output_folder, os.path.splitext(file)[0] + ".pdf")
            image = Image.open(png_path)
            pdf = image.convert("RGB")
            pdf.save(pdf_path)

def merge_pdfs(output_folder, output_filename, save_folder):
    pdf_writer = PdfFileWriter()

    # outputフォルダ内のPDFファイルを読み込んで結合
    for file in os.listdir(output_folder):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(output_folder, file)
            pdf_reader = PdfFileReader(pdf_path)

            for page_num in range(pdf_reader.getNumPages()):
                pdf_writer.addPage(pdf_reader.getPage(page_num))

    # 結合したPDFを単一ファイルとして保存
    with open(os.path.join(save_folder, output_filename), "wb") as output_file:
        pdf_writer.write(output_file)


def select_folder(prompt_text):
    root = tk.Tk()
    root.withdraw()

    folder_path = filedialog.askdirectory(initialdir=os.getcwd(), title=prompt_text)
    return folder_path

#　フォルダパスと左上、右下ポイントを指定しフォルダパス内の画像をトリミングする。
#　トリミングした画像はsave_pathに保存する。
def trimming(folder_path, save_path, left, upper, right, lower):
    # トリミングするPNGファイルへのパスのリスト
    png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
    for file in png_files:
        # 画像を開く
        im = Image.open(folder_path + '\\'+ file)
        # 座標で切り抜く
        im_crop = im.crop((left, upper, right, lower))
        # 新しいファイル名で保存
        im_crop.save(save_path + '\\'+ file)

#フォルダ内のファイルを削除する。
def delete_files_in_folder(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)


# トリミングしたい座標
left = 193
upper = 100
right = 828
lower = 1000

# トリミングするPNGファイルが入ったフォルダのパス
# デフォルト値　r"C:\Users\shin\Desktop\screenshotFolder"
folder_path = select_folder('取り込んだPNGファイルが入っているフォルダを指定してください') 

# 本のタイトルを確定する
BookTitle = simpledialog.askstring(title="本のタイトル",
                                  prompt="書籍の名前を入力してください:")

# トリミングした後のPNGファイルを入れるフォルダのパス
save_path = r"C:\Users\shin\Documents\PrivateEBooks\input"

# トリミングを行う
trimming(folder_path, save_path, left, upper, right, lower)

#元のPNGファイルを削除する。
delete_files_in_folder(folder_path)


#　トリミング後のPNGファイルをPDFファイルに変換する
input_folder = "input"
output_folder = "output"
convert_png_to_pdf(input_folder, output_folder)

#　結合したPDFファイルを保存するフォルダのパス
Ebook_folder = r"C:\Users\shin\Documents\PrivateEBooks\PDFBooks"

# 結合したPDFファイルの保存名
merge_pdfs(output_folder, BookTitle + '.pdf', Ebook_folder)

#　途中経過ファイルの削除
delete_files_in_folder(input_folder)
delete_files_in_folder(output_folder)
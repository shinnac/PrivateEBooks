# フォルダパスを指定
$folderPath = "C:\Users\shin\Documents\PrivateEBooks\input"

# 出力フォルダを指定
$outputFolder = "C:\Users\shin\Documents\PrivateEBooks\output\"

# 指定されたフォルダ内のすべてのPNGファイルを取得
$files = Get-ChildItem $folderPath -Filter *.png

# すべてのPNGファイルに対して処理を行う
foreach ($file in $files) {
    # Tesseract OCRを使用してPDFファイルを作成
    &"C:\Program Files\Tesseract-OCR\tesseract.exe" $file.FullName "$outputFolder\$($file.BaseName)" -l jpn_vert pdf
}

explorer.exe $outputFolder
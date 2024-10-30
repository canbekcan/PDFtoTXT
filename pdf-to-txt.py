import os
import camelot
print(camelot.__version__)
from pdfminer.high_level import extract_text


def extract_tables_and_text(pdf_path, txt_path, csv_folder):
    # PDF'den metni çıkart
    text = extract_text(pdf_path)

    # PDF'den tabloları çıkart
    tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream')

    # CSV dosyalarını kaydet ve referansları metne ekle
    csv_references = []
    for i, table in enumerate(tables):
        csv_file_name = f'table_{i}.csv'
        csv_path = os.path.join(csv_folder, csv_file_name)
        table.to_csv(csv_path)
        csv_references.append(csv_file_name)

    # Metni ve CSV referanslarını TXT dosyasına yaz
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text + '\n\n' + 'Tablolar:\n' + '\n'.join(csv_references))


def convert_pdfs_in_folder(source_folder, target_folder):
    csv_folder = os.path.join(target_folder, 'csv')
    os.makedirs(csv_folder, exist_ok=True)

    for file_name in os.listdir(source_folder):
        if file_name.endswith('.pdf'):
            pdf_file_path = os.path.join(source_folder, file_name)
            txt_file_name = os.path.splitext(file_name)[0] + '.txt'
            txt_file_path = os.path.join(target_folder, txt_file_name)
            extract_tables_and_text(pdf_file_path, txt_file_path, csv_folder)
            print(f'İşlendi: {file_name}')


if __name__ == "__main__":
    source_folder = 'pdf'  # PDF dosyalarının bulunduğu klasör
    target_folder = 'txt'  # TXT ve CSV dosyalarının kaydedileceği klasör

    convert_pdfs_in_folder(source_folder, target_folder)

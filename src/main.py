from pdf.extractor import extract_pdf
from pdf.image import extract_image

def main():
    pdf = "example/Roteiro-Ada.pdf"
    image = "example/Relatório_de_Atividade__Análise_de_Interface.pdf"
    name_image = "teste_"
    extract_pdf(pdf)
    extract_image(image, name_image)
    
if __name__ == '__main__':
    main()
from fpdf import FPDF
from datetime import date

#Metodo para gerar PDF
def GerarPDF(rota):
    pdf = FPDF()
  
    # Adding a page
    pdf.add_page()
    
    # set style and size of font 
    pdf.set_font("Arial", size = 12)
    
    # create a cell
    pdf.cell(200, 10, txt = "ProLinear", ln = 1, align = 'C')
    pdf.cell(200, 10, txt = "Resultado da otimização de rota, {}".format(date.today()), ln = 2, align = 'C')
    
    # add another
    cont = 0
    for x in rota:
        cont += 1
        pdf.cell(200, 10, txt="{}º cidade: {}".format(cont, x),ln=6, align='L')
    pdf.cell(200, 10, txt="Retorna para: {}".format(rota[0]),ln=6, align='L')
    
    # save the pdf
    pdf.output("ProLinear.pdf")
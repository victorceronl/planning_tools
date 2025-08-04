# planning_tools
Scripts to simplify work at  Tunkers for Project Planning

Librerias esenciales: pandas, PyPDF2, fitz, os

filesName.py: Crea un listado en un archivo csv con los nombres de cada uno de los archivos de la carpeta en la variable: ruta_carpeta. Todos en orden de menor a mayor.

etiquetasPDF.py: Agrega etiquetas a archivos PDF de una carpeta carpeta_pdfs desde un arvhivo etiquetas.xlsx donde se consideran las siguientes columnas: A, B, C, D, E, F. Donde la primera (A) debe coincidir con el nombre del archivo.

PDFaJPG.py: Convierte los archivos PDF de una carpeta o Directorio a imagenes JPG y los guarda en una nueva carpeta.
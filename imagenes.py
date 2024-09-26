from PIL import Image, ImageDraw, ImageFont
import random

def dibujaGrafico(origen,img):
    # Abrir una imagen JPG existente
    imagen = Image.open(origen+'.jpg')

    # Generar un color aleatorio en formato RGB
    color_aleatorio = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Crear una nueva imagen del mismo tamaño que la original con el color aleatorio
    filtro_color = Image.new('RGB', imagen.size, color_aleatorio)

    # Combinar las dos imágenes usando transparencia (alpha)
    imagen_con_filtro = Image.blend(imagen, filtro_color, alpha=0.5)  # Ajusta el valor de alpha para la intensidad

    # Crear un objeto de dibujo para agregar texto
    dibujo = ImageDraw.Draw(imagen_con_filtro)

    # Definir la fuente (puedes cambiar el tamaño y la fuente personalizada si tienes una)
    fuente = ImageFont.load_default()

    # Definir el texto y su posición
    texto = "Hotel " + str(img);
    posicion = (10, 10)  # Coordenadas X, Y

    # Definir el color del texto (en formato RGB)
    color_texto = (0, 0, 0)  # Blanco

    # Escribir el texto en la imagen
    dibujo.text(posicion, texto, font=fuente, fill=color_texto)

    # Guardar la imagen con el filtro aplicado y el texto añadido
    imagen_con_filtro.save('imagenes/'+origen+'_'+str(img)+'.jpg')

    # Mostrar la imagen (opcional)
    #imagen_con_filtro.show()


hoteles= [303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,331,332,333,334,335,336,337,338,339,340,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,451,452,453,454,455,456,457,458,459,460,461,462,463,464,465,466,467,468,469,470,471,472,473,474,475,476,477,478,513,514,515,516,517,518,519,520,521,522,523,524,525,526,527,528,529,530,531,532,533,534,535,536,537,538,539,540]
campings =[50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,450,668,669,670,671,672,673,674,675,676,677,678,679,680,681,682,683,684,685,686,687,688,689,690,691,692,693,694,695,699,700,701,702,703,704,705,706,707,708,709,710,711,712,713,714,715,716,717,718,719,720,721,722,723,724,725,726]
hostales= [176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,544,545,546,547,548,549,550,551,552,553,554,555,556,557,558,559,560,561,562,563,564,565,566,567,568,569,570,571,575,576,577,578,579,580,581,582,583,584,585,586,587,588,589,590,591,592,593,594,595,596,597,598,599,600,601,602]
apartamentos =[113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,606,607,608,609,610,611,612,613,614,615,616,617,618,619,620,621,622,623,624,625,626,627,628,629,630,631,632,633,637,638,639,640,641,642,643,644,645,646,647,648,649,650,651,652,653,654,655,656,657,658,659,660,661,662,663,664]
for hotel in hoteles:
    dibujaGrafico('hotel',hotel)

for camping in campings:
    dibujaGrafico('hotel',camping)

for hostal in hostales:
    dibujaGrafico('hostal',hostal)

for apartamento in apartamentos:
    dibujaGrafico('apartamento',apartamento)
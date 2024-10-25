Función generar_archivo: 
Esta función permite crear tanto los archivos de RETENCIONES como SUJETOS en una sola definición de función.

Parámetros de consulta: 
Se utilizan parámetros (:cuit y :nro_interfase) en la consulta para mejorar la seguridad y legibilidad del código.

Estructura de archivos: 
El tipo de archivo (RETENCIONES o SUJETOS) se pasa como parámetro, y el nombre del archivo se ajusta dinámicamente.

Estructura principal: 
El bucle final recorre ORGANISMOS, y para cada clave-valor genera ambos archivos, uno de RETENCIONES y otro de SUJETOS.
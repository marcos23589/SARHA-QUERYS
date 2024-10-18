PARA EL FORMATEO DE LOS ARCHIVOS PARA SUBIR A LA BBDD PARA GANANCIAS:

1. Se corre en la máquina virtual el programa LIQAFIP.CBL que toma el archivo

- LIQMESII.IDX
- MAESTRO.IDX

y crea un txt formateado para trabajar con los programas en este proyecto.

2. Se corre liq_formateo.py que toma el txt y lo transforma en un excel

3. Se corre el ganancias_cobol.py que toma el excel creado anteriomente y lo formatea para crear otro excel con el formato de la tabla CONCEPTO_EMPLEADO de la BBDD.

4. SE RECOMIENDA QUE UNA VEZ CREADO EL EXCEL DE MIGRACION, SE PRUEBE CON 1 REGISTRO PARA ESTAR SEGURO DE LOS FORMATOS DE FECHA

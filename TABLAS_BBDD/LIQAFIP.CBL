
       IDENTIFICATION DIVISION.
       PROGRAM-ID.   LIQAFIP.
       AUTHOR.       MARCOS DANIEL OLIVERA.
       DATE-WRITTEN. 06/08/2024.
       SECURITY.
       ENVIRONMENT DIVISION.
       CONFIGURATION SECTION.
       SPECIAL-NAMES. DECIMAL-POINT IS COMMA.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.

           SELECT LIQMES
           ASSIGN TO DISK
           "S:\ADRITIMO\PEDIDOS\2024\11\LIQMESII.IDX"
           ORGANIZATION INDEXED
           ACCESS MODE DYNAMIC
           RECORD KEY LEGAJO-LIQ
           ALTERNATE RECORD KEY APELLIDO-LIQ WITH DUPLICATES.

           SELECT maestro
           ASSIGN TO DISK "S:\ADRITIMO\PEDIDOS\2024\11\MAESTRO.IDX"
           ORGANIZATION INDEXED
           ACCESS MODE DYNAMIC
           RECORD KEY LEGAJO-mae.


           SELECT salida
           ASSIGN TO DISK
           "S:\ADRITIMO\PEDIDOS\2024\11\LIQ-10-SALUD-COMPLE.TXT"
           ORGANIZATION LINE SEQUENTIAL.

           SELECT detalle
               assign to random NOMBRE-LIQMES
               organization is line sequential.



       DATA DIVISION.
       FILE SECTION.
       FD  LIQMES
           LABEL RECORDS ARE STANDARD.
       01  REC-LIQMES.
           05  LEGAJO-LIQ              pic 9(07).
           05  UBICACION-LIQ.
               10  ANEXO-LIQ           PIC 99.
               10  ITEM-LIQ            PIC 99.
               10  CLASE-LIQ           PIC 9.
               10  AGRUP-LIQ           PIC 99.
               10  NRO-ESTAB-LIQ       PIC 99.
               10  CATEGORIA-LIQ       pic 999.
               10  DESTINO-LIQ         PIC 9999.
           05  DOCUMENTO-LIQ.
               10  TIPO-LIQ            PIC 9.
               10  DOCU-LIQ            PIC 9(8).
           05  APELLIDO-LIQ            PIC X(30).
           05  HS-SEC-LIQ              PIC 99.
           05  HS-UNIV-LIQ             PIC 99.
           05  CONCEPT-LIQ  OCCURS 40 TIMES.
               10  CODIGO-LIQ          PIC  999.
               10  IMPORTE-LIQ         PIC  9(8)V99.
           05  ORDEN-LIQ               PIC 9(5).
           05  PLANTA-LIQ              PIC 9.
           05  DESCONTAR-LIQ           PIC 99.
           05  FECHA-LIQ.
               10  MES-LIQ             PIC 99.
               10  ANIO-LIQ            PIC 99.
           05  NRO-CONTROL             PIC 9(4).
           05  COD-LOC                 PIC 999.
           05  FICHERO                 PIC X(3).

       FD  MAESTRO
           LABEL RECORDS ARE STANDARD.
       01  REG-MAE.
           05 LEGAJO-MAE.
                   10  LEG-MAE             PIC 9(05).
                   10  INTER-MAE           PIC 9(01).
                   10  DAV-MAE             PIC 9(01).
               05  UBICACION-MAE.
                   10  ANEXO-MAE           PIC 9(02).
                   10  ITEM-MAE            PIC 9(02).
                   10  CLASE-MAE           PIC 9(01).
                   10  AGRUP-MAE           PIC 9(02).
                   10  NRO-ESTAB-MAE.
                       15 ESTAB1           PIC 9(01).
                       15 ESTAB2           PIC 9(01).
                   10  CATEG-MAE.
                       15  CAT1-MAE        PIC 9(01).
                       15  CAT2-MAE        PIC 9(02).
                   10  DESTINO-MAE         PIC 9(04).
                   10  PLANTA-MAE       PIC 9(01).
                   10  CARGO-FUNC-MAE      PIC 9(03).
               05  APEL-NOM-MAE            PIC X(30).
               05  APEL-MATER-MAE          PIC X(12).
               05  FECHA-ING-CTO-MAE.
                   10  DIA-CTO-MAE         PIC 9(02).
                   10  MES-CTO-MAE         PIC 9(02).
                   10  ANIO-CTO-MAE        PIC 9(02).
               05  FECHA-ING-DEF-MAE.
                   10  DIA-DEF-MAE         PIC 9(02).
                   10  MES-DEF-MAE         PIC 9(02).
                   10  ANIO-DEF-MAE        PIC 9(02).
               05  ANTIGUEDAD-ANTER-MAE.
                   10  ANT-PAGO-MAE        PIC 9(03).
                   10  ANT-LICENCIA-MAE    PIC 9(03).
               05  ANTIG-EN-DIAS-MAE REDEFINES ANTIGUEDAD-ANTER-MAE.
                   10  ANT-MAESTROS-MAE    PIC 9(06).
               05  FECHA-ULTIMO-ASCENSO-MAE.
                   10  DIA-ASCENSO-MAE     PIC 9(02).
                   10  MES-ASCENSO-MAE     PIC 9(02).
                   10  ANIO-ASCENSO-MAE    PIC 9(02).
               05  DOCTOS-IDENTIDAD-MAE.
                   10  COD-DNI-MAE         PIC 9(01).
                   10  NRO-DNI-MAE         PIC 9(10).
                   10  NRO-CIPF-MAE        PIC 9(11).
                   10  NRO-CISC-MAE        PIC 9(10).
      *             10  OFIC-ENROL-MAE      PIC 9(04).
               05  SEXO                    PIC 9(01).
               05  FECHA-NAC-MAE.
                   10 DIA-NAC-MAE          PIC 9(02).
                   10 MES-NAC-MAE          PIC 9(02).
                   10 ANIO-NAC-MAE         PIC 9(02).
               05  LUGAR-NAC-MAE           PIC 9(04).
               05  PAIS-NAC-MAE            PIC 9(02).
               05  NACIONALIDAD-MAE        PIC 9(02).
               05  NATURALIZACION-MAE.
                   10  FECHA-NATUR-MAE.
                       15  DIA-NATUR-MAE   PIC 9(02).
                       15  MES-NATUR-MAE   PIC 9(02).
                       15  ANIO-NATUR-MAE  PIC 9(02).
                   10  CARTA-CIUDAD-MAE    PIC X(10).
               05  ESTADO-CIVIL-MAE        PIC X(01).
               05  APEL-NOM-CONYUGE-MAE    PIC X(23).
               05  DOCTO-ID-CONYUGE-MAE.
                   10  COD-DOC-CONY-MAE    PIC 9(01).
                   10  NRO-DOC-CONY-MAE    PIC 9(10).
               05  FECHA-NAC-CONY-MAE.
                   10  DIA-CONY-MAE        PIC 9(02).
                   10  MES-CONY-MAE        PIC 9(02).
                   10  ANIO-CONY-MAE       PIC 9(02).
               05  HIJOS-MAE OCCURS     10 TIMES INDEXED BY H-MAE.
                   10  FECHA-NAC-HJ-MAE.
                       15  DIA-HJ-MAE      PIC 9(02).
                       15  MES-HJ-MAE      PIC 9(02).
                       15  ANIO-HJ-MAE     PIC 9(02).
                   10  SEXO-HJ-MAE         PIC 9(01).
                   10  DOCUMENTO-HJ-MAE.
                       15  COD-DOC-HJ-MAE  PIC 9(01).
                       15  NRO-DOC-HJ-MAE  PIC 9(10).
                   10  ESTUDIOS-HJ-MAE     PIC 9(02).
                   10 SUBSIDIO-HJ-MAE      PIC 9(01).
               05  FAM-A-CARGO-MAE         PIC 9(01).
               05  GRUPO-SANG-MAE          PIC 9(01).
               05  DOMICILIO-MAE           PIC X(38).
               05  LOCALIDAD-MAE           PIC X(15).
               05  COD-PROVINCIA-MAE       PIC X(01).
               05  ESTUDIOS-MAE.
                   10  ESTUDIO1-MAE.
                       15  EST11-MAE       PIC 9(01).
                       15  EST12-MAE       PIC 9(02).
                   10  ESTUDIO2-MAE.
                       15  EST21-MAE       PIC 9(01).
                       15  EST22-MAE       PIC 9(02).
               05  ACTIV-MILITAR-MAE.
                   10  SER-MILITAR-MAE     PIC 9(01).
                   10  ARMA-O-EXCEP-MAE    PIC 9(02).
                   10  ANIO-SERV-MAE       PIC 9(02).
                   10  ESPEC-MIL-MAE       PIC 9(02).
                   10  GRADO-MIL-MAE       PIC 9(02).
                   10  ACTIVIDAD-MAE       PIC 9(01).
               05  DATOS-LIQ-MAE.
                   10  COD-12-MAE          PIC 9(01).
                   10  COD-13-MAE          PIC 9(03).
                   10  COD-16-MAE          PIC 9(01).
                   10  COD-17-MAE          PIC 9(01).
                   10  COD-18-MAE          PIC X(01).
                   10  COD-20-MAE          PIC 9(01).
                   10  COD-23-MAE          PIC X(01).
                   10  COD-24-MAE          PIC 9(01).
                   10  COD-25-MAE          PIC 9(01).
                   10  COD-26-MAE          PIC X(01).
                   10  COD-27-MAE          PIC X(01).
                   10  COD-28              PIC 9(02).
                   10  COD-30-MAE          PIC 9(01).
                   10  COD-31-MAE          PIC 9(01).
                   10  COD-34-MAE          PIC 9(01).
                   10  COD-36-MAE          PIC 9(01).
                   10  HS-SEC-MAE          PIC 9(02).
                   10  HS-UNIV-MAE         PIC 9(02).
                   10  TIT-SEC-MAE         PIC 9(01).
               05  DATOS-RETENC-MAE.
                   10  COD-914-MAE         PIC X(01).
                   10  COD-922-MAE         PIC 9(07).
                   10  COD-920-MAE         PIC 9(01).
                   10  COD-925-MAE         PIC 9(01).
                   10  FILLER              PIC 9(01).
                   10  FILLER              PIC 9(01).
                   10  COD-926-MAE         PIC 9(01).
                   10  COD-926-2           PIC 9(03)V99.
                   10  COD-927-MAE         PIC 9(01).
                   10  COD-927-2           PIC 9(03)V99.
                   10  COD-929-MAE         PIC X(01).
                   10  COD-934-MAE         PIC 9(01).
                   10  COD-935-MAE         PIC 9(01).
                   10  COD-951-MAE         PIC 9(01).
                   10  COD-955-MAE         PIC 9(01).
                   10  COD-960-MAE         PIC 9(01).
                   10  COD-963-MAE         PIC 9(01).
                   10  COD-968-MAE.
                       15 INDICADOR-968-MAE PIC 9(01).
                       15 CODIGO-968-MAE    PIC 9(02).
                   10  COD-973-MAE         PIC 9(01).
                   10  COD-977-MAE         PIC 9(01).
                   10  COD-983-MAE         PIC 9(01).
                   10  COD-990-MAE         PIC 9(05)V99.
                   10  COD-991-MAE         PIC 9(05)V99.
                   10  COD-995-MAE         PIC 9(01).
                   10  COD-997-MAE         PIC 9(01).
                   10  COD-986-MAE         PIC 9(01).
                   10  COD-987-MAE         PIC 9(01).
                   10  COD-988-MAE         PIC 9(01).
                   10  COD-992-MAE         PIC 9(01).
                   10  COD-982-MAE         PIC 9(01).
                   10  COD-941-MAE         PIC 9(01).
                   10  COD-980-MAE         PIC 9(01).
                   10  COD-943-MAE         PIC 9(01).
                   10  COD-945-MAE         PIC 9(01).
                   10  COD-947-MAE         PIC 9(01).
                   10  COD-936-MAE         PIC 9(01).
                   10  COD-918-MAE         PIC X(01).
               05  FILLER                  PIC X(02).
               05  ESTADO-REG-MAE          PIC 9(01).
               05  FECHA-BAJA-MAE.
                   10 DIA-BAJA-MAE         PIC 9(02).
                   10 MES-BAJA-MAE         PIC 9(02).
                   10 ANIO-BAJA-MAE        PIC 9(02).
               05  MOTIVO-BAJA-MAE         PIC X(01).

       FD  salida
           LABEL RECORDS ARE STANDARD.
       01  salida-RECORD.
           03  CUIT-SAL           pic 9(11).
           03  c1                 pic X.
           03  ORGANISMO-SAL      pic X(20).
           03  c2                 pic x.
           03  legajo-sal         pic 9(07).
           03  C3                 PIC X.
           03  apellido-sal       pic x(30).
           03  C4                 PIC X.
           03  cuil-sal           pic 9(11).
           03  C5                 PIC X.
           03  REMUNERACION-SAL   pic 9(09)V99.
           03  C6                 PIC X.
           03  ASIGNACION-SAL     pic 9(09)V99.
           03  C7                 PIC X.
           03  HSEXTRAS-SAL       pic 9(09)V99.
           03  C8                 PIC X.
           03  SAC-SAL            pic 9(09)V99.
           03  C9                 PIC X.
           03  REMUNERATIVO-SAL   pic 9(09)V99.
           03  C10                pic X.
           03  CPREVISION-SAL     pic 9(09)V99.
           03  C11                PIC X.
           03  CSS-SAL            pic 9(09)V99.
           03  C12                PIC X.
           03  GREMIO-SAL         pic 9(09)V99.
           03  C13                PIC X.
           03  ISPRO-SAL          pic 9(09)V99.
           03  C14                PIC X.

       FD  detalle
           LABEL RECORDS ARE STANDARD.
       01  detalle-record.
           05  CUIT-per             pic 9(11).
           05  fi00                 pic x.
           05  ORGANISMO-DET        pic x(30).
           05  fi41                pic x.
           05  ano-det             pic 9(04).
           05  fi27                pic x.
           05  mes-det             pic 9(02).
           05  fi28                pic x.
           05  anexo-det           pic 9(02).
           05  fi29                pic x.
           05  agrup-det           pic 9(02).
           05  fi30                pic x.
           05  categ-det           pic 9(03).
           05  fi31                pic x.
           05  clase-det           pic 9(03).
           05  fi32                pic x.
           05  item-det            pic 9(02).
           05  fi33                pic x.
           05  13mae-det           pic 9(03).
           05  fi34                pic x.
           05  23mae-det           pic 9.
           05  fi55                pic x.
           05  27mae-det           pic 9.
           05  fi35                pic x.
           05  planta-det          pic 9(01).
           05  fi36                pic x.
           05  localidad-det       PIC X(15).
           05  fi42                pic x.
           05  DESTINO-det         PIC 9(04).
           05  fi43                pic x.
           05  CUIL-det             PIC 9(11).
           05  fi44                pic x.
           05  apellido-det        PIC X(30).
           05  fi37                pic x.
           05  legajo-det          pic 9(07).
           05  fi38                pic x.
           05  codigo-det          pic 9(03).
           05  fi39                pic x.
           05  descrip-det         pic x(30).
           05  fi40                pic x.
           05  importe-det         pic x(011).


       working-storage section.
       77  I                        pic 99.

       01  CLAVE-TAB.
           03  ANEXO-TAB            PIC 9(2).
           03  ITEM-TAB             PIC 9(2).
           03  AGRUP-TAB            PIC 9(2).
       01  CLAVE-AGRUP.
           03  A-TAB                PIC 9(1).
           03  AG-TAB               PIC 9(2).
           03  RESTO                PIC 9(3).

       01  nombre-liqmes.
           03  FILLER            PIC  X(33)
                 VALUE "S:\LDDAT\PRUEBAS LIQUIDACION\liq-".
           03  ANO-NOM-LIQ       PIC  9(04) VALUE zeros.
           03  FILLER            PIC  X(01) VALUE "-".
           03  MES-NOM-LIQ       PIC  9(02) VALUE zeros.
           03  FILLER            PIC  X(04) VALUE ".txt".

       01  VARIABLES.
           03  AGENTES             PIC 9(06)    VALUE ZEROS.
           03  ANIOS               PIC 9(06)    VALUE ZEROS.
           03  TANIOS              PIC 9(06)    VALUE ZEROS.
           03  REMUN               PIC 9(09)V99 VALUE ZEROS.
           03  SALARIO             PIC 9(09)V99 VALUE ZEROS.
           03  LIQUIDO             PIC 9(09)V99 VALUE ZEROS.
           03  RETLEY              PIC 9(09)V99 VALUE ZEROS.
           03  RETSINLEY           PIC 9(09)V99 VALUE ZEROS.
           03  COSTO-LABORAL       PIC 9(09)V99 VALUE ZEROS.
           03  SALARIO-BRUTO       PIC 9(09)V99 VALUE ZEROS.
           03  PROMEDIO            PIC 9(05)V99 VALUE ZEROS.
           03  PATCSS              PIC 9(09)V99 VALUE ZEROS.
           03  PATCPS              PIC 9(09)V99 VALUE ZEROS.
           03  PATISPRO            PIC 9(09)V99 VALUE ZEROS.
           03  PATRIESGO           PIC 9(09)V99 VALUE ZEROS.
           03  S-APORTES           PIC 9(09)V99 VALUE ZEROS.
           03  C-APORTES           PIC 9(09)V99 VALUE ZEROS.
           03  REMUNERACION        PIC 9(09)V99 VALUE ZEROS.
           03  ASIGNACION          PIC 9(09)V99 VALUE ZEROS.
           03  RETENCION           PIC 9(09)V99 VALUE ZEROS.
           03  HSEXTRAS            PIC 9(09)V99 VALUE ZEROS.
           03  SAC                 PIC 9(09)V99 VALUE ZEROS.
           03  CPREVISION          PIC 9(09)V99 VALUE ZEROS.
           03  CSS                 PIC 9(09)V99 VALUE ZEROS.
           03  GREMIO              PIC 9(09)V99 VALUE ZEROS.
           03  ISPRO               PIC 9(09)V99 VALUE ZEROS.
           03  REMUNERATIVO        PIC 9(09)V99 VALUE ZEROS.
           03  DESCUENTOS        PIC 9(09)V99 VALUE ZEROS.
.
       PROCEDURE DIVISION.
       CATE.
           OPEN OUTPUT SALIDA detalle.
       ABRO.
           OPEN INPUT LIQMES MAESTRO.

       LEO.
           INITIALIZE SALIDA-RECORD.
           INITIALIZE VARIABLES.
           READ LIQMES NEXT AT END
                        CLOSE LIQMES
                        CLOSE MAESTRO
                        CLOSE SALIDA
                        CLOSE detalle
                        STOP RUN.
           move legajo-liq to legajo-mae.
           read maestro.

           IF ESTADO-REG-MAE = 1
               GO LEO
           ELSE
           IF ESTADO-REG-MAE = 0 OR = 5 OR = 7 OR = 4
              CONTINUE
           END-IF.

       CODIGO.
           INITIALIZE VARIABLES SALIDA-RECORD.

           PERFORM VEO-SUELDO THRU F-VEOS VARYING I FROM 1 BY 1 UNTIL
                  I > 40

           COMPUTE LIQUIDO = SALARIO-BRUTO - RETENCION.

           PERFORM VEO-REMU THRU F-VEO-REMU VARYING I FROM 1 BY 1 UNTIL
                  I > 40

           COMPUTE REMUNERATIVO = (C-APORTES - DESCUENTOS - ASIGNACION
            ) * 0,06833333.


      ***** CARGO EL CUIT DEL ORGANISMO *****

      ***** GOBERNACION   // FISCALIA
           if anexo-liq = 01 and item-liq not = 30
               move 30715443577 to CUIT-PER
               move "Gobernacion" to organismo-det
           ELSE
               IF ANEXO-LIQ = 01
                   move 30715322745 to CUIT-PER
                   move "Fiscalia de Estado" to organismo-det
               END-IF

           end-if.


      ***** TRIBUNAL DE CUENTAS
           if anexo-liq = 03
               move 30673674433 to CUIT-PER
               move "Tribunal de Cuentas" to organismo-det
           end-if.

      ***** DESARROLLO SOCIAL
           if anexo-liq = 07
               move 30711853738 to CUIT-PER
                  move "Min. Desarrollo Social" to organismo-det
           end-if.

      ***** MSGG         // CASA SANTA CRUZ
           if anexo-liq = 08 AND ITEM-LIQ NOT = 13
               move 30673657687 to CUIT-PER
               move "Casa de Sta Cruz" to organismo-det
           ELSE
              IF ANEXO-LIQ = 08
                    move 30707677879 to CUIT-PER
                    move "MSGG" to organismo-det
              END-IF

           end-if.

      ***** TRIBUNAL DISCIPLINARIO
           if anexo-liq = 11
               move 30673656524 to CUIT-PER
               move "Tribunal Disciplinario" to organismo-det
           end-if.


      ***** MINISTERIO DE GOBIERNO
           if anexo-liq = 04
               move 30673656699 to CUIT-PER
               move "Min. de Gobierno" to organismo-det
           end-if.

      ***** CONSEJO AGRARIO (CAP) // MEFI
           if anexo-liq = 05 AND (ITEM-LIQ = 18 OR = 19)
               move 30656949836 to CUIT-PER
               move "Consejo Agrario" to organismo-det
           ELSE
               IF ANEXO-LIQ = 05
                   move 30673639603 to CUIT-PER
                   move "Min. de Economia" to organismo-det
               END-IF
           end-if.

      ***** MIN PRODUCCION
           if anexo-liq = 12
               move 30710660839 to CUIT-PER
               move "Min. Produccion" to organismo-det
           end-if.

      ***** MIN JEFATURA GABINETE
           if anexo-liq = 13
               move 30716837250 to CUIT-PER
               move "Jefatura de Gabinete" to organismo-det
           end-if.

      ***** MIN SALUD
           if anexo-liq = 14
               move 30711796602 to CUIT-PER
               move "Ministerio de Salud" to organismo-det
           end-if.

      ***** VIALIDAD
           if anexo-liq = 21
               move 30654106378 to CUIT-PER
               move "Vialidad Provincial" to organismo-det
           end-if.

      ***** IDUV
           if anexo-liq = 24
               move 30653141994 to CUIT-PER
               move "IDUV" to organismo-det
           end-if.

      ***** UNEPOSC
           if anexo-liq = 30
               move 30652487080 to CUIT-PER
               move "UNEPOSC" to organismo-det
           end-if.


      ***** MIN TRABAJO
           if anexo-liq = 16
               move 30716110326 to CUIT-PER
               move "Min. de Trabajo" to organismo-det
           end-if.

      ***** POLICIA
           if anexo-liq = 17 AND ITEM-LIQ = 08
               move 30656997806 to CUIT-PER
               move "Policia Provincial" to organismo-det
           ELSE

      ***** SERVICIO  PENITENCIARIO
               if anexo-liq = 17 AND ITEM-LIQ = 31
                    move 30716401959 to CUIT-PER
                    move "Servicio Penitenciario" to organismo-det
               ELSE
                   IF ANEXO-LIQ = 17
                       move 33716718439 to CUIT-PER
                       move "Min. de Seguridad" to organismo-det
                   END-IF
               end-if
           end-if.


      ***** MIEI (IGUALDAD)
           if anexo-liq = 18
               move 30717665704 to CUIT-PER
               move "Min. de Igualdad" to organismo-det
           end-if.

      ***** AMA
           if anexo-liq = 45
               move 30717554287 to CUIT-PER
               move "A.M.A." to organismo-det
           end-if.

      ***** CYT
           if anexo-liq = 62
               move 30717532879 to CUIT-PER
               move "Ciencia y Tecnologia" to organismo-det
           end-if.






       SIG-CATE.
           MOVE ";" TO C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 C12 C13 C14.
           MOVE ORGANISMO-det  TO ORGANISMO-SAL.
           MOVE CUIT-PER       TO CUIT-SAL.
           MOVE LEGAJO-LIQ     TO LEGAJO-SAL.
           MOVE APEL-NOM-MAE   TO APELLIDO-SAL.
           MOVE NRO-CIPF-MAE   TO CUIL-SAL.
           MOVE REMUNERACION   TO REMUNERACION-SAL.
           MOVE ASIGNACION     TO ASIGNACION-SAL.
           MOVE HSEXTRAS       TO HSEXTRAS-SAL.
           MOVE SAC            TO SAC-SAL.
           MOVE CPREVISION     TO CPREVISION-SAL.
           MOVE CSS            TO CSS-SAL.
           MOVE GREMIO         TO GREMIO-SAL.
           MOVE ISPRO          TO ISPRO-SAL.
           MOVE REMUNERATIVO   TO REMUNERATIVO-SAL.




           WRITE SALIDA-RECORD.
           GO LEO.

       F-VEO.
           EXIT.

       VEO-SUELDO.
           IF CODIGO-LIQ(I) < 200
              ADD IMPORTE-LIQ(I) TO ASIGNACION
           ELSE
              IF CODIGO-LIQ(I) = 248
              ADD IMPORTE-LIQ(I) TO HSEXTRAS
              ELSE
              IF CODIGO-LIQ(I) = 214 OR = 314 OR = 414
                 OR = 514 OR = 614 OR = 714 OR = 814
                 ADD IMPORTE-LIQ(I) TO SAC
              ELSE
              IF CODIGO-LIQ(I) = 901
                   ADD IMPORTE-LIQ(I) TO CPREVISION
               ELSE
               IF CODIGO-LIQ(I) = 911
                   ADD IMPORTE-LIQ(I) TO CSS
               ELSE
               IF CODIGO-LIQ(I) = 921
                   ADD IMPORTE-LIQ(I) TO ISPRO
               ELSE
               IF CODIGO-LIQ(I) = 951 OR = 955 OR = 960
                          OR = 980 OR = 983 OR = 990 OR = 996 OR = 997
                   ADD IMPORTE-LIQ(I) TO GREMIO
               ELSE
               IF CODIGO-LIQ(I) > 200 AND CODIGO-LIQ(I) < 900
                   ADD IMPORTE-LIQ(I) TO REMUNERACION
           END-IF.
       F-VEOS.
           EXIT.

       VEO-REMU.
           IF CODIGO-LIQ(I) = 240 OR = 241 OR = 242 OR = 243 OR =
                  245 OR = 292 OR = 293 OR = 294 OR =
                  291 OR = 299 OR = 458 OR = 248 OR =
                  340 OR = 341 OR = 342 OR = 345 OR = 346 OR =
                  391 OR = 399 OR = 832 OR = 833 OR =
                  430 OR = 435 OR = 440 OR = 442 OR = 443 OR =
                  445 OR = 446 OR = 491 OR = 499 OR = 543 OR =
                  635 OR = 640 OR = 641 OR = 642 OR = 643 OR = 645
                  OR = 646 OR = 649 OR = 691 OR = 699 OR =
                  735 OR = 740 OR = 741 OR = 742 OR = 743 OR = 745 OR =
                  746 OR = 791 OR = 799 OR = 344 OR = 444 OR =
                  644 OR = 744 OR = 292 OR = 392 OR = 492 OR = 692 OR =
                  792 or = 474  OR = 548 OR = 285
                  OR = 276 OR = 277 OR = 278  or = 648
                  OR = 540 OR = 541 OR = 281 OR = 681 OR = 298 OR =
                  221 OR = 432 OR = 433 OR = 832 OR = 833
                  OR = 830 OR = 840 OR = 842 OR = 858 OR = 254 OR =
                  844 or = 259 OR = 293 OR = 294 OR = 759 OR = 834
                  OR = 434
                    ADD IMPORTE-LIQ(I) TO S-APORTES

           ELSE

                    ADD IMPORTE-LIQ(I) TO C-APORTES

           END-IF.

           IF CODIGO-LIQ(I) > 900
               ADD IMPORTE-LIQ(I) TO DESCUENTOS
           END-IF.



       F-VEO-REMU.
           EXIT.

       FINALIZA.
           CLOSE SALIDA.


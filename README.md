# OscDataAnalysis

Este repositorio contiene codigo fuente que permite analizar datos capturados por un osciloscopio en experimentos para detección de 
partículas.<p>

Especificamente, está diseñado para procesar datos de radiación emitida por una fuente radioactiva de sodio-22 (na22), detectada por un mini TGC (Thin gap chamber) y muestreado por un osciloscopio.<p>

El software incluye funciones para seleccionar datos, realizar calculos 
y graficar los resultados.<p>

### Prerequisitos

El código está escrito en lenguaje Python 2.7 32bits y usa las librerias de ROOT (framework para trabajar datos de física de particulas en CERN). Está diseñado para ser compilado y ejecutado en sistemas operativos Windows y Linux.<p> 
El código fue desarrollaado y probado en windows 10 con las siguientes dependencias:<p>
- Python 2.7 (libs: tk, numpy, time, tqdm)<br>
- ROOT v5.34/38 <br>


## Ejecución

Para ejecutar el programa, las librerias de ROOT debe estar incluidas correctamente en las rutas del sistema.
El programa principal es "na22-exp-py".

## Autor
* **Jairo Gonzáez** - jairo.gonzalez.13@sansano.usm.cl

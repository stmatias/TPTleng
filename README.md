# Teoría de Lenguajes
## Trabajo Práctico: Generador de JSON de ejemplo

### Instrucciones para correr el TP
#### Dependencias
Se debe crear una carpeta con nombre **/ply** en la raíz del proyecto incluyendo los archivos **lex.py** y **yacc&#46;py** que pueden obtenerse de este repositorio: https://github.com/dabeaz/ply.
#### Tests
En la carpeta **/tests** se encuentran los archivos de test con structs de GO a parsear. Algunos archivos contienen la palabra **ERROR** en su nombre, indicando que ese caso de test debe devolver un error capturado por el programa.
#### Ejecución
El programa acepta los siguiente argumentos:
|    |Parámetro    		|Comportamiento						   |
|----|------------------|--------------------------------------|
|-f  |Ruta del archivo  |Parsea el contenido del archivo       |
|-t  |Cadena a procesar |Parsea la cadena pasada por parámetro |
|-rt |					|Corre los tests sin error			   |
|-rte|					|Corre los tests con error			   |
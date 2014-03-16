Padrón  Contribuyentes AFIP
===========================

Este proyecto crea OLAPNW con los datos del KDD CUP:
http://www.kaggle.com/c/kdd-cup-2013-author-paper-identification-challenge/data

Descripción de la red
---------------------

- La red esta estructurada de tal forma que cada haplotipo (nodo) es uno de los
  autores de la tabla ``author``.
- Los ``hap_id`` son los *id* de la tabla ``author``
- La red conecta solo los authores que tienen papers en comun, y el peso de los
  arcos es la cantidad de papers que desarrollaron en comun.
- Los hechos son un resumen de las demas tablas.
- Las tablas ``validpaper``, ``traindeleted`` y ``trainconfirmed`` se convierten
  en bools


Salida de describe
------------------

.. code-block:: python

Instrucciones
-------------

#. Descargar el dump de la db de la pagina de la competencia.
#. Restaurar la base en un postgres
#. Correr el ETL pasandole como argumetno la coneccion al postgres que se
   restauró

Archivos
--------

    - ``papers_etl.py`` ETL que genera la red basada en el db generada.
    - ``papers.yxf.zip`` NW-OLAP en formato YXF (Yatel XML Format)
      comprimida.


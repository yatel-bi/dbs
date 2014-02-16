Padron  Contribuyentes AFIP
===========================

Este proyecto crea OLAPNW con los datos del padron electoral del AFIP.

Descripcion de la red
---------------------

La red esta estructurada de tal forma que cada haplotipo (nodo) es uno de los
posibles combinaciones de los impuestos IVA y Ganancias mas un contador con
la cantidad de ocurrencias de esa combinación.

(Los valores posibles de cada uno de estos impuestos se listan en
http://www.sistemasagiles.com.ar/trac/wiki/PadronContribuyentesAFIP#M%C3%A9todos)
Los arcos conectan cada haplotipos con los demas y el peso esta dado por la
distancia de hamming de cada nodo
Los hechos, por otra parte, son una copia de la base datos original enlazados
a los haplotipos.

El haplotype_id es una string de 5 caracteres; los 2 primeros son el estado del
impuesto iva y los dós ultimos del impuesto a las ganancias. El intermedio es
siempre un guión bajo

Description
-----------


Archivos
--------

    - ``lib/padron.py``: Conector del padron electoral parte del proyecto
      PyAfipWs_
      Todos los datos son publicos brindados por el AFIP. (Un poco modificada
      del original para que los archivos temporales se guarden en ``_temp``
    - ``lib/utils.py`` usado por padron.py y tambien parte de PyAfipWs_.
    - ``padronafip_etl.py`` ETL que genera la red basada en el padron utilizando
      ``lib/padron.py``
    - ``padron_afip.yjf`` NW-OLAP generada con el etl. (CONGELADA AL 2014-02-15)


.. _ PyAfipWs: http://www.sistemasagiles.com.ar/trac/wiki/PyAfipWs


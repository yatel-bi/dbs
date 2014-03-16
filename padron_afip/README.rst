Padrón  Contribuyentes AFIP
===========================

Este proyecto crea OLAPNW con los datos del padrón electoral del AFIP.

Descripción de la red
---------------------

La red esta estructurada de tal forma que cada haplotipo (nodo) es uno de los
posibles combinaciones de los impuestos IVA y Ganancias.

(Los valores posibles de cada uno de estos impuestos se listan en
http://www.sistemasagiles.com.ar/trac/wiki/PadronContribuyentesAFIP#M%C3%A9todos)

La red es totalmente conectada y el peso de cada arco esta dado por la distancia
de Hamming de cada nodo

Los hechos, por otra parte, son una copia de la base datos original enlazados
a los haplotipos.

El **hap_id** es una string dividido a por un guion bajo ``_``:
    - Primer mitad: estado del impuesto IVA.
    - Segunda mitad: Estado del impuesto a las ganancias.



Salida de describe
------------------

.. code-block:: python

    {
        'edge_attributes': {u'max_nodes': 2, u'weight': <type 'float'>},
        'fact_attributes': {u'actividad_monotributo': <type 'str'>,
                            u'cuit': <type 'long'>,
                            u'denominacion': <type 'str'>,
                            u'empleador': <type 'str'>,
                            u'hap_id': <type 'str'>,
                            u'imp_ganancias': <type 'str'>,
                            u'imp_iva': <type 'str'>,
                            u'integrante_soc': <type 'str'>,
                            u'monotributo': <type 'str'>},
        'haplotype_attributes': {u'hap_id': <type 'str'>,
                                 u'imp_ganancias': <type 'str'>,
                                 u'imp_iva': <type 'str'>},
        'mode': 'r',
        'size': {u'edges': 276, u'facts': 4105258, u'haplotypes': 24}
    }


Archivos
--------

    - ``lib/padron.py``: Conector del padrón electoral parte del proyecto
      PyAfipWs_. Todos los datos son públicos brindados por el AFIP.
    - ``lib/utils.py`` usado por padron.py y tambien parte de PyAfipWs_.
    - ``padronafip_etl.py`` ETL que genera la red basada en el padrón utilizando
      ``lib/padron.py``
    - ``padron_afip.yxf.zip`` NW-OLAP en formato YXF (Yatel XML Format)
      comprimida. (CONGELADA AL 2014-02-16)



.. _ PyAfipWs: http://www.sistemasagiles.com.ar/trac/wiki/PyAfipWs


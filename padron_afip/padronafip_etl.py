#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''auto created template for create your custom etl for yatel'''


#===============================================================================
# IMPORTS
#===============================================================================

import sys, os

from yatel import etl, dom, weight

import sqlalchemy as sa


#===============================================================================
# CONSTANTS
#===============================================================================

PATH = os.path.abspath(os.path.dirname(__file__))
TEMP_DIR = os.path.join(PATH, "_temp")
FILENAME = os.path.join(TEMP_DIR, "padron.txt")
DBNAME = os.path.join(TEMP_DIR, "padron.db")


#===============================================================================
# PATCH PATH
#===============================================================================

sys.path.insert(0, PATH)


#===============================================================================
# CONFIG
#===============================================================================

from lib import padron
padron.PadronAFIP.InstallDir = TEMP_DIR

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)


#===============================================================================
# PUT YOUT ETLs HERE
#===============================================================================

class ETL(etl.BaseETL):

    def setup(self):
        p = padron.PadronAFIP()
        if p.Descargar(filename=FILENAME) == 200:
            if not os.path.exists(DBNAME):
                with open(DBNAME, "w") as fp:
                    fp.write("trash")
            p.Procesar(filename=FILENAME)
        self.src_engine = sa.create_engine("sqlite:///" + DBNAME)
        self.src_meta = sa.MetaData(self.src_engine)
        self.src_meta.reflect()
        self.table = self.src_meta.tables["padron"]

    def haplotype_gen(self):
        self.haps = []
        query = sa.sql.select([
            self.table.c[u'imp_ganancias'], self.table.c[u'imp_iva']
        ]).distinct()
        for row in self.src_engine.execute(query):
            hap_id = u"{}_{}".format(row.imp_iva, row.imp_ganancias)
            hap = dom.Haplotype(hap_id, **dict(row))
            self.haps.append(hap)
            yield hap

    def edge_gen(self):
        for haps, wgh in weight.weights("ham", self.haps):
            yield dom.Edge(wgh, [h.hap_id for h in haps])

    def fact_gen(self):
        query = sa.sql.select([self.table])
        for row in self.src_engine.execute(query):
            hap_id = u"{}_{}".format(row.imp_iva, row.imp_ganancias)
            yield dom.Fact(hap_id, **dict(row))


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

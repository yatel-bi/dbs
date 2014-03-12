#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''auto created template for create your custom etl for yatel'''


#===============================================================================
# IMPORTS
#===============================================================================

import sys, os, itertools

from yatel import etl, dom, weight

import sqlalchemy as sa
from sqlalchemy import sql
from sqlalchemy import func


#===============================================================================
# CONSTANTS
#===============================================================================

PATH = os.path.abspath(os.path.dirname(__file__))
TEMP_DIR = os.path.join(PATH, "_temp")


#===============================================================================
# PATCH PATH
#===============================================================================

sys.path.insert(0, PATH)


#===============================================================================
# CONFIG
#===============================================================================

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)


#===============================================================================
# PUT YOUT ETLs HERE
#===============================================================================

class ETL(etl.BaseETL):
    """migrate all data from paper stores in postgres to nw-olap.

    To create the source db you need to download and restore this db

    """

    def setup(self, pgconn):
        self.src_engine = sa.create_engine(pgconn)
        self.src_meta = sa.MetaData(self.src_engine)
        self.src_meta.reflect()

    def haplotype_gen(self):
        self.haps = []
        query = sql.select([
            self.src_meta.tables["author"]
        ])
        for row in self.src_engine.execute(query):
            hap = dom.Haplotype(
                hap_id=row["id"], name=row["name"],
                affiliation=row["affiliation"]
            )
            self.haps.append(hap.hap_id)
            yield hap
            if len(self.haps) == 100:
                break

    def edge_gen(self):
        paper = self.src_meta.tables["paper"]
        paperauthor = self.src_meta.tables["paperauthor"]

        for hap_id0, hap_id1 in itertools.combinations(self.haps, 2):
                query = sql.select(
                    [func.count(paper.c.id)]
                ).select_from(
                    paper.join(paperauthor, paper.c.id == paperauthor.c.paperid)
                ).where(
                    sql.or_(
                        paperauthor.c.authorid == hap_id0,
                        paperauthor.c.authorid == hap_id1
                    )
                ).distinct()
                count = self.src_engine.execute(query).fetchone()[0]
                if count:
                    yield dom.Edge(count, (hap_id0, hap_id1))

    def fact_gen(self):
        return ()
            #~ for hap_id in self.haps:
                #~ data = {}
#~
                #~ paperauthor_query = sql.select([
                    #~ self.src_meta.tables["paperauthor"]
                #~ ]).where(
                    #~ self.src_meta.tables["paperauthor"].c["authorid"]==hap_id
                #~ ).distinct()
#~
                #~ for pa_row in self.src_engine.execute(paperauthor_query):
                    #~ data["paperauthor_name"] = row["Name"]
                    #~ data["paperauthor_affiliation"] = row["Affiliation"]
#~
                    #~ paper = sql.select(
                        #~ self.src_meta.tables["paper"]
                    #~ ).where(
                        #~ self.src_meta.tables["paper"].c["id"]==row["paperID"]
                    #~ )


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
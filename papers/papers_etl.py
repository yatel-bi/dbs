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

    def edge_gen(self):
        paper = self.src_meta.tables["paper"]
        paperauthor = self.src_meta.tables["paperauthor"]

        def _papers_ids(authorid):
            query = sql.select(
                [paperauthor.c.paperid]
            ).where(
                paperauthor.c.authorid == authorid,
            ).distinct()
            return frozenset(row[0] for row in self.src_engine.execute(query))

        paper_buff = {}
        for hap_id0, hap_id1 in itertools.combinations(self.haps, 2):
            if hap_id0 not in paper_buff:
                paper_buff[hap_id0] = _papers_ids(hap_id0)
            if hap_id1 not in paper_buff:
                paper_buff[hap_id1] = _papers_ids(hap_id1)
            papers0 = paper_buff[hap_id0]
            papers1 = paper_buff[hap_id1]
            count = len(papers0.intersection(papers1))
            if count:
                yield dom.Edge(count, (hap_id0, hap_id1))

    def fact_gen(self):
        for hap_id in self.haps:
            data = {}
#~
            paperauthor_query = sql.select([
                self.src_meta.tables["paperauthor"]
            ]).where(
                self.src_meta.tables["paperauthor"].c["authorid"]==hap_id
            ).distinct()

            for pa_row in self.src_engine.execute(paperauthor_query):

                data["paperauthor_name"] = pa_row["name"]
                data["paperauthor_affiliation"] = pa_row["affiliation"]

                paper_row = self.src_engine.execute(sql.select([
                    self.src_meta.tables["paper"]
                ]).where(
                    self.src_meta.tables["paper"].c["id"]==pa_row["paperid"]
                )).fetchall()

                if not paper_row:
                    continue
                paper_row = paper_row[0]

                data["keyword"] = paper_row["keyword"]
                data["title"] = paper_row["title"]
                data["year"] = paper_row["year"]

                if paper_row["journalid"]:
                    journal_row = self.src_engine.execute(sql.select([
                        self.src_meta.tables["journal"]
                    ]).where(
                        self.src_meta.tables["journal"].c["id"]==paper_row["journalid"]
                    )).fetchall()

                    if journal_row:
                        data["journal_shortname"] = journal_row[0]["shortname"]
                        data["journal_fullname"] = journal_row[0]["fullname"]
                        data["journal_homepage"] = journal_row[0]["homepage"]

                if paper_row["conferenceid"]:
                    conference_row = self.src_engine.execute(sql.select([
                        self.src_meta.tables["conference"]
                    ]).where(
                        self.src_meta.tables["conference"].c["id"]==paper_row["conferenceid"]
                    )).fetchall()

                    if conference_row:
                        data["conference_shortname"] = conference_row[0]["shortname"]
                        data["conference_fullname"] = conference_row[0]["fullname"]
                        data["conference_homepage"] = conference_row[0]["homepage"]

                for flag in ["validpaper", "traindeleted", "trainconfirmed"]:
                    flag_row = self.src_engine.execute(sql.select([
                            self.src_meta.tables[flag]
                        ]).where(
                            (self.src_meta.tables[flag].c["paperid"]==paper_row["id"]) &
                            (self.src_meta.tables[flag].c["authorid"]==hap_id)
                        )).fetchall()
                    data[flag] = bool(flag_row)

                yield dom.Fact(hap_id, **data)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)

#!/usr/bin/python3
import argparse
import os
import sys
import json
import sys

# these are basic DERIVA APIs to access raw ERMrest query capabilities
from deriva.core import ErmrestCatalog, urlquote, DEFAULT_HEADERS, DEFAULT_SESSION_CONFIG
from deriva.core.datapath import Min, Max, Cnt, CntD, Avg, Sum, Bin, ArrayD


def main():
    p = argparse.ArgumentParser()
    p.add_argument('-o', '--output', required=True)
    args = p.parse_args()

    # get some params from environment
    servername = os.getenv('DERIVA_SERVERNAME', 'app.nih-cfde.org')
    catalogid = os.getenv('DERIVA_CATALOGID', '1')

    # bind to ermrest service
    # not using credentials, so only works for public catalogs...
    catalog = ErmrestCatalog('https', servername, catalogid)

    # get datapath query builders
    # and build a datapath query by pulling things from model and connecting them
    builder = catalog.getPathBuilder()
    dcc = builder.CFDE.dcc

    combined_fact = builder.CFDE.combined_fact
    core_fact = builder.CFDE.core_fact
    pubchem_fact = builder.CFDE.pubchem_fact
    protein_fact = builder.CFDE.protein_fact
    gene_fact = builder.CFDE.gene_fact

    # vocab_tables[cname] --> datapath tname
    vocab_tables = {
        # core_fact arrays
        "phenotypes": 'phenotype',
        "diseases": 'disease',
        "sexes": 'sex',
        "races": 'race',
        "ethnicities": 'ethnicity',
        "ncbi_taxons": 'ncbi_taxonomy',
        "anatomies": 'anatomy',
        "assay_types": 'assay_type',
        "analysis_types": 'analysis_type',
        "file_formats": 'file_format',
        "compression_formats": 'file_format',
        "data_types": 'data_type',

        # pubchem_fact arrays
        "substances": 'substance',
        "compounds": 'compound',

        # protein_fact arrays
        "proteins": 'protein',

        # gene_fact arrays
        "genes": 'gene',
    }

    # rewrite tname to table iff table and cname exists in catalog
    # for backward compatibility...
    # vocab_tables[cname] -> datapath table
    vocab_tables = {
        cname: builder.CFDE.tables[tname]
        for cname, tname in vocab_tables.items()
        if tname in builder.CFDE.tables and (
                (cname in core_fact.columns)
                or (cname in pubchem_fact.columns)
                or (cname in protein_fact.columns)
                or (cname in gene_fact.columns)
        )
    }

    # prefetch vocabs so we can convert numeric ID to other info
    # vocab_terms[tname][nid] --> term row
    vocab_terms = {
        table._name: {
            row["nid"]: row
            for row in table.path.entities().fetch()
        }
        # compute set of distinct tables to fetch
        for table in set(vocab_tables.values()) | {builder.CFDE.dcc,}
    }

    # accumulator for all stats
    # vocab_stats[tname][term id][dcc abbrev] -> { "num_files": N, ... }
    vocab_stats = {}

    # need to join fact tables to get dcc info plus other concepts
    path = combined_fact.alias('s').path
    path = path.link(core_fact.alias('cf'), on=(path.s.core_fact == core_fact.nid))
    path = path.link(pubchem_fact.alias('pcf'), on=(path.s.pubchem_fact == pubchem_fact.nid))
    path = path.link(protein_fact.alias('prf'), on=(path.s.protein_fact == protein_fact.nid))
    path = path.link(gene_fact.alias('gf'), on=(path.s.gene_fact == gene_fact.nid))
    path.context = path.s
    path = path.attributes(*(
        [
            combined_fact.num_collections,
            combined_fact.num_files,
            combined_fact.num_biosamples,
            combined_fact.num_subjects,
            path.cf.dccs,
        ] + [
            path.cf.columns[cname]
            for cname in vocab_tables
            if cname in core_fact.columns
        ] + [
            path.pcf.columns[cname]
            for cname in vocab_tables
            if cname in pubchem_fact.columns
        ] + [
            path.prf.columns[cname]
            for cname in vocab_tables
            if cname in protein_fact.columns
        ] + [
            path.gf.columns[cname]
            for cname in vocab_tables
            if cname in gene_fact.columns
        ]
    ))

    for row in path.fetch(limit=None):
        dcc_nids = row['dccs']
        if len(dcc_nids) > 1:
            # skip this, must be a collection from _the future_?
            continue
        elif len(dcc_nids) == 0:
            # skip this, cannot attribute it to any dcc?!
            continue

        dcc_key = vocab_terms['dcc'][int(dcc_nids[0])]['dcc_abbreviation']
        for nid_array_cname, vocab_table in vocab_tables.items():
            tname = vocab_table._name
            nid_array = row[nid_array_cname]
            for nid in nid_array:
                try:
                    if isinstance(nid, str):
                        nid = json.loads(nid) # compat shim
                    if isinstance(nid, list):
                        nid = nid[0] # found [term, association_type] pair
                    tid = vocab_terms[tname][nid]['id']
                    label = vocab_terms[tname][nid]['name']
                except:
                    sys.stderr.write('%s\n' % (('BUG', nid_array_cname, tname, nid_array, nid),))
                    raise
                vocab_stats.setdefault(tname, {}).setdefault(tid, {"_name": label}).setdefault(dcc_key, {})
                for cnt in {'num_collections', 'num_files', 'num_biosamples', 'num_subjects'}:
                    cnt_val = row[cnt] if row[cnt] is not None else 0
                    vocab_stats[tname][tid][dcc_key].setdefault(cnt, 0)
                    vocab_stats[tname][tid][dcc_key][cnt] += cnt_val

    # either load this somewhere else or just take a look and massage the data further...
    #print(json.dumps([ dcc['dcc_abbreviation'] for dcc in vocab_terms['dcc'].values() ]))
    print(json.dumps(vocab_stats, indent=2), file=args.output)

    return 0


if __name__ == '__main__':
    sys.exit(main())

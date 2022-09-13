# Generating Controlled Vocabulary from C2M2
The purpose of this repository is to create the data requested in this Help Desk inquiry: [https://cfde.atlassian.net/jira/servicedesk/projects/HELP/queues/custom/4/HELP-262](https://cfde.atlassian.net/jira/servicedesk/projects/HELP/queues/custom/4/HELP-262)

Relevant text:

We previously worked with Amanda Charbonneau to get information on tissue blocks that could be RUI registered, see https://hubmapconsortium.github.io/ccf-ui/rui/  

We also need Uberon terms, see Amanda’s earlier data compilation at 

https://docs.google.com/spreadsheets/d/1wkoN9fyUtVZWYnbK0S0AKJmiTS-yELCRKgkNqk870eA/edit?pli=1#gid=1729887084 

### Column Descriptions

- Column A: Row number starting from 1
- Column B named `format_type`: The identifier for each row, found in JSON. All options: `NCBI:txid10116`, `data:2044`, `DOID:9256`, `format:3547`, `OBI:0001271`, `UBERON:0002441`
- Column C named `label`: This comes from the `_name` field in the JSON. Examples: `cervicothoracic ganglion`, `nervous system`, `heart`
- Column D named `record_type`: The type of record, found in JSON. Examples: `data_type`, `disease`, `file_format`
- Columns E through M named by DCC: The number of biosamples from each DCC from `num_biosamples`

### Workflow

```
# create conda environment

conda env create -f environment.yml

# activate and install deriva

conda activate deriva

# run the C2M2 download etc. etc
make
```

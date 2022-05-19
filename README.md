# Generating Controlled Vocabulary from C2M2
The purpose of this repository is to create the data requested in this Help Desk inquiry: [https://cfde.atlassian.net/jira/servicedesk/projects/HELP/queues/custom/4/HELP-262](https://cfde.atlassian.net/jira/servicedesk/projects/HELP/queues/custom/4/HELP-262)

Relevant text:

We previously worked with Amanda Charbonneau to get information on tissue blocks that could be RUI registered, see https://hubmapconsortium.github.io/ccf-ui/rui/  

We also need Uberon terms, see Amanda’s earlier data compilation at 

https://docs.google.com/spreadsheets/d/1wkoN9fyUtVZWYnbK0S0AKJmiTS-yELCRKgkNqk870eA/edit?pli=1#gid=1729887084 

### Workflow

```
# create conda environment

conda create -n deriva -y python==3.9

# activate and install deriva

conda activate deriva
pip install deriva

# run the C2M2 script

python c2m2_cv_usage.py > out.txt

# remove top line of out.txt that prints all DCCs name

# run reformatting script to make csv

python display.py > table.csv

# install pandas, remove rows that contain all zeros

conda install pandas

python remove_zeros.py
```

# Generating Controlled Vocabulary from C2M2
This repository is to create the data requested in this Help Desk inquiry: [https://cfde.atlassian.net/jira/servicedesk/projects/HELP/queues/custom/4/HELP-262](https://cfde.atlassian.net/jira/servicedesk/projects/HELP/queues/custom/4/HELP-262)

Relevant text:

We previously worked with Amanda Charbonneau to get information on tissue blocks that could be RUI registered, see https://hubmapconsortium.github.io/ccf-ui/rui/  

We also need Uberon terms, see Amanda’s earlier data compilation at 

https://docs.google.com/spreadsheets/d/1wkoN9fyUtVZWYnbK0S0AKJmiTS-yELCRKgkNqk870eA/edit?pli=1#gid=1729887084 

### Commands ran

```
# create conda environment

conda create -n deriva -y python==3.9

# activate and install deriva
conda activate deriva
pip install deriva

# run the script
python c2m2_cv_usage.py
```

Then I get the error message:

```
(deriva) jessicalumian@Jessicas-MacBook-Pro uberon_cfde % python c2m2_cv_usage.py
Traceback (most recent call last):
  File "/Users/jessicalumian/uberon_cfde/c2m2_cv_usage.py", line 137, in <module>
    tid = vocab_terms[tname][int(nid)]['id']
ValueError: invalid literal for int() with base 10: '[16, 2]'
(deriva) jessicalumian@Jessicas-MacBook-Pro uberon_cfde %
```

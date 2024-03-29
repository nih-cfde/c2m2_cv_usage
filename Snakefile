##
## Workflow to Generate Controlled Vocabulary from C2M2
##

rule all:
    message:
        f"Generate Controlled Vocabulary from C2M2"
    input:
        "table_no_zero.csv",
        "table.csv",
        "usage.json",
        "c2m2_cv_usage.py"


rule run_C2M2_script:
    message:
        "Running C2M2 script"
    output:
        "usage.json"
    shell: """
        # run the C2M2 script
        python c2m2_cv_usage.py -o {output}
    """


rule run_formatting_script:
    message:
        "Running formatting script"
    input:
        "usage.json"
    output:
        "table.csv"       
    shell: """
        # run reformatting script to make csv
        python display.py {input} -o {output}
        python remove_zeros.py
        cat table_no_zero.csv
    """

rule remove_zeros:
    message:
        "Removing zeros"
    output:
        "table_no_zero.csv"
    input:
        "table.csv"       
    shell: """
        python remove_zeros.py
        head {output}
        tail {output}
    """    

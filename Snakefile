##
## Workflow to Generate Controlled Vocabulary from C2M2
##

rule all:
    message:
        f"Generate Controlled Vocabulary from C2M2"
    input:
        "table.csv",
        "c2m2_cv_usage.py"


rule run_C2M2_script:
    message:
        "Running C2M2 script"
    output:
        "out.txt"
    shell: """
        # run the C2M2 script
        python c2m2_cv_usage.py > {output}
    """


rule run_formatting_script:
    message:
        "Running formatting script"
    input:
        "out.txt"
    output:
        "table.csv"       
    shell: """
        # run reformatting script to make csv
        python display.py {input} -o {output}
        python remove_zeros.py
        cat table_no_zero.csv
    """
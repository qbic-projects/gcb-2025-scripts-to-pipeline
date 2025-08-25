# gcb-2025-scripts-to-pipeline
This holds all files related to the workshop " From a Collection of Scripts to a Pipeline – Writing Nextflow Workflows with nf-core Best Practices" at the GCB 2025.

Authors: Famke Bäuerle ([@famosab](https://github.com/famosab)), Mark Polster ([@mapo9](https://github.com/mapo9))

> Bioinformatics analyses often begin as a set of scattered scripts, but scaling them into reproducible and maintainable workflows can be challenging. In this hands-on workshop we aim to guide you through transforming your scripts into a robust Nextflow pipeline using nf-core components and best practices. We will cover essential topics such as pipeline structuring, version control, and best practices for collaboration and reproducibility. Whether you're new to Nextflow or looking to refine your workflow development skills, this workshop will provide practical insights and hands-on experience to help you understand and utilize the nf-core framework for your own research.
 
## What is this repository?

Here we provide the materials for the workshop. You can find everything related to "bash-scripts" in the `bash/` folder and everything related to "python-scripts" in the `py_scripts/` folder. Exemplary VCF files to test out different things are available in the `vcf-files/` folder. Each of the folders comes with a short README which gives you more information on how to use the files and scripts in the respective folder.

Our objective is to guide you through the process of transforming existing scripts into a working [nextflow](https://www.nextflow.io/) pipeline by utilizing [nf-core](https://nf-co.re/) components. 

## Step zero: Create a new pipeline by using the nf-core template

...

## Step one: Transform bash scripts by utilizing nf-core modules

1. Try running the bash scripts by following the advice in the README.

2. The provided bash scripts are available as [nf-core modules](https://nf-co.re/modules/). Look for them and install them to your pipeline with nf-core tools.

```bash
nf-core modules install ...
```

3. Integrate these scripts into a subworkflow called ...

## Step two: Utilize existing python scripts in your pipeline

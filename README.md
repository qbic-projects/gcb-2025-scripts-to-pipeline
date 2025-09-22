# gcb-2025-scripts-to-pipeline
This holds all files related to the workshop "From a Collection of Scripts to a Pipeline – Writing Nextflow Workflows with nf-core Best Practices" at the GCB 2025.

Authors: Famke Bäuerle ([@famosab](https://github.com/famosab)), Mark Polster ([@mapo9](https://github.com/mapo9))

> Bioinformatics analyses often begin as a set of scattered scripts, but scaling them into reproducible and maintainable workflows can be challenging. In this hands-on workshop we aim to guide you through transforming your scripts into a robust Nextflow pipeline using nf-core components and best practices. We will cover essential topics such as pipeline structuring, version control, and best practices for collaboration and reproducibility. Whether you're new to Nextflow or looking to refine your workflow development skills, this workshop will provide practical insights and hands-on experience to help you understand and utilize the nf-core framework for your own research.
 
## What is this repository?

Here we provide the materials for the workshop. You can find everything related to "bash-scripts" in the `bash/` folder and everything related to "python-scripts" in the `py_scripts/` folder. Exemplary VCF files to test out different things are available in the `vcf-files/` folder. Each of the folders comes with a short README which gives you more information on how to use the files and scripts in the respective folder.

Our objective is to guide you through the process of transforming existing scripts into a working [nextflow](https://www.nextflow.io/) pipeline by utilizing [nf-core](https://nf-co.re/) components. 

## Workshop: Create your own pipeline

### Step zero: Create a new pipeline by using the nf-core template

1. You need the [nf-core toolbox](https://nf-co.re/docs/nf-core-tools). 
```bash
conda create --name nf-core python=3.12 nf-core nextflow
conda activate nf-core
```

2. Use the pipelines create command to create a new pipeline.
Do this in a new and empty folder. The pipeline name can be anything, for example `gcbworkshop`.
```bash
nf-core pipelines create
```

3. Further steps.
You will find a lot of TODO statements in the pipeline code. You do not need to worry about those for now. We will work on simple modules and subworkflows to help you understand the template a little more.

> [!NOTE]
> The nf-core documentation is a great source for recommendations and tricks. You can find a lot of answers [over there](https://nf-co.re/docs/guidelines/pipelines/overview). Anything Nextflow related can be looked up in the [Nextflow docs](www.nextflow.io/docs/latest/index.html).

#### Files you need to adapt

If you work with out exemplary scripts you will need to adapt files in the `assets` folder of your pipeline. The adapted files are given under `files_to_change/assets`.

### Step one: Transform bash scripts by utilizing nf-core modules

1. Try running the bash scripts by following the advice in the README.

2. The provided bash scripts are available as [nf-core modules](https://nf-co.re/modules/). Look for them and install them to your pipeline with nf-core tools. You can find the tool by having a look in the bash script or the provided conda environment.

```bash
nf-core modules install ...
```
The modules we want to use here are very similar to their usage in the [qbic-pipelines/vcftomaf pipeline](https://github.com/qbic-pipelines/vcftomaf). You can refer to that pipeline if you get stuck but note that it has more functionality than what we are aiming for.

3. Integrate these scripts into a subworkflow called `bash_scripts.nf` in your pipeline.

```bash
nf-core subworkflows create
```
This creates the files necessary for a new subworkflow within your pipeline. You can adapt those to your needs.

### Step two: Utilize existing python scripts in your pipeline
1. Try running the python scripts by following the advice in the README.

2. Go to [Seqera Containers](https://seqera.io/containers/) and create your own Container with the required tools to run the scripts (see `conda_py.yml`)

3. Create a subworkflow called `py_scripts.nf` in your pipeline (see above)

4. Copy the python scripts to the `bin` folder of the pipeline and make them executable

5. Create a module for each of the scripts and call them in the subworkflow (you can use the [fasta2peptides module](https://github.com/nf-core/epitopeprediction) as an orientation)
 
```bash
nf-core modules create 
```
This creates the files necessary for a new module within your pipeline. You can adapt those to your needs.

To understand how Python  scripts can be utilized you can check out the  [nf-core/epitopeprediction](github.com/nf-core/epitopeprediction) pipeline, e.g. the [fasta2peptides module](https://github.com/nf-core/epitopeprediction).

## Using nf-core pipelines

Many bioinformatics problems have a nf-core pipeline that you can use to run your own analysis. Feel free to check out [the nf-core website](https://nf-co.re/pipelines/) and search for keywords matching your data. You can then read the documentation and try to run the pipeline for your own analysis. If you get stuck you can always ask in the slack channel of the pipeline. You can join the slack [here](https://nf-co.re/join).

## Common problems

1. Wrong nf-core version.
```bash
pip install --upgrade nf-core
````
should upgrade to nf-core version > 3.0

2. Java is missing
```bash
sdk install java 17.0.10-tem
````
needs to be added to your path aswell:
```bash
export JAVA_CMD="/home-link/paifb01/.sdkman/candidates/java/17.0.10-tem/bin/java"
```
replace `/home-link/paifb01/` with the path to your sdkman installation.
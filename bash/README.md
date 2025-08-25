# How to use the bash scripts in this folder
Intended use: First filter the VCF files by PASS and then transform them into MAF files.

### 1. Install necessary packages
You need to create an environment that contains the packages bcftools and vcf2maf.

```bash
conda create -n gcb --file conda.yml
conda activate gcb
```

### 2. Reference sequence 
You will need to download the reference sequence (its too big to be stored in this repo) unzip and bgzip it.

```bash
curl https://hgdownload.soe.ucsc.edu/goldenpath/hg38/bigZips/hg38.fa.gz --output hg38.fa.gz
# unzip and bgzip to make sure the file is bgzipped and works with vcf2maf
gunzip hg38.fa.gz
bgzip --threads 4 hg38.fa
```

The release 113 is the one that matches the VEP annotation info in the VCF file:
```
##VEP="v113.0" API="v113" time="2025-04-09 11:23:34" cache="/tmp/nahbu450-849233/nxf.NWrquFAhtf/113_GRCh38/homo_sapiens/113_GRCh38" ensembl=113.58650ec ensembl-compara=113.d7a53c5 ensembl-funcgen=113.e30608c ensembl-io=113.bee6816 ensembl-variation=113.cef2add 1000genomes="phase3" COSMIC="99" ClinVar="202404" HGMD-PUBLIC="20204" assembly="GRCh38.p14" dbSNP="156" gencode="GENCODE 47" genebuild="GENCODE47" gnomADe="v4.1" gnomADg="v4.1" polyphen="2.2.3" regbuild="1.0" sift="6.2.1"
```

### 3. Run the scripts 
Then you can run the scripts for the muse VCF file like following:

```bash
bash filter.sh ../vcf-files/tumor_5_vs_normal_5.muse_VEP.ann.vcf.gz muse.filtered.vcf.gz

# you need .. because the convert.sh script will descend one folder
bash convert.sh ../muse.filtered.vcf.gz ../muse.maf ../hg38.fa.gz
```
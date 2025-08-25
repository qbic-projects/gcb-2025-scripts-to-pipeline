# How to use the python scripts in this folder
Intended use: Take the vcf files in the "vcf-files" directory and plot statistics on the individual files, as well as a combination of files.

### 1. Install necessary packages
You need to create an environment that contains the packages bcftools and vcf2maf.

```bash
conda create -n gcb_py --file conda.yml
conda activate gcb_py
```


### 2. Run the scripts 
Then you can run the scripts as seen in the test_files

```bash
# Single VCF
python3 single_vcf_stats.py \
    --vcf ../vcf-files/tumor_5_vs_normal_5.muse_VEP.ann.vcf.gz \
    --out single

# Multiple VCF
python3 multiple_vcf_stats.py \
    --vcf ../vcf-files/tumor_5_vs_normal_5.muse_VEP.ann.vcf.gz ../vcf-files/tumor_5_vs_normal_5.strelka.somatic_indels_VEP.ann.vcf.gz \
    --out multi
```
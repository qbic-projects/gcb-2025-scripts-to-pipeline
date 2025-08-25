#!/bin/bash
# Usage: ./convert.sh input.filtered.vcf.gz output.maf

export VCF2MAF_URL=`curl -sL https://api.github.com/repos/mskcc/vcf2maf/releases | grep -m1 tarball_url | cut -d\" -f4`
curl -L -o mskcc-vcf2maf.tar.gz $VCF2MAF_URL; tar -zxf mskcc-vcf2maf.tar.gz; cd mskcc-vcf2maf-*

INPUT_VCF="$1"
OUTPUT_MAF="$2"
REFERENCE_FA="$3"

gunzip "$INPUT_VCF"

# Remove .gz extension from INPUT_VCF variable for use in the perl script
INPUT_VCF_UNZIPPED="${INPUT_VCF%.gz}"

perl vcf2maf.pl --input-vcf "$INPUT_VCF_UNZIPPED" --output-maf "$OUTPUT_MAF" --ref-fasta "$REFERENCE_FA" --ncbi-build GRCh38 --species homo_sapiens --inhibit-vep --tumor-id TUMOR --normal-id NORMAL --verbose

bgzip "$INPUT_VCF_UNZIPPED"

#!/bin/bash

# Usage: ./convert.sh input.filtered.vcf.gz reference.fa output.maf

INPUT_VCF="$1"
REFERENCE_FA="$2"
OUTPUT_MAF="$3"

# Run vcf2maf (assumes vcf2maf.pl and VEP are installed and in PATH)
vcf2maf.pl \
  --input-vcf "$INPUT_VCF" \
  --output-maf "$OUTPUT_MAF" \
  --ref-fasta "$REFERENCE_FA" \

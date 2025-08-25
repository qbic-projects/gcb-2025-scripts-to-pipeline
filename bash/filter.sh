#!/bin/bash

# Usage: ./filter.sh input.vcf.gz intervals.bed output.filtered.vcf.gz

INPUT_VCF="$1"
INTERVALS_BED="$2"
OUTPUT_VCF="$3"

# Filter for PASS variants and regions in BED file
bcftools view -f PASS -R "$INTERVALS_BED" "$INPUT_VCF" -Oz -o "$OUTPUT_VCF"

# Index the output VCF
tabix -p vcf "$OUTPUT_VCF"
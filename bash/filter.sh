#!/bin/bash

# Usage: ./filter.sh input.vcf.gz output.filtered.vcf.gz

INPUT_VCF="$1"
OUTPUT_VCF="$2"

bcftools view -f 'PASS,.' "$INPUT_VCF" --output-type z --write-index=tbi -o "$OUTPUT_VCF"

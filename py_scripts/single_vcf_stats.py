"""
VCF Stats Plotter (Single VCF)
------------------------------
Takes one VCF file and generates summary statistics plots.

Usage:
    python vcf_stats_single.py --vcf input.vcf.gz --out output_prefix
"""

import argparse
from cyvcf2 import VCF
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re


def sort_chromosomes(chrom_list):
    """Sort chromosomes alphanumerically (chr1, chr2, ..., chr10, chr11, ..., chrX, chrY)."""
    def chrom_key(chrom):
        # Remove 'chr' prefix if present
        chrom_clean = chrom.replace('chr', '') if chrom.startswith('chr') else chrom
        
        # Handle numeric chromosomes
        if chrom_clean.isdigit():
            return (0, int(chrom_clean))
        # Handle X chromosome
        elif chrom_clean == 'X':
            return (1, 0)
        # Handle Y chromosome  
        elif chrom_clean == 'Y':
            return (1, 1)
        # Handle other chromosomes (MT, etc.)
        else:
            return (2, chrom_clean)
    
    return sorted(chrom_list, key=chrom_key)


def parse_vcf(vcf_file):
    """Parse a single VEP-annotated VCF and return a DataFrame of variant stats."""
    records = []
    vcf = VCF(vcf_file)

    for variant in vcf:
        ref_len = len(variant.REF)
        alt_len = len(variant.ALT[0]) if variant.ALT else 0
        var_type = "SNP" if (ref_len == 1 and alt_len == 1) else "INDEL"

        # Extract VEP CSQ annotation (pipe-delimited fields)
        csq = variant.INFO.get("CSQ", "")
        csq_split = csq.split("|") if csq else []
        consequence = csq_split[1] if len(csq_split) > 1 else None
        impact = csq_split[2] if len(csq_split) > 2 else None        # HIGH/MODERATE/LOW/MODIFIER
        vep_type = csq_split[21] if len(csq_split) > 21 else None  # "SNV", "insertion", "deletion" etc.
        gene = csq_split[3] if len(csq_split) > 3 else None          # gene symbol

        records.append({
            "chrom": variant.CHROM,
            "pos": variant.POS,
            "ref": variant.REF,
            "alt": variant.ALT[0] if variant.ALT else None,
            "qual": variant.QUAL,
            "refalt_type": var_type,          # SNP vs INDEL (REF/ALT length based)
            "vep_consequence": consequence,   # intron_variant, missense_variant, etc.
            "vep_type": vep_type,             # SNV, insertion, deletion (VEP)
            "impact": impact,                 # HIGH/MODERATE/LOW/MODIFIER
            "gene": gene                      # gene symbol
        })

    return pd.DataFrame(records)



def plot_stats(df, out_prefix="vcf_stats"):
    """Generate plots for one VCF."""
    # Set modern style with custom parameters
    plt.style.use('default')
    plt.rcParams.update({
        'font.size': 12,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 11,
        'figure.titlesize': 16
    })

    # Variants per chromosome
    plt.figure(figsize=(12,7))
    ax = sns.countplot(data=df, x="chrom", order=sort_chromosomes(df["chrom"].unique()), color="darkblue")
    plt.title("Variants per Chromosome", fontweight='bold', pad=20)
    plt.xlabel("Chromosome", fontweight='bold')
    plt.ylabel("Number of Variants", fontweight='bold')
    plt.xticks(rotation=45, ha="right")
    
    # Add value labels on bars
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                   (p.get_x() + p.get_width()/2., p.get_height()), 
                   ha='center', va='bottom', fontsize=9)
    
    sns.despine()
    plt.tight_layout()
    plt.savefig(f"{out_prefix}_per_chrom.png", dpi=300, bbox_inches='tight')
    plt.close()

    # SNV/indel/etc from VEP annotation
    if df["vep_type"].notna().any():
        plt.figure(figsize=(8,6))
        ax = sns.countplot(data=df, x="vep_type", 
                          order=df["vep_type"].value_counts().index, color="darkblue")
        plt.title("Variant Types (VEP Annotation)", fontweight='bold', pad=20)
        plt.xlabel("Variant Type", fontweight='bold')
        plt.ylabel("Count", fontweight='bold')
        plt.xticks(rotation=45, ha="right")
        
        # Add value labels
        for p in ax.patches:
            ax.annotate(f'{int(p.get_height())}', 
                       (p.get_x() + p.get_width()/2., p.get_height()), 
                       ha='center', va='bottom', fontsize=10)
        
        sns.despine()
        plt.tight_layout()
        plt.savefig(f"{out_prefix}_vep_type.png", dpi=300, bbox_inches='tight')
        plt.close()

    # SNP/INDEL (REF/ALT length)
    plt.figure(figsize=(8,6))
    colors = ['#3498db', '#e74c3c']  # Blue and red
    ax = sns.countplot(data=df, x="refalt_type", palette=colors, hue="refalt_type", color="darkblue")
    plt.title("Variant Classification (SNP vs INDEL)", fontweight='bold', pad=20)
    plt.xlabel("Variant Type", fontweight='bold')
    plt.ylabel("Count", fontweight='bold')
    
    # Add value labels
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', 
                   (p.get_x() + p.get_width()/2., p.get_height()), 
                   ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    sns.despine()
    plt.tight_layout()
    plt.savefig(f"{out_prefix}_refalt_type.png", dpi=300, bbox_inches='tight')
    plt.close()

    # Top functional consequences
    if df["vep_consequence"].notna().any():
        top_terms = df["vep_consequence"].value_counts().nlargest(10)
        plt.figure(figsize=(10,8))
        ax = sns.barplot(x=top_terms.values, y=top_terms.index, orient='h', color="darkblue")
        plt.title("Top 10 Functional Consequences", fontweight='bold', pad=20)
        plt.xlabel("Number of Variants", fontweight='bold')
        plt.ylabel("Consequence Type", fontweight='bold')
        
        # Add value labels
        for i, v in enumerate(top_terms.values):
            ax.text(v + max(top_terms.values) * 0.01, i, str(v), 
                   va='center', fontweight='bold')
        
        sns.despine()
        plt.tight_layout()
        plt.savefig(f"{out_prefix}_vep_consequence.png", dpi=300, bbox_inches='tight')
        plt.close()

    # Impact severity (HIGH/MODERATE/LOW/MODIFIER)
    if df["impact"].notna().any():
        plt.figure(figsize=(8,6))
        # Custom colors for impact levels
        impact_colors = {'HIGH': '#e74c3c', 'MODERATE': '#f39c12', 
                        'LOW': '#f1c40f', 'MODIFIER': '#95a5a6'}
        order = ["HIGH","MODERATE","LOW","MODIFIER"]
        colors = [impact_colors.get(x, '#34495e') for x in order]
        
        ax = sns.countplot(data=df, x="impact", order=order, palette=colors, hue="impact")
        plt.title("Impact Severity Distribution", fontweight='bold', pad=20)
        plt.xlabel("Impact Level", fontweight='bold')
        plt.ylabel("Count", fontweight='bold')
        
        # Add value labels
        for p in ax.patches:
            ax.annotate(f'{int(p.get_height())}', 
                       (p.get_x() + p.get_width()/2., p.get_height()), 
                       ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        sns.despine()
        plt.tight_layout()
        plt.savefig(f"{out_prefix}_impact.png", dpi=300, bbox_inches='tight')
        plt.close()

    # Top 10 genes with most variants
    if df["gene"].notna().any():
        # adapt empty as NaN 
        df["gene"] = np.where(df["gene"] == "", "NaN", df["gene"])
        top_genes = df["gene"].value_counts().nlargest(10)

        plt.figure(figsize=(10,8))
        ax = sns.barplot(x=top_genes.values, y=top_genes.index, orient='h', color="darkblue")
        plt.title("Top 10 Genes with Most Variants", fontweight='bold', pad=20)
        plt.xlabel("Number of Variants", fontweight='bold')
        plt.ylabel("Gene Symbol", fontweight='bold')
        
        # Add value labels
        for i, v in enumerate(top_genes.values):
            ax.text(v + max(top_genes.values) * 0.01, i, str(v), 
                   va='center', fontweight='bold')
        
        sns.despine()
        plt.tight_layout()
        plt.savefig(f"{out_prefix}_top_genes.png", dpi=300, bbox_inches='tight')
        plt.close()


def main():
    parser = argparse.ArgumentParser(description="Plot statistics from a single VCF")
    parser.add_argument("--vcf", type=str, required=True, help="VCF file (.vcf or .vcf.gz)")
    parser.add_argument("--out", type=str, required=True, help="Output prefix for plots")
    args = parser.parse_args()

    print(f"Processing {args.vcf} ...")
    df = parse_vcf(args.vcf)
    plot_stats(df, out_prefix=args.out)
    print(f"Plots saved with prefix {args.out}_*.png")

if __name__ == "__main__":
    main()

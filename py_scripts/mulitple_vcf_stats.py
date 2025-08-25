"""
VCF Stats Comparator (Multiple VEP-annotated VCFs)
-------------------------------------------------
Generates comparative statistics plots for multiple VCF files.

Usage:
    python vcf_stats_multi.py file1.vcf.gz file2.vcf.gz -o compare_out
"""

import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from cyvcf2 import VCF


def parse_vcf(vcf_file):
    """Parse one VEP-annotated VCF and return DataFrame with file label."""
    records = []
    vcf = VCF(vcf_file)

    for variant in vcf:
        ref_len = len(variant.REF)
        alt_len = len(variant.ALT[0]) if variant.ALT else 0
        var_type = "SNP" if (ref_len == 1 and alt_len == 1) else "INDEL"

        csq = variant.INFO.get("CSQ", "")
        csq_split = csq.split("|") if csq else []

        consequence = csq_split[1] if len(csq_split) > 1 else None
        gene = csq_split[3] if len(csq_split) > 3 else None
        impact = csq_split[2] if len(csq_split) > 2 else None
        vep_type = csq_split[16] if len(csq_split) > 16 else None

        records.append({
            "chrom": variant.CHROM,
            "refalt_type": var_type,
            "vep_consequence": consequence,
            "vep_type": vep_type,
            "impact": impact,
            "gene": gene,
            "file": vcf_file
        })

    return pd.DataFrame(records)


def plot_stats(df, out_prefix="vcf_compare"):
    """Generate comparative plots for multiple VEP-annotated VCFs."""
    sns.set(style="whitegrid")

    # 1. Variants per chromosome (per file)
    plt.figure(figsize=(12,6))
    sns.countplot(data=df, x="chrom", hue="file", order=sorted(df["chrom"].unique()))
    plt.title("Variants per chromosome")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(f"{out_prefix}_per_chrom.png")
    plt.close()

    # 2. SNP/INDEL (REF/ALT length) per file
    plt.figure(figsize=(8,5))
    sns.countplot(data=df, x="refalt_type", hue="file")
    plt.title("Variant type (SNP vs INDEL, REF/ALT length)")
    plt.tight_layout()
    plt.savefig(f"{out_prefix}_refalt_type.png")
    plt.close()

    # 3. SNV/indel/etc from VEP annotation
    if df["vep_type"].notna().any():
        plt.figure(figsize=(10,6))
        sns.countplot(data=df, x="vep_type", hue="file",
                      order=df["vep_type"].value_counts().index)
        plt.title("Variant type (VEP CSQ annotation)")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(f"{out_prefix}_vep_type.png")
        plt.close()

    # 4. Top 10 functional consequences (combined across files)
    if df["vep_consequence"].notna().any():
        top_terms = df["vep_consequence"].value_counts().nlargest(10).index
        df_top = df[df["vep_consequence"].isin(top_terms)]
        plt.figure(figsize=(10,6))
        sns.countplot(data=df_top, y="vep_consequence", hue="file",
                      order=top_terms)
        plt.title("Top 10 functional consequences (VEP)")
        plt.tight_layout()
        plt.savefig(f"{out_prefix}_vep_consequence.png")
        plt.close()

    # 5. Impact severity distribution
    if df["impact"].notna().any():
        plt.figure(figsize=(8,5))
        sns.countplot(data=df, x="impact", hue="file",
                      order=["HIGH","MODERATE","LOW","MODIFIER"])
        plt.title("Impact severity distribution")
        plt.tight_layout()
        plt.savefig(f"{out_prefix}_impact.png")
        plt.close()

    # 6. Top 10 genes with most variants (combined)
    if df["gene"].notna().any():
        top_genes = df["gene"].value_counts().nlargest(10).index
        df_top = df[df["gene"].isin(top_genes)]
        plt.figure(figsize=(10,6))
        sns.countplot(data=df_top, y="gene", hue="file",
                      order=top_genes)
        plt.title("Top 10 genes with most variants")
        plt.tight_layout()
        plt.savefig(f"{out_prefix}_top_genes.png")
        plt.close()


def main():
    parser = argparse.ArgumentParser(description="Compare statistics across multiple VEP-annotated VCFs")
    parser.add_argument("--vcfs", required=True, type=str, nargs="+", help="VCF files (.vcf or .vcf.gz)")
    parser.add_argument("--out", required=True, type=str, default="vcf_compare", help="Output prefix for plots")
    args = parser.parse_args()

    dfs = []
    for vcf_file in args.vcfs:
        print(f"Processing {vcf_file} ...")
        dfs.append(parse_vcf(vcf_file))

    combined_df = pd.concat(dfs, ignore_index=True)
    plot_stats(combined_df, out_prefix=args.out)
    print(f"Plots saved with prefix {args.out}_*.png")


if __name__ == "__main__":
    main()
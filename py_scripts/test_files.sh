python3 single_vcf_stats.py \
    --vcf ../vcf-files/tumor_5_vs_normal_5.muse_VEP.ann.vcf.gz \
    --out test_out


python3 multiple_vcf_stats.py \
    --vcf ../vcf-files/tumor_5_vs_normal_5.muse_VEP.ann.vcf.gz /Users/markpolster/workdir/gcb_2025/gcb-2025-scripts-to-pipeline/vcf-files/tumor_5_vs_normal_5.strelka.somatic_indels_VEP.ann.vcf.gz \
    --out multi
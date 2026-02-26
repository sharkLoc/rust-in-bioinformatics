# smrest

smrest is a prototype somatic mutation caller for single molecule long reads. It uses haplotype phasing patterns for tumour samples that have a sigificant proportion of normal cells (purity > 0.3, < 0.8) to identify somatic mutations. For more details, see the preprint linked below.

## Citation

[Simpson, J.T., Detecting Somatic Mutations Without Matched Normal Samples Using Long Reads, BioRxiv](https://www.biorxiv.org/content/10.1101/2024.02.26.582089v1)

## Compiling

This program is written in Rust and uses the [Cargo](https://doc.rust-lang.org/cargo/getting-started/installation.html) build system. After you have installed Cargo, you can compile this software from github as follows:

```
git clone https://github.com/jts/smrest.git
cd smrest
cargo build --release
```

## Usage

smrest has three steps: first it finds heterozygous SNPs using a panel of known population variants from gnomAD, then these are phased using `whatshap`, followed by somatic mutation calling. These steps can be run manually, or using a Snakemake pipeline we have provided for convenience. We describe both methods here, using a small demo dataset that is descibed in the following section.

### Demo data preparation

To demonstrate the usage of this program, we have prepared a small dataset consisting of ONT reads for chromosome 20 of COLO829/COLO829BL. To get the demo data you can use the snakemake pipeline (for simplicitly all commands shown below will assume you are running in the `smrest/workflow` directory, if you are running from a different path you will need to adjust the commands):

```
snakemake prepare_demo
```

This command will place the reads in `data/COLO829.mixture.chr20.bam`. `smrest` needs a set of population variants to estimate the local of heterozygous SNPs and a BED file describing the callable regions of the genome. You can download these resources using snakemake as well:

```
snakemake prepare_resources
```

### Mutation calling (manual)

There are three steps to calling somatic mutations with smrest. First, we find heterozygous SNPs with `smrest genotype-hets`:

```
smrest genotype-hets -c resources/genotype_sites.vcf -r chr20 -g resources/GRCh38_no_alt_analysis_set.GCA_000001405.15.fna data/COLO829.mixture.chr20.bam > COLO829.gnomad_genotype.vcf
```

Next, we phase these hets using whatshap:

```
whatshap phase --ignore-read-groups -r resources/GRCh38_no_alt_analysis_set.GCA_000001405.15.fna -o COLO829.gnomad_genotype_whatshap_phased.vcf COLO829.gnomad_genotype.vcf data/COLO829.mixture.chr20.bam
```

Finally, we call somatic mutations:

```
smrest call -m haplotype-likelihood --purity 0.5 -r chr20 -g resources/GRCh38_no_alt_analysis_set.GCA_000001405.15.fna -p COLO829.gnomad_genotype_whatshap_phased.vcf -o COLO829.smrest_called_regions.bed data/COLO829.mixture.chr20.bam > COLO829.smrest_somatic_calls.vcf
```
These mutations calls are over all regions of the genome that could be phased. To produce the final call set we intersect the phased BED file with the GIAB best practices BED:

```
bedtools intersect -b resources/GRCh38_notinalldifficultregions.bed -a COLO829.smrest_called_regions.bed > COLO829.smrest_best_practice_called_regions.bed
```

Then use this BED to produce the final call set:

```
bcftools filter -T COLO829.smrest_best_practice_called_regions.bed COLO829.smrest_somatic_calls.vcf > COLO829.smrest_somatic_calls_final.vcf
```

### Mutation calling (pipeline)

A Snakemake pipeline is provided in `workflow/Snakemake` to automate these three steps. It will also parallelize the process across 10Mb segments of the genome. It assumes the BAM file is in `data/` (as in the demo data) and the pipeline can be run by building the `smrest_calls/<sample>/<sample>.whatshap.final_q20_pass_calls.vcf` target, where <sample> is the prefix of the BAM file. For example:

```
snakemake smrest_calls/COLO829.mixture.chr20/COLO829.mixture.chr20.whatshap.final_q20_pass_calls.vcf
```

## License

MIT

## Acknowledgements

This program reuses code originally developed by Edge et al for the [Longshot](https://github.com/pjedge/longshot) variant caller.


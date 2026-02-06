# floria - metagenomic long or short-read strain haplotype phasing

## Introduction

**Floria** is a software package for recovering microbial haplotypes and clustering reads at the strain level from metagenomic sequencing data. See [the introduction here](https://phase-doc.readthedocs.io/en/latest/introduction.html) for more information. 

After calling SNPs against reference genomes __or__ a metagenomic assembly, floria produces 1) strain-level clusters of short or long reads and 2) their haplotypes **in minutes**. 

<p align="center">
  <img width="460" height="400" src="https://github.com/bluenote-1577/vartig-utils/blob/main/visualize-vartig-example.png", caption="asdf">
</p>
<p align="center">
  <i>
    A 1Mbp contig (Brevefilum fermentans) was automatically phased into two strains (top: y-axis is coverage). Only two strains are present with high HAPQ; spurious "haplosets" are given low HAPQ.
  </i>
</p>

### Inputs

Floria requires: 

1. a list of variants in .vcf format
2. a set of reads mapped to assembled contigs/references in .bam format

See the **"Floria-PL"** pipeline [here](https://github.com/jsgounot/Floria_analysis_workflow) for reads-to-haplotype pipelines if you do not know how to get started with generating VCFs or BAMs. 

## Outputs, tutorials, and manuals (full documentation)

See https://phase-doc.readthedocs.io/en/latest/index.html for more information on tutorials, outputs, and extra manuals for usage. 

## Install + Quick start 

#### Option 1 - compile from scratch

A relatively recent standard toolchain is needed.

1. [rust](https://www.rust-lang.org/tools/install) **version > 1.80.0** and associated tools such as cargo are required and assumed to be in PATH.
2. [cmake](https://cmake.org/download/) **version > 3.12** is required. It's sufficient to download the binary from the link and do `PATH="/path/to/cmake-3.xx.x-linux-x86_64/bin/:$PATH"` before installation. 
3. make 
4. GCC 

If you're using an **x86-64 architecture with SSE instructions (most linux systems)**: 

```sh
git clone https://github.com/bluenote-1577/floria
cd floria

cargo install --path . 
floria -h # binary is available in PATH
```

If you're using an **ARM architecture with NEON instructions** (e.g. Mac M1): 

```sh

# If using ARM architecture with NEON instructions
cargo install --path . --root ~/.cargo --features=neon --no-default-features
floria -h # binary is available in PATH

```

#### Option 2 - bioconda

```sh
conda install -c bioconda floria
```

#### Option 3 - precompiled static binary on **x86-64-linux**

The static binary is only for x86-64 linux with SSE instructions currently. 

```sh
wget https://github.com/bluenote-1577/floria/releases/download/latest/floria
chmod +x floria
./floria -h
```

### Quick Start after install 

```sh
git clone https://github.com/bluenote-1577/floria
cd floria

# run floria on mock data
floria -b tests/test_long.bam  -v tests/test.vcf  -r tests/MN-03.fa -o 3_klebsiella_strains
ls 3_klebsiella_strains

# visualize strain "vartigs" if you have matplotlib
python scripts/visualize_vartigs.py 3_klebsiella_strains/NZ_CP081897.1/NZ_CP081897.1.vartigs
```

## Citation
\*Co-lead authors

Jim Shaw\*, Jean-Sebastien Gounot\*, Hanrong Chen, Niranjan Nagarajan, Yun William Yu. [Floria: Fast and accurate strain haplotyping in metagenomes](https://doi.org/10.1093/bioinformatics/btae252) (2024). Bioinformatics.


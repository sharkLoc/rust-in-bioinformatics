[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](http://bioconda.github.io/recipes/lorikeet-genome/README.html)
![](https://anaconda.org/bioconda/lorikeet-genome/badges/license.svg)
![](https://anaconda.org/bioconda/lorikeet-genome/badges/version.svg)
![](https://anaconda.org/bioconda/lorikeet-genome/badges/latest_release_relative_date.svg)
![](https://anaconda.org/bioconda/lorikeet-genome/badges/platforms.svg)
[![DOI](https://zenodo.org/badge/187937357.svg)](https://zenodo.org/doi/10.5281/zenodo.10275468)

![](docs/_include/images/lorikeet_logo.png)

## Lorikeet

Lorikeet is a within-species variant analysis pipeline for metagenomic communities that utilizes both long and short reads.
Lorikeet utilizes a re-implementaion of the GATK HaplotypeCaller algorithm, performing local re-assembly of potentially active
regions within candidate genomes. Called variants can be clustered into likely strains using a combination of UMAP and HDBSCAN.

## Documentation

For detailed documentation of Lorikeet and the various algorithms and concepts it touches on please visit the 
[Lorikeet Docs](https://rhysnewell.github.io/Lorikeet)


## Quick Start

### Installation

Lorikeet is distributed via Crates.io https://crates.io/crates/lorikeet-genome. Additional packages can be downloaded via conda using the `lorikeet.yml` file provided. Ensure that cargo is installed on your system:

```bash
curl https://sh.rustup.rs -sSf | sh
```

Then install lorikeet:

```bash
cargo install lorikeet-genome
```

Alongside required packages:

```bash
conda env create -f lorikeet.yml -n lorikeet
conda activate lorikeet
```

## Usage

Input can either be reads and reference genome, or MAG. Or a BAM file and associated genome.

```
Strain genotyping analysis for metagenomics

Usage: lorikeet <subcommand> ...

Main subcommands:
    genotype    *Experimental* Resolve strain-level genotypes of MAGs from microbial communities
    consensus   Creates consensus genomes for each input reference and for each sample
    call        Performs variant calling with no downstream analysis
    evolve      Calculate dN/dS values for genes from read mappings

Other options:
    -V, --version   Print version information

Rhys J. P. Newell <r.newell near uq.edu.au>
```

Call variants from bam:

`lorikeet call --bam-files my.bam --longread-bam-files my-longread.bam --genome-fasta-directory genomes/ -x fna
     --bam-file-cache-directory saved_bam_files --output-directory lorikeet_out/ --threads 10 --plot`

Call variants from short reads and longread bam files:

`lorikeet call -r input_genome.fna -1 forward_reads.fastq -2 reverse_reads.fastq -l longread.bam`


## Shell completion

Completion scripts for various shells e.g. BASH can be generated. For example, to install the bash completion script system-wide (this requires root privileges):

```
lorikeet shell-completion --output-file lorikeet --shell bash
mv lorikeet /etc/bash_completion.d/
```

It can also be installed into a user's home directory (root privileges not required):

```
lorikeet shell-completion --shell bash --output-file /dev/stdout >>~/.bash_completion
```

In both cases, to take effect, the terminal will likely need to be restarted. To test, type `lorikeet ca` and it should complete after pressing the TAB key.

## License

Code is [GPL-3.0](LICENSE)


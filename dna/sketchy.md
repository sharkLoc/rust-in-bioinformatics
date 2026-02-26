# sketchy <a href='https://github.com/esteinig'><img src='docs/images/logo.png' align="right" height="250" /></a>

![](https://img.shields.io/badge/lang-rust-black.svg)
![](https://img.shields.io/badge/version-0.6.0-green.svg)
![](https://img.shields.io/badge/preprint-0.12.0-green.svg)

Genomic neighbor typing for lineage and genotype inference

## Overview

**`v0.6.0`**

`Sketchy` is a lineage calling and genotyping tool based on the heuristic principle of genomic neighbor typing developed by [Karel Břinda and colleagues (2020)](https://www.biorxiv.org/content/10.1101/403204v2). It queries species-wide ('hypothesis-agnostic') reference sketches using MinHash and infers associated genotypes based on the closest match, including multi-locus sequence types, susceptibility profiles, virulence factors or other genome-associated features provided by the user. Unlike the original implementation in [`RASE`](https://github.com/c2-d2/rase-pipeline), `sketchy` does not use phylogenetic trees which has some downsides, e.g. for sublineage genotype predictions (see below). 

See the [latest docs](https://esteinig.github.io/sketchy) for install, usage and database building.

## Install

Cargo:

```
cargo install sketchy
```

BioConda:

```
conda install -c bioconda sketchy
```

[Release binaries](https://github.com/esteinig/sketchy/releases) available for download. Reference sketches can be constructed from local [assembly and genotype collections](https://esteinig.github.io/sketchy/#local-sketches). *S. aureus* reference sketches are available in the data availability section below.

## Strengths and limitations


* Reference sketches and genotype indices can be constructed easily from large genotype collections
* `Sketchy` requires few resources when using small sketch sizes (`s = 1000`) 
* `Sketchy` performs best on lineage predictions and lineage-wide genotypes from very few reads - we found that tens to hundreds of reads can often give a good idea of the close matches in the reference sketch (especially when inspecting the top matches using `--top`)

However:

* Clade-specific genotype resolution is not as good as when using phylogenetic guide trees (`RASE`)
* Sketch size can be increased to increase performance (`s = 10000`), but resources scale approximately linearly
* `Sketchy` genotype inference may be difficult for species with high rates of homologous recombination

## Data availability

* Reference sketches and genotype files (`s = 1000`, `s = 10000`, `k = 16`) for [*S. aureus*](https://cloudstor.aarnet.edu.au/plus/s/3EBgvXi6sVHW8Ne) (full genotypes including susceptibility predictions and other genotypes), *S. pneumoniae*, *K. pneumoniae*, *P. aeruginosa* and *Neisseria spp.* (MLST) can be found in the [data repository](https://cloudstor.aarnet.edu.au/plus/s/rL0RHYunqhRK3i1).
* Reference sketches for cross-validation on the simulated species data can be found in this [data repository](https://cloudstor.aarnet.edu.au/plus/s/7ICPoSru6s6EHNY); genome assemblies for all species extracted from the ENA reference collection are available in this [data repository](https://cloudstor.aarnet.edu.au/plus/s/Td3ahBCPP2YAhCU)
* Scripts to extract data from the ENA collections [Grace Blackwell et al.](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3001421) and compute reference metrics can be found in the [scripts directory](scripts/).
* Nanopore reads for the outbreak isolates and genotype surveillance panels in Papua New Guinea (Flongle, Goroka, sequential protocol) are available for download in the [data repository](https://cloudstor.aarnet.edu.au/plus/s/MFkirfq1N6uIosc). Raw sequence data (Illumina / ONT) is being uploaded to NCBI (PRJNA657380).

## Preprint

If you use `sketchy` for research and other applications, please cite:

>  Steinig et al. (2022) - Genomic neighbor typing for bacterial outbreak surveillance - bioRxiv 2022.02.05.479210; doi: https://doi.org/10.1101/2022.02.05.479210 


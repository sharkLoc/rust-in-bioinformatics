# vircov <a href='https://github.com/esteinig'><img src='docs/vircov.png' align="right" height="200"/></a>

![](https://img.shields.io/badge/version-0.8.0-black.svg)

Automated coverage statistics, genome recovery and subtyping for metagenomic diagnostics of viral infections from reads or alignments.

## Overview


**`v1.0.0`**

- [Install](#install)
- [Examples](#examples)
- [Concepts](#concepts)
- [Etymology](#etymology)

## Install

Anaconda installation with dependencies:

```
mamba create -n vircov -c esteinig vircov
```

Dependencies for full pipeline from reads:

* `bowtie2` | `minimap2` | `strobealign` 
* `samtools`
* `ivar` 

Source installation without dependencies:

```
git clone https://github.com/esteinig/vircov
cd vircov && cargo build --release 
```

## Usage

### Virus detection and whole genome recovery

```

```

### Virus population graphs and genomic neighbor typing

```

```

#### Reference databases and subtyping schemes

We make automatically updated [subtyping databases]() and parsed genotype annotation schemes available for a range of common viral pathogen, at least where data-sharing arrangements make this possible (e.g. NCBI- but not GISAID™-derived assemblies). Scheme extractions and release updates are checked and if necessary corrected by our bioinformatics team at the Victorian Infectious Diseases Reference Laboratory (VIDRL) in Melbourne.

## Concepts

### Low-abundance infections and coverage assessment for detection from reads

Definitive viral diagnosis from metagenomic clinical samples can be extremely challenging due to low sequencing depth, large amounts of host reads and low infectious titres.

One way to distinguish a positive viral diagnosis is to look at alignment coverage against one or multiple reference sequences. When only few reads map to the reference - and genome coverage is low - positive infections often display multiple distinct
alignment regions, as opposed to reads mapping to a single or few regions on the reference. [De Vries et al. (2021)](https://www.sciencedirect.com/science/article/pii/S1386653221000792) summarize this concept succinctly in this figure (adapted):

![devries](https://user-images.githubusercontent.com/12873366/158775480-447d847e-5b0d-487c-a39a-81bdf428e09d.png)

Positive calls in these cases can be made from coverage plots showing the distinct alignment regions and a minimum threshold on the number of regions is chosen by the authors (> 3). `Vircov` computes the number of distinct alignment regions as part of the genome recovery module.

### Genomic neighbor typing using viral population graphs

```

```

## Etymology

Not a very creative abbreviation of "virus coverage" but the little spectacles in the logo are a reference to [Rudolf Virchow](https://en.wikipedia.org/wiki/Rudolf_Virchow). His surname is pronounced like `vircov` if you mumble the terminal `v`.



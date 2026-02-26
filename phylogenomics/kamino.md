[![Cargo Build & Test](https://github.com/rderelle/kamino/actions/workflows/ci.yml/badge.svg)](https://github.com/rderelle/kamino/actions/workflows/ci.yml)
[![Clippy check](https://github.com/rderelle/kamino/actions/workflows/clippy.yml/badge.svg)](https://github.com/rderelle/kamino/actions/workflows/clippy.yml)
[![codecov](https://codecov.io/github/rderelle/kamino/graph/badge.svg?token=6B8WIGZL2F)](https://codecov.io/github/rderelle/kamino)
[![Crates.io](https://img.shields.io/crates/v/kamino-cli.svg)](https://crates.io/crates/kamino-cli)
[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](https://bioconda.github.io/recipes/kamino/README.html)

<br><br>
<p align="center">
  <img src="logo_kamino.svg" alt="kamino logo" width="400">
</p>

<br><br>

From the Spanish word for *path*.  

Builds an amino-acid alignment in a reference-free, alignment-free manner from a set of proteomes.  
Not ‘better’ than traditional marker-based pipelines, but simpler and faster to run.  
  
Typical usages range from between-species to within-phylum phylogenetic analyses (bacteria, archaea and eukaryotes).

<br>

---
## under the hood
kamino performs the following successive steps:
- lists proteome files from the input directory (-i or -I)
- recodes proteins with a 6-letters recoding scheme (-r)
- simplifies proteomes by pre-filtering proteins and discarding out-branching k-mers 
- builds a global assembly graph and identifies variant groups as described <a href="https://academic.oup.com/mbe/article/42/4/msaf077/8103706">here</a> (-d)
- converts variant group paths back to amino acids using a sliding window
- mask long polymorphism runs within variant groups (-m)
- filters variant groups by missing data and middle-length thresholds (-f and -l)
- extracts middle positions and incorporate 'constant' positions (-c)
- outputs the final amino acid alignment (-o)

---

## installation
You can either compile the code locally using rustc, or install a precompiled binary from Bioconda:

```bash
conda install bioconda::kamino
```

---

## running kamino
Input consists of proteome files in FASTA format (gzipped or not), with one file per sample. Files can be placed in a single directory (specified with the -i argument), or their paths can be provided in a tab-delimited file using -I.

A basic run using four threads can be performed with either of the following commands:
```bash
kamino -i <input_dir> -t 4
kamino -I <tabular_file> -t 4
```
---

## examples

All analyses were performed on a MacBook *M4 Pro* using v0.6.1 and 4 threads (other parameters set to default):  

| dataset                     | taxonomic diversity  | runtime (min) | memory (GB) | alignment size (aa) |
|-----------------------------|----------------------|---------------|-------------|---------------------|
| 50 *Mycobacterium*          | within-genera        | 0.1           | 0.7         | 24,678              |
| 400 *Mycobacterium*         | within-genera        | 0.5           | 2.5         | 21,011              |
| 50 Polyporales (fungi)      | within-order         | 0.3           | 3.8         | 29,483              |
| 165 Arthropoda              | within-phylum        | 1.1           | 8.5         | 13,002              |
| 55 Mammalia                 | within-class         | 1.6           | 8.1         | 334,108             |  

---

## FAQ

- **When not to use kamino?**
    * low diversity datasets (ie, within-species), for which genome-based approaches will be more powerful 
    * highly divergent datasets (eg, animal kingdom)
    * distant outgroup composed of a few isolates: these might have disproportionately more missing data

- **Is the output reproducible?**
<p>Yes, kamino is fully deterministic so will produce the exact same alignment for a given version, set of parameters and input proteomes.</p>

- **How to get more phylogenetic positions?**
<p>Increase the maximum depth of the graph traversal (-d) or lower the minimum proportion of isolates with amino acid per position (-f) if that is acceptable for downstream analyses.</p>

 

---

This codebase is provided under the MIT License. Some parts of the code were drafted using AI assistance.


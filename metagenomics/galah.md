<img src="images/galah_logo.png" alt="Galah logo" width="600"/>

- [Galah](#galah)
  - [Installation](#installation)
    - [Install through the bioconda package](#install-through-the-bioconda-package)
    - [Pre-compiled binary](#pre-compiled-binary)
    - [Compiling from source](#compiling-from-source)
    - [Development](#development)
    - [Dependencies](#dependencies)
  - [Usage](#usage)
    - [Precluster ANI](#precluster-ani)
  - [License](#license)

# Galah

[![Anaconda-Server Badge](https://anaconda.org/bioconda/galah/badges/version.svg)](https://anaconda.org/bioconda/galah)

Galah aims to be a more scalable metagenome assembled genome (MAG) dereplication
method. That is, it clusters microbial genomes together based on their average
nucleotide identity (ANI), and chooses a single member of each cluster as the
representative.

Galah uses a greedy clustering approach to speed up genome dereplication,
relative to e.g. [dRep](https://drep.readthedocs.io/), particularly when there
are many closely related genomes (i.e. >95% ANI). Generated cluster
representatives have 2 properties. If the ANI threshold was set to 99%, then:

1. Each representative is <99% ANI to each other representative.
2. All members are >=99% ANI to the representative.

If [CheckM](https://ecogenomics.github.io/CheckM/) genome qualities were
specified, then the clusters have an additional property:

3. Each representative genome has a better quality score than other members of
   the cluster. Each genome is assigned a quality score based on the formula
   `completeness-5*contamination-5*num_contigs/100-5*num_ambiguous_bases/100000`, which is reduced from a quality formula described in
  Parks et. al. 2020 https://doi.org/10.1038/s41587-020-0501-8.

If instead CheckM qualities were not provided, then the following holds instead:

3. Each representative genome was specified to galah before other members of the
   cluster.

The overall greedy clustering approach was largely inspired by the work of
Donovan Parks, as described in [Parks et. al. 2020](https://doi.org/10.1038/s41587-020-0501-8). It
operates in 3 steps. In the first step, genomes are assigned as representative
if no genomes of higher quality are >99% ANI. In the second step, each
non-representative genome is assigned to the representative genome it has the
highest ANI with.

## Installation

### Install through the bioconda package

Galah can be installed through the [bioconda](https://bioconda.github.io/) conda channel. After initial setup of conda and the bioconda channel, it can be installed with mamba (or conda) with:

```
mamba install galah
```

One can see [details of the galah recipe](https://bioconda.github.io/recipes/galah/README.html).

Galah can also be used indirectly through
[CoverM](https://github.com/wwood/CoverM) via its `cluster` subcommand, which is also available on bioconda.

### Pre-compiled binary

Galah can be installed by downloading statically compiled binaries, available on
the [releases page](https://github.com/wwood/Galah/releases).

Third party dependencies listed below are required for this method.

### Compiling from source

Galah can also be installed from source, using the cargo build system after
installing [Rust](https://www.rust-lang.org/).

```
cargo install galah
```
Third party dependencies listed below are required for this method.

### Development

To run an unreleased version of Galah, after installing
[Rust](https://www.rust-lang.org/):

```
git clone https://github.com/wwood/galah
cd galah
pixi run cargo run -- cluster ...etc...
```
Third party dependencies listed below are required for this method.

### Dependencies

For some advanced usage of Galah, 3rd party tools are required, which must be installed separately:

* skani v0.2.2 https://github.com/bluenote-1577/skani
* FastANI v1.34 https://github.com/ParBLiSS/FastANI

## Usage
For clustering a set of genomes at 99% ANI:
```
galah cluster --genome-fasta-files /path/to/genome1.fna /path/to/genome2.fna --output-cluster-definition clusters.tsv
```
There are several other options for specifying genomes, ANI cutoffs, etc.

For clustering a set of contigs at 99% ANI:
```
galah cluster --cluster-contigs --small-genomes --genome-fasta-files /path/to/contigs.fna --output-cluster-definition clusters.tsv
```

The full usage is described on the [manual page](https://wwood.github.io/galah/galah-cluster.html), which can be accessed on the command line running `galah cluster --full-help`.

### Precluster ANI
Similar to dRep, galah operates in two stages. In the first, a fast
pre-clustering distance ([finch](https://github.com/onecodex/finch-rs)
or [skani](https://github.com/bluenote-1577/skani)) is
calculated between each pair of genomes. Genome pairs are only considered as
potentially in the same cluster with [skani](https://github.com/bluenote-1577/skani) or
[FastANI](https://github.com/ParBLiSS/FastANI) if the prethreshold ANI is
greater than the specified value. By default, the precluster ANI is set at 95%
and the final ANI is set at 99%.

## License

Galah is made available under GPL3+. See LICENSE.txt for details. Copyright Ben
Woodcroft.

Developed by Ben Woodcroft at the [Centre for Microbiome Research, Queensland University of Technology](https://www.qut.edu.au/health/schools/school-of-biomedical-sciences/centre-for-microbiome-research).

[galah]: Eolophus_roseicapilla_-Wamboin,_NSW,_Australia_-juvenile-8.smaller.jpg


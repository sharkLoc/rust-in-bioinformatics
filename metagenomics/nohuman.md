# NoHuman

[![Rust CI](https://github.com/mbhall88/nohuman/actions/workflows/ci.yaml/badge.svg)](https://github.com/mbhall88/nohuman/actions/workflows/ci.yaml)
[![Crates.io](https://img.shields.io/crates/v/nohuman.svg)](https://crates.io/crates/nohuman)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![github release version](https://img.shields.io/github/v/release/mbhall88/nohuman)](https://github.com/mbhall88/nohuman/releases)
[![DOI:10.1093/gigascience/giae010](https://img.shields.io/badge/citation-10.1093/gigascience/giae010-blue)][paper]

👤🧬🚫 **Remove human reads from a sequencing run** 👤🧬️🚫

`nohuman` removes human reads from sequencing reads by classifying them with [kraken2][kraken] against a custom database
built from all of the genomes in the Human Pangenome Reference Consortium's (
HPRC) [second release](https://humanpangenome.org/hprc-data-release-2/). It can take any type of
sequencing technology. Read more about the development of this method [here][paper].

- [NoHuman](#nohuman)
    - [Install](#install)
        - [Conda (recommended)](#conda-recommended)
        - [Precompiled binary](#precompiled-binary)
        - [Cargo](#cargo)
        - [Container](#container)
            - [`apptainer`](#apptainer)
            - [`docker`](#docker)
        - [Build from source](#build-from-source)
    - [Usage](#usage)
        - [Download the database](#download-the-database)
        - [Check dependencies are available](#check-dependencies-are-available)
        - [Remove human reads](#remove-human-reads)
        - [Keep human reads](#keep-human-reads)
        - [Full usage](#full-usage)
    - [Alternates](#alternates)
    - [Cite](#cite)

## Install

### Conda (recommended)

[![Conda (channel only)](https://img.shields.io/conda/vn/bioconda/nohuman)](https://anaconda.org/bioconda/nohuman)
[![bioconda version](https://anaconda.org/bioconda/nohuman/badges/platforms.svg)](https://anaconda.org/bioconda/nohuman)
![Conda Downloads](https://img.shields.io/conda/d/bioconda/nohuman)

```shell
$ conda install -c bioconda nohuman
```

### Precompiled binary

![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/mbhall88/nohuman/total)

> [!IMPORTANT]
> You will need to [install kraken2][kraken] yourself using this install method.

```shell
curl -sSL nohuman.mbh.sh | sh
# or with wget
wget -nv -O - nohuman.mbh.sh | sh
```

You can also pass options to the script like so

```
$ curl -sSL nohuman.mbh.sh | sh -s -- --help
install.sh [option]

Fetch and install the latest version of nohuman, if nohuman is already
installed it will be updated to the latest version.

Options
        -V, --verbose
                Enable verbose output for the installer

        -f, -y, --force, --yes
                Skip the confirmation prompt during installation

        -p, --platform
                Override the platform identified by the installer [default: apple-darwin]

        -b, --bin-dir
                Override the bin installation directory [default: /usr/local/bin]

        -a, --arch
                Override the architecture identified by the installer [default: x86_64]

        -B, --base-url
                Override the base URL used for downloading releases [default: https://github.com/mbhall88/nohuman/releases]

        -h, --help
                Display this help message
```

### Cargo

![Crates.io](https://img.shields.io/crates/d/nohuman)

> [!IMPORTANT]
> You will need to [install kraken2][kraken] yourself using this install method.

```shell
$ cargo install nohuman
```

### Container

Docker images are hosted on the GitHub Container registry.

#### `apptainer`

Prerequisite: [`apptainer`][apptainer] (previously `singularity`)

```shell
$ URI="docker://ghcr.io/mbhall88/nohuman:latest"
$ apptainer exec "$URI" nohuman --help
```

The above will use the latest version. If you want to specify a version then use a
[tag][ghcr] like so.

```shell
$ VERSION="0.2.1"
$ URI="docker://ghcr.io/mbhall88/nohuman:${VERSION}"
```

#### `docker`

Prerequisite: [`docker`][docker]

```shell
$ docker pull ghcr.io/mbhall88/nohuman:latest
$ docker run ghcr.io/mbhall88/nohuman:latest nohuman --help
```

You can find all the available tags [here][ghcr].

### Build from source

> [!IMPORTANT]
> You will need to [install kraken2][kraken] yourself using this install method.

```shell
$ git clone https://github.com/mbhall88/nohuman.git
$ cd nohuman
$ cargo build --release
$ target/release/nohuman -h
```

## Usage

### Download the database

`nohuman` now keeps a manifest of the available Kraken2 databases so you can install as many versions as you want.

List the available versions (the default is always the most recent dataset, currently `HPRC.r2` that includes the
latest Human Pangenome Reference genomes):

```
$ nohuman --list-db-versions
```

Download the default (latest) database:

```
$ nohuman --download
```

Download a specific version or fetch every available release:

```
$ nohuman --download --db-version HPRC.r1
$ nohuman --download --db-version all
```

By default, databases are cached under `$HOME/.nohuman/db/<version>`. When you run `nohuman` without any additional
options it will automatically choose the newest database you have installed. Use `--db-version` to pin a specific
version, or `--db` to point at a directory that already contains a Kraken2 database (for example, a shared install):

```
$ nohuman --db-version HPRC.r1 -t 4 in.fq
$ nohuman --db /data/my_kraken_db -t 4 in.fq
```

> [!TIP]
> Set the `NOHUMAN_DB` environment variable to override the default database location for every command without having to
> pass `--db` each time.

### Check dependencies are available

```
$ nohuman -c
[2023-12-14T04:10:46Z INFO ] All dependencies are available
```

### Remove human reads

```
$ nohuman -t 4 in.fq
```

this will pass 4 threads to kraken2 and output the clean reads as `in.nohuman.fq`.

You can specify where to write the output file with `-o`

```
$ nohuman -t 4 -o clean.fq in.fq
```

If you have paired-end Illumina reads

```
$ nohuman -t 4 in_1.fq in_2.fq
```

or to specify a different path for the output

```
$ nohuman -t 4 --out1 clean_1.fq --out2 clean_2.fq in_1.fq in_2.fq
```

Set a [minimum confidence score][conf] for kraken2 classifications

```
$ nohuman --conf 0.5 in.fq
```

or write the kraken2 read classification output to a file

```
$ nohuman -k kraken.out in.fq
```

or write the kraken2 [sample report](https://github.com/DerrickWood/kraken2/blob/master/docs/MANUAL.markdown#sample-report-output-format) to file

```
$ nohuman -r kraken.report in.fq
```

> [!TIP]
> Compressed output will be inferred from the specified output path(s). If no output path is provided, the same
> compression as the input will be used. To override the output compression format, use the `--output-type` option. 
> Supported compression formats are gzip (`.gz`), zstandard (`zst`), bzip2 (`.bz2`), and xz (`.xz`). If multiple threads are provided, these
> will be used for compression of the output (where possible).

### Keep human reads

You can invert the functionality of `nohuman` to keep only the human reads by using the `--human/-H` flag.

```
$ nohuman -h
Remove human reads from a sequencing run

Usage: nohuman [OPTIONS] [INPUT]...

Arguments:
  [INPUT]...  Input file(s) to remove human reads from

Options:
  -o, --out1 <OUTPUT_1>       First output file.
  -O, --out2 <OUTPUT_2>       Second output file.
  -c, --check                 Check that all required dependencies are available and exit
  -d, --download              Download the database
  -D, --db <PATH>             Path to the database [default: /home/michael/.nohuman/db]
      --db-version <VERSION>  Name of a downloaded database version to use (use `all` with
                              `--download` to fetch every version)
      --list-db-versions      List available database versions and exit
  -F, --output-type <FORMAT>  Output compression format. u: uncompressed; b: Bzip2; g: Gzip; x: Xz (Lzma); z: Zstd
  -t, --threads <INT>         Number of threads to use in kraken2 and optional output compression. Cannot be 0 [default: 1]
  -H, --human                 Output human reads instead of removing them
  -C, --conf <[0, 1]>         Kraken2 minimum confidence score [default: 0.0]
  -k, --kraken-output <FILE>  Write the Kraken2 read classification output to a file  
  -r, --kraken-report <FILE>  Write the Kraken2 report with aggregate counts/clade to file    
  -v, --verbose               Set the logging level to verbose
  -h, --help                  Print help (see more with '--help')
  -V, --version               Print version
```

### Full usage

```
$ nohuman --help
Remove human reads from a sequencing run

Usage: nohuman [OPTIONS] [INPUT]...

Arguments:
  [INPUT]...
          Input file(s) to remove human reads from

Options:
  -o, --out1 <OUTPUT_1>
          First output file.

          Defaults to the name of the first input file with the suffix "nohuman" appended.
          e.g. "input_1.fastq" -> "input_1.nohuman.fq".
          Compression of the output file is determined by the file extension of the output file name.
          Or by using the `--output-type` option. If no output path is given, the same compression
          as the input file will be used.

  -O, --out2 <OUTPUT_2>
          Second output file.

          Defaults to the name of the first input file with the suffix "nohuman" appended.
          e.g. "input_2.fastq" -> "input_2.nohuman.fq".
          Compression of the output file is determined by the file extension of the output file name.
          Or by using the `--output-type` option. If no output path is given, the same compression
          as the input file will be used.

  -c, --check
          Check that all required dependencies are available and exit

  -d, --download
          Download the database

  -D, --db <PATH>
          Path to the database

          [default: ~/.nohuman/db]

      --db-version <VERSION>
          Name of a downloaded database version to use (use `all` with `--download` to fetch every version)

      --list-db-versions
          List available database versions and exit

  -F, --output-type <FORMAT>
          Output compression format. u: uncompressed; b: Bzip2; g: Gzip; x: Xz (Lzma); z: Zstd

          If not provided, the format will be inferred from the given output file name(s), or the
          format of the input file(s) if no output file name(s) are given.

  -t, --threads <INT>
          Number of threads to use in kraken2 and optional output compression. Cannot be 0

          [default: 1]

  -H, --human
          Output human reads instead of removing them
          
  -C, --conf <[0, 1]>
          Kraken2 minimum confidence score

          [default: 0.0]
          
  -k, --kraken-output <FILE>
          Write the Kraken2 read classification output to a file
         
  -r, --kraken-report <FILE>
          Write the Kraken2 report with aggregate counts/clade to file 
          
  -v, --verbose
          Set the logging level to verbose

  -h, --help
          Print help (see a summary with '-h')

  -V, --version
          Print version
```

## Alternates

[Hostile](https://github.com/bede/hostile) is an alignment-based approach that performs well. It take longer and uses
more memory than the `nohuman` kraken approach, but has slightly better accuracy for Illumina data. See the [paper] for
more details and for other alternate approaches.

## Cite

[![DOI:10.1093/gigascience/giae010](https://img.shields.io/badge/citation-10.1093/gigascience/giae010-blue)][paper]

> Hall, Michael B., and Lachlan J. M. Coin. “Pangenome databases improve host removal and mycobacteria classification
> from clinical metagenomic data” GigaScience, April 4, 2024. <https://doi.org/10.1093/gigascience/giae010>

```bibtex
@article{hall_pangenome_2024,
	title = {Pangenome databases improve host removal and mycobacteria classification from clinical metagenomic data},
	volume = {13},
	issn = {2047-217X},
	url = {https://doi.org/10.1093/gigascience/giae010},
	doi = {10.1093/gigascience/giae010},
	urldate = {2024-04-07},
	journal = {GigaScience},
	author = {Hall, Michael B and Coin, Lachlan J M},
	month = jan,
	year = {2024},
	pages = {giae010},
}

```

[quay.io]: https://quay.io/repository/mbhall88/nohuman

[apptainer]: https://github.com/apptainer/apptainer

[docker]: https://docs.docker.com/v17.12/install/

[kraken]: https://github.com/DerrickWood/kraken2

[paper]: https://doi.org/10.1093/gigascience/giae010

[ghcr]: https://github.com/mbhall88/nohuman/pkgs/container/nohuman

[conf]: https://github.com/DerrickWood/kraken2/blob/master/docs/MANUAL.markdown#confidence-scoring


[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/natir/fpa/blob/master/LICENSE)
![CI](https://github.com/natir/fpa/workflows/CI/badge.svg)
[![CodeCov](https://codecov.io/gh/natir/fpa/branch/master/graph/badge.svg)](https://codecov.io/gh/natir/fpa)

# fpa Filter Pairwise Alignment 🧬 💻

Filter output of all-against-all read mapping, you filter or select:

- internal match
- containment
- dovetails
- self matching
- read name match against regex
- length of overlap
- length of read in overlap

For internal match, containment, dovetails definition go read [algorithm 5 in minimap article](https://academic.oup.com/bioinformatics/article/32/14/2103/1742895/Minimap-and-miniasm-fast-mapping-and-de-novo)

- [Rationale](#rationale)
- [Usage](#usage)
- [Requirements](#requirements)
- [Instalation](#instalation)
- [Minimum supported Rust version](#minimum-supported-rust-version)
- [Citation](#citation)

## Rationale

Long Read mapping tools provides all match they found in read dataset, for many usage some of match aren't useful, this programme provide some filter to remove it.
This soft can be replace by a simple script in awk, bash, python, ~perl~, {your favorite language}.

More details and some experiment are present in this [blog post](https://blog.pierre.marijon.fr/binary-mapping-format/). We have evaluated the effects of some fpa filter on miniasm assemblies, you can find scripts and how to get the real data sets in [this repository](https://gitlab.inria.fr/pmarijon/yacrd-and-fpa-upstream-tools-for-lr-genome-assembly).

## Usage

```
fpa -i <input> -o <output> <option> <subcommand: drop | keep | index | rename | gfa>
```

Subcommand can be split in two group:
- filters (drop, keep), select wich overlap are write in output
- generators (index, rename, gfa), generate new data from overlap

By default input and output are stdin and stdout so you can use like this:

```
minimap2 long_read.fasta long_read.fasta | fpa keep -d | gzip - > only_dovetail.paf.gz
minimap2 long_read.fasta long_read.fasta | fpa drop -l 500 -L 2000 > only_between_500_2000.paf
minimap2 long_read.fasta long_read.fasta | fpa drop -m -n read_1 > no_self_no_match_read_1.paf
minimap2 long_read.fasta long_read.fasta | fpa drop -m rename -o rename.csv > no_self_match_renamed.paf
minimap2 long_read.fasta long_read.fasta | fpa drop -m rename -o rename.csv gfa -o no_self_match_renamed.gfa > no_self_match_renamed.paf
minimap2 long_read.fasta long_read.fasta | fpa drop -l 500 index -t query -f match_upper_500.paf.idx query > match_upper_500.paf
minimap2 long_read.fasta long_read.fasta | fpa -o match_upper_500.paf.bz2 -z bzip2 drop -l 500 index -f match_upper_500.paf.idx -t target
```

### Generators

Only the mapping passed the filters are analyse by generators

#### Rename

The rename subcommand replaces the name of the read with another one.

If you use `-i` option the file will be read as a two-column csv, the first column is the original name and the second corresponds to the new name:
```
original name1, new name1
original name2, new name2
```

If the name of the read does not exist in the file it will not be replaced.

If you use `-o`, the names will automatically be replaced by a number a file like above example will be created.

#### Index

fpa can build an index of offset of the records in the file where a reads appears.

The index file looks like this:
```
read_id1, start_of_range_1:end_of_range_1; start_of_range_2:end_of_range_2;…
read_id2, start_of_range_1:end_of_range_1; start_of_range_2:end_of_range_2;…
```

fpa can index read only when it's query (first read in record) or target (second read in record) or both of them.

#### Gfa

fpa can generate an overlap graph with overlap pass filters

## Requirements

- [Rust](https://www.rust-lang.org/)
- libgz
- libbzip2
- liblzma

## Instalation

### With cargo

If you have a rust environment setup you can run :

```
cargo install fpa_lr
```

### With conda

fpa is avaible in [bioconda channel](https://bioconda.github.io/)

if bioconda channel is setup you can run :

```
conda install fpa
```

### From source

```
git clone https://github.com/natir/fpa.git
cd fpa
git checkout v0.5.1

cargo build
cargo test
cargo install
```

## Minimum supported Rust version

Currently the minimum supported Rust version is 1.56.0.

## Citation

If you use fpa in your research, please cite the following publication:

```
Pierre Marijon, Rayan Chikhi, Jean-Stéphane Varré, yacrd and fpa: upstream tools for long-read genome assembly, Bioinformatics, btaa262, https://doi.org/10.1093/bioinformatics/btaa262
```

bibtex format:
```
@article {@article{Marijon_2020,
	doi = {10.1093/bioinformatics/btaa262},
	url = {https://doi.org/10.1093%2Fbioinformatics%2Fbtaa262},
	year = 2020,
	month = {apr},
	publisher = {Oxford University Press ({OUP})},
	author = {Pierre Marijon and Rayan Chikhi and Jean-St{\'{e}}phane Varr{\'{e}}},
	editor = {Inanc Birol},
	title = {yacrd and fpa: upstream tools for long-read genome assembly},
	journal = {Bioinformatics}
}
```


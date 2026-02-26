[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/koesterlab/alignoth/rust.yml?branch=main&label=tests)](https://github.com/koesterlab/alignoth/actions)
[![codecov](https://codecov.io/gh/alignoth/alignoth/branch/main/graph/badge.svg?token=G751JNS6PU)](https://codecov.io/gh/koesterlab/alignoth)
[![Bioconda downloads](https://img.shields.io/conda/dn/bioconda/alignoth.svg?style=flat)](http://bioconda.github.io/recipes/alignoth/README.html)
[![Bioconda version](https://img.shields.io/conda/vn/bioconda/alignoth.svg?style=flat)](http://bioconda.github.io/recipes/alignoth/README.html)
[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat)](http://bioconda.github.io/recipes/alignoth/README.html)
[![Licence](https://img.shields.io/conda/l/bioconda/alignoth.svg?style=flat)](http://bioconda.github.io/recipes/alignoth/README.html)
[![DOI](https://img.shields.io/badge/DOI-10.1093%2Fbioinformatics/btaf663-blue.svg)](https://doi.org/10.1093/bioinformatics/btaf663)
[![DOI](https://zenodo.org/badge/478152744.svg)](https://doi.org/10.5281/zenodo.15837719)

# alignoth

A tool for creating alignment plots from bam files. The generated [vega-lite](https://vega.github.io/vega-lite/) plots are written to stdout per default.
An example of a generated plot can be seen [here](https://alignoth.github.io/preview.html).
The name alignoth is derived from the visualized **align**ments combined with the star **alioth** (usage of vega plots).

Alignoth supports an interactive mode that can be activated by simply executing it without any arguments (i.e. `alignoth`).
This launches a wizard that guides you through selecting input files, defining the region of interest, and choosing between an interactive HTML output or a Vega-Lite specification.

## Usage

```alignoth```

To activate the interactive mode guiding you through the process of creating an alignment plot.

```alignoth -b path/to/my.bam -r path/to/my/reference.fa -g chr1:200-300 > plot.vl.json```

To directly generate a plot in svg, png or pdf format we advice using the [vega-cli](https://vega.github.io/vega/usage/#cli) and [vega-lite-cli]( https://vega.github.io/vega-lite/usage/compile.html#cli) packages:

```alignoth -b path/to/my.bam -r path/to/my/reference.fa -g chr1:200-300 | vl2vg | vg2pdf > plot.pdf```

To generate an interactive view within an html file use `--html` and capture the output to a file:

```alignoth -b path/to/my.bam -r path/to/my/reference.fa -g chr1:200-300 --html > plot.html```

### Arguments

The following options are available when using alignoth:

| argument              | short | explanation                                                                                                                                                       | default |
|-----------------------|-------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| bam-path              | -b    | The bam file to be visualized.                                                                                                                                    |         |
| reference             | -r    | The path to the reference fasta file                                                                                                                              |         |
| region                | -g    | Chromosome and region for the visualization. Example: 2:132424-132924                                                                                             |         |
| around                | -a    | A chromosome and a base position that will define the region that will be plotted starting 500bp before and end 500bp behind the given position. Example: 2:17348 |         |
| highlight             | -h    | Named intervals or single base positions that will be highlighted in the visualization. Example: myinterval:132400-132500 or myvariant:132440                     |         |
| vcf                   | -v    | Path to a VCF file. Variants from the VCF file will be highlighted in the resulting plot similar to the highlight option.                                         |         |
| bed                   | -b    | Path to a BED file. Regions from the BED file will be highlighted in the resulting plot similar to the highlight option.                                          |         |
| plot-all              | -p    | Plot all reads in the given region. We advise to only use this command for small bam files with a single target.                                                  | false   |
| max-read-depth        | -d    | Set the maximum rows of reads that will be shown in the alignment plots                                                                                           | 500     |
| max-width             | -w    | Set the maximum width of the resulting alignment plot                                                                                                             | 1024    |
| output                | -o    | If present, data and vega-lite specs of the generated plot will be split and written to the given directory                                                       |         |
| data-format           | -f    | Sets the output format for the read, reference and highlight data                                                                                                 | json    |
| aux_tag               | -x    | Displays the given content of the aux tag in the tooltip of the plot. Multiple usage for more than one tag is possible.                                           |         |
| spec-output           |       | If present vega-lite specs will be written to the given file path                                                                                                 |         |
| read-data-output      |       | If present read data will be written to the given file path                                                                                                       |         |
| ref-data-output       |       | If present reference data will be written to the given file path                                                                                                  |         |
| highlight-data-output |       | If present highlight data will be written to the given file path                                                                                                  |         |
| coverage-data-output  |       | If present coverage data will be written to the given file path                                                                                                   |         |
| html                  |       | If present the generated plot will inserted into a plain html file containing the plot centered which is then written to stdout                                   |         |
| no-embed-js           |       | If present, the generated html will not embed javscript dependencies and therefore be considerably smaller but require internet access to load the dependencies.  | false   |
| around-vcf-record     | -a    | Plots a region around a specified VCF record taken via its index from the VCF file given via the --vcf option.                                                    |         |
| mismatch-display-min-percent |     | The minimum percentage of mismatches to display in the coverage plot.                                                                                        | 1       |


## Installation

There a multiple ways to install alignoth:

#### Pixi

Alignoth can be easily installed globally using [pixi](https://pixi.sh/):

    pixi global install alignoth

#### Bioconda

Rust-Bio-Tools is available via [Bioconda](https://bioconda.github.io).
With Bioconda set up, installation is as easy as

    conda install alignoth -c conda-forge -c bioconda -c nodefaults

Pay attention to the correct channel ordering for the installation.

#### Cargo

If the [Rust](https://www.rust-lang.org/tools/install) compiler and associated [Cargo](https://github.com/rust-lang/cargo/) are installed, alignoth may be installed via

    cargo install alignoth

#### Source

Download the source code and within the root directory of source run

    cargo install

## Authors

* [Felix Wiegand](https://github.com/fxwiegand)
* [Johannes Köster](https://github.com/johanneskoester) (https://koesterlab.github.io)


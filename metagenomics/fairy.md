# fairy - fast approximate contig coverage for metagenomic binning

**Fairy** computes **multi-sample** contig coverage for metagenome-assembled genome (MAG) binning. 

Fairy is used after metagenomic assembly and before binning. It can

* Calculate coverage 100x-1000x faster than read alignment (e.g. BWA) 
* Give comparable bins for **multi-sample** binning (short read or nanopore reads)
* Output formats that are compatible with MetaBAT2, MaxBin2, SemiBin2, and more

**Caveats**: 

* Don't use fairy for single-sample binning
* Don't use fairy for PacBio HiFi

> [!NOTE]  
> See [here for results and additional information/context about fairy](https://github.com/bluenote-1577/fairy/wiki/Introduction-to-fairy).

##  Install (current version v0.5.7)

#### Option 1: conda install 
[![Anaconda-Server Badge](https://anaconda.org/bioconda/fairy/badges/version.svg)](https://anaconda.org/bioconda/fairy)
[![Anaconda-Server Badge](https://anaconda.org/bioconda/fairy/badges/latest_release_date.svg)](https://anaconda.org/bioconda/fairy)

```sh
mamba install -c bioconda fairy
# conda install -c bioconda fairy
```

#### Option 2: Build from source

Requirements:
1. [rust](https://www.rust-lang.org/tools/install) (version > 1.63) programming language and associated tools such as cargo are required and assumed to be in PATH.
2. A c compiler (e.g. GCC)
3. make
4. cmake

Building takes a few minutes (depending on # of cores).

```sh
git clone https://github.com/bluenote-1577/fairy
cd fairy

# If default rust install directory is ~/.cargo
cargo install --path . 
fairy -h 
```
#### Option 3: Pre-built x86-64 linux statically compiled executable

If you're on an x86-64 Linux system, you can download the binary and use it without any installation. 

```sh
wget https://github.com/bluenote-1577/fairy/releases/download/latest/fairy
chmod +x fairy
./fairy -h
```

Note: the binary is compiled with a different set of libraries (musl instead of glibc), probably impacting performance. 

## Quick start

### Step 1: Index reads
```sh
# sketch/index short reads
fairy sketch -1 *_1.fastq.gz -2 *_2.fastq.gz -d sketch_dir

# sketch/index long reads
fairy sketch -r long_reads.fq -d sketch_dir

# rename the sketches if filenames are identical
fairy sketch -r dir1/reads.fq dir2/reads.fq -S sample1 sample2 -d sketch_dir
```

### Step 2: Calculate coverage
```sh
# calculate coverage
fairy coverage sketch_dir/*.bcsp contigs1.fa -t 10 -o coverage1.tsv
fairy coverage sketch_dir/*.bcsp contigs2.fa -t 10 -o coverage2.tsv
```

### Step 3: Bin
```sh
# default format is compatible with metabat2
metabat2 -i contigs1.fa -a coverage1.tsv ...
metabat2 -i contigs2.fa -a coverage2.tsv ...

# maxbin2 (requires different options; see below)
maxbin2 ...

# SemiBin2 (requires different options; see below)
SemiBin2 single_easy_bin -i contigs1.fa -a cov_aemb_1.tsv cov_aemb_2.tsv ...

```
## Output

### MetaBAT2 format (default)

The default output is compatible with the `jgi_summarize_bam_contig_depths` script from MetaBAT2 (the column names are different, however). 

```sh
contigName  contigLen  totalAvgDepth  reads1.fq  reads1.fq-var  reads2.fq  reads2.fq-var  ...
contig_1    38370      1.4            1.4        1.1100          0       0
...
```

1. First three columns give the name, the length, and average coverage.
2. The next columns are `mean coverage` and `coverage variance` for each sample.

The above output can be fed directly into MetaBAT2 with default parameters. 

### SemiBin2 format (--aemb-format option)

Since fairy v0.5.5 and [SemiBin v2.1](https://github.com/BigDataBiology/SemiBin), you can use SemiBin as follows

```sh
fairy coverage contigs1.fa reads1.bcsp --aemb-format -o cov_aemb1.tsv
fairy coverage contigs1.fa reads2.bcsp --aemb-format -o cov_aemb2.tsv
...
SemiBin2 single_easy_bin -i contigs.fa cov_aemb*.tsv -o results 
```
> [!TIP]
> **Fairy usage for SemiBin2 is different than other tools**: SemiBin2 requires *separate* coverage files for each read sample -- other tools require a *single coverage matrix*. 

### MaxBin2 format

Alternatively, `--maxbin-format` works directly with MaxBin2 and is also available. This removes the variance columns as well as the `contigLen` and `totalAvgDepth` columns. 

## Citing fairy

Jim Shaw, Yun William Yu. Fairy: fast approximate coverage for multi-sample metagenomic binning (2024). Microbiome.


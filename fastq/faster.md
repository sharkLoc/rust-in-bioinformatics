![Rust](https://github.com/angelovangel/faster/workflows/Rust/badge.svg)
# faster

A (very) fast program for getting statistics and features from a fastq file, in a usable form, written in Rust.

## Description

I wrote this program to get *fast* and *accurate* statistics about a fastq file, formatted as a tab-delimited table. In addition, it can do the following with a fastq file:

- get the read lengths
- get gc content per read
- get geometric mean of phred scores per read
- get NX values for all the reads, e.g. N50
- filter reads based on length (both greater than and smaller than a desired length)
- subsample reads (by proportion of all reads in the file)
- trim front and trim tail - trim x number of bases from the beginning/end of each read
- regex search for reads containing a pattern in their description field

The motivation behind it:

- many of the tools out there are just wrong when it comes to calculating 'mean' phred scores (yes, just taking the arithmetic mean phred score is wrong)
- one simple executable doing one thing well, no dependencies
- it is straightforward to parse the output in other programs and the output is easy to tweak as desired
- reasonably fast
- can be easily run in parallel

## Install

Compiled binaries are provided for x86_64 Linux, macOS and Windows - download from the releases section and run. You will have to make the file executable (`chmod a+x faster`) and for MacOS, allow running external apps in your security settings. If you need to run it on something else (your phone?!), you will have to compile it yourself (which is pretty easy though). Below is an example on how to setup a Rust toolchain and compile `faster`:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
git clone https://github.com/angelovangel/faster.git

cd faster
cargo build --release

# the binary is now under ./target/release/, run it like this:
./target/release/faster -t /path/to/fastq/file.fastq.gz

```

## Usage and tweaking the output

The program takes one fastq/fastq.gz file as an argument and, when used with the `--table` flag, outputs a tab-separated table with statistics to stdout. There are options to obtain the length, GC-content, and 'mean' phred scores per read, or to filter reads by length, see `-help` for details.

```bash
# for help
faster --help # or -h

# get some N10, N50 and N90 values
for i in 0.1 0.5 0.9; do faster --nx $i /path/to/fastq/file.fastq; done

# get a table with statistics
faster -t /path/to/fastq/file.fastq

# for many files, with parallel
parallel faster -t ::: /path/to/fastq/*.fastq.gz

# again with parallel, but get rid of the table header
parallel faster -ts ::: /path/to/fastq/*.fastq.gz
```

The statistics output is a tab-separated table with the following columns:   
`file   reads   bases   n_bases   min_len   max_len   mean_len   Q1   Q2   Q3   N50 Q20_percent Q30_percent`

## Performance

To get an idea how `faster` compares to other tools, I have benchmarked it with two other popular programs and 3 different datasets. **I am aware that these tools have different and often much richer functionality (especially seqkit, I use it all the time), so these comparisons are for orientation only**. 
The benchmarks were performed with [hyperfine](https://github.com/sharkdp/hyperfine) (`-r 15 --warmup 2`) on a MacBook Pro with an 8-core 2.3 GHz Quad-Core Intel Core i5 and 8 GB RAM. For Illumina reads, `faster` is slightly slower than `seqstats` (written in C using the `klib` [library by Heng Li](https://github.com/attractivechaos/klib) - the fastest thing possible out there), and for Nanopore it is even a bit faster than `seqstats`. `seqkit stats` performs worse of the three tools tested, but bear in mind the extraordinarily rich functionality it has.

***
### dataset A - a small Nanopore fastq file with 37k reads and 350M bases

| Command | Mean [ms] | Min [ms] | Max [ms] | Relative |
|:---|---:|---:|---:|---:|
| `faster -t datasetA.fastq` | 398.1 ± 21.2 | 380.4 | 469.6 | 1.00 |
| `seqstats datasetA.fastq` | 633.6 ± 54.1 | 593.3 | 773.6 | 1.59 ± 0.16 |
| `seqkit stats -a datasetA.fastq` | 1864.5 ± 70.3 | 1828.7 | 2117.3 | 4.68 ± 0.31 |

***

### dataset B - a small Illumina fastq.gz file with ~100k reads

| Command | Mean [ms] | Min [ms] | Max [ms] | Relative |
|:---|---:|---:|---:|---:|
| `faster -t datasetB.fastq.gz` | 181.7 ± 2.3 | 177.7 | 184.6 | 1.36 ± 0.09 |
| `seqstats datasetB.fastq.gz` | 133.4 ± 8.4 | 125.7 | 154.2 | 1.00 |
| `seqkit stats -a datasetB.fastq.gz` | 932.6 ± 37.0 | 873.8 | 1028.9 | 6.99 ± 0.52 |

***

### dataset C - a small Illumina iSeq run, 11.5M reads and 1.7G bases, using `gnu parallel`

| Command | Mean [s] | Min [s] | Max [s] | Relative |
|:---|---:|---:|---:|---:|
| `parallel faster -t ::: *.fastq.gz` | 6.438 ± 0.384 | 6.009 | 7.062 | 1.43 ± 0.15 |
| `parallel seqstats ::: *.fastq.gz` | 4.488 ± 0.394 | 4.120 | 5.312 | 1.00 |
| `parallel seqkit stats -a ::: *.fastq.gz` | 40.156 ± 1.747 | 38.762 | 44.132 | 8.95 ± 0.88 |

***
## Reference

`faster` uses the excellent Rust-Bio library:

[Köster, J. (2016). Rust-Bio: a fast and safe bioinformatics library. Bioinformatics, 32(3), 444-446.](https://academic.oup.com/bioinformatics/article/32/3/444/1743419)
# oarfish: transcript quantification from long-read RNA-seq data

`oarfish` is a program, written in Rust (https://www.rust-lang.org/), for quantifying transcript-level expression from long-read (i.e. Oxford nanopore cDNA and direct RNA and PacBio) sequencing technologies. `oarfish` requires a sample of sequencing reads aligned to the _transcriptome_ (currntly not to the genome). It handles multi-mapping reads through the use of probabilistic allocation via an expectation-maximization (EM) algorithm.

It optionally employs many filters to help discard alignments that may reduce quantification accuracy. Currently, the set of filters applied in `oarfish` are directly derived from the [`NanoCount`](https://github.com/a-slide/NanoCount)[^Gleeson] tool; both the filters that exist, and the way their values are set (with the exception of the `--three-prime-clip` filter, which is not set by default in `oarfish` but is in `NanoCount`).

Additionally, `oarfish` provides options to make use of coverage profiles derived from the aligned reads to improve quantification accuracy. The use of this coverage model is enabled with the `--model-coverage` flag. You can read more about `oarfish`[^preprint] in the [preprint](https://www.biorxiv.org/content/10.1101/2024.02.28.582591v1). Please cite the preprint if you use `oarfish` in your work or analysis.

Also, please note that `oarfish` is scientific software in active development. Therefore, please check the [GitHub Release](https://github.com/COMBINE-lab/oarfish/releases) page to make sure that you are using the latest version

## Installation

`oarfish` can be installed in a variety of ways.

### Precompiled binaries

Binaries are available via [GitHub Releases](https://github.com/COMBINE-lab/oarfish/releases).

You can quickly install the latest release using the following helper script:

```sh
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/COMBINE-lab/oarfish/releases/latest/download/oarfish-installer.sh | sh
```

### Using `cargo`

If you have `cargo` installed, you can install `oarfish` directly from the source code:

```sh
cargo install oarfish
```

You can find the crate on [crates.io](https://crates.io/crates/oarfish).

### Bioconda

`oarfish` is available via [Bioconda](https://anaconda.org/bioconda/oarfish):

```sh
conda install -c bioconda oarfish
```

## Basic usage

The usage can be provided by passing `-h` at the command line.

```
A fast, accurate and versatile tool for long-read transcript quantification.

Usage: oarfish [OPTIONS] <--alignments <ALIGNMENTS>|--reads <READS>|--only-index>

Options:
      --quiet
          be quiet (i.e. don't output log messages that aren't at least warnings)
      --verbose
          be verbose (i.e. output all non-developer logging messages)
  -o, --output <OUTPUT>
          location where output quantification file should be written
      --single-cell
          input is assumed to be a single-cell BAM and to have the `CB:z` tag for all read records
  -j, --threads <THREADS>
          number of cores that oarfish will use during different phases of quantification. Note: This value will be at least 2 for bulk quantification and at least 3 for single-cell quantifi
cation due to the use of dedicated parsing threads [default: 3]
      --num-bootstraps <NUM_BOOTSTRAPS>
          number of bootstrap replicates to produce to assess quantification uncertainty [default: 0]
  -h, --help
          Print help
  -V, --version
          Print version

alignment mode:
  -a, --alignments <ALIGNMENTS>  path to the file containing the input alignments

raw read mode:
      --reads <READS>
          path to the file containing the input reads; these can be in FASTA/Q format (possibly gzipped), or provided in uBAM (unaligned BAM) format. The format will be inferred from the fil
e suffixes, and if a format cannot be inferred, it will be assumed to be (possibly gzipped) FASTA/Q
      --annotated <ANNOTATED>
          path to the file containing the annotated transcriptome (e.g. GENCODE) against which to map
      --novel <NOVEL>
          path to the file containing novel (de novo, or reference-guided assembled) transcripts against which to map. These are ultimately indexed together with reference transcripts, but p
assed in separately for the purposes of provenance tracking
      --index <INDEX>
          path to an existing minimap2 index (either created with oarfish, which is preferred, or with minimap2 itself)
      --seq-tech <SEQ_TECH>
          sequencing technology in which to expect reads if using mapping based mode [possible values: ont-cdna, ont-drna, pac-bio, pac-bio-hifi]
      --best-n <BEST_N>
          maximum number of secondary mappings to consider when mapping reads to the transcriptome [default: 100]
      --thread-buff-size <THREAD_BUFF_SIZE>
          total memory to allow for thread-local alignment buffers (each buffer will get this value / # of alignment threads) [default: 1GB]

indexing:
      --only-index             If this flag is passed, oarfish only performs indexing and not quantification. Designed primarily for workflow management systems. Note: A prebuilt index is no
t needed to quantify with oarfish; an index can be written concurrently with quantification using the `--index-out` parameter
      --index-out <INDEX_OUT>  path where minimap2 index will be written (if provided)

filters:
      --filter-group <FILTER_GROUP>
          [possible values: no-filters, nanocount-filters]
  -t, --three-prime-clip <THREE_PRIME_CLIP>
          maximum allowable distance of the right-most end of an alignment from the 3' transcript end [default: *4294967295]
  -f, --five-prime-clip <FIVE_PRIME_CLIP>
          maximum allowable distance of the left-most end of an alignment from the 5' transcript end [default: *4294967295]
  -s, --score-threshold <SCORE_THRESHOLD>
          fraction of the best possible alignment score that a secondary alignment must have for consideration [default: *0.95]
  -m, --min-aligned-fraction <MIN_ALIGNED_FRACTION>
          fraction of a query that must be mapped within an alignemnt to consider the alignemnt valid [default: *0.5]
  -l, --min-aligned-len <MIN_ALIGNED_LEN>
          minimum number of nucleotides in the aligned portion of a read [default: *50]
  -d, --strand-filter <STRAND_FILTER>
          only alignments to this strand will be allowed; options are (fw /+, rc/-, or both/.) [default: .]

coverage model:
      --model-coverage             apply the coverage model
  -k, --growth-rate <GROWTH_RATE>  if using the coverage model, use this as the value of `k` in the logistic equation [default: 2]
  -b, --bin-width <BIN_WIDTH>      width of the bins used in the coverage model [default: 100]

output read-txps probabilities:
      --write-assignment-probs[=<WRITE_ASSIGNMENT_PROBS>]
          write output alignment probabilites (optionally compressed) for each mapped read. If <WRITE_ASSIGNMENT_PROBS> is present, it must be one of `uncompressed` (default) or `compressed`
, which will cause the output file to be lz4 compressed

EM:
      --max-em-iter <MAX_EM_ITER>
          maximum number of iterations for which to run the EM algorithm [default: 1000]
      --convergence-thresh <CONVERGENCE_THRESH>
          maximum number of iterations for which to run the EM algorithm [default: 0.001]
  -q, --short-quant <SHORT_QUANT>
          location of short read quantification (if provided)
```

## Usage examples

Assume that you have ONT cDNA sequencing reads in a file named `sample1_reads.fq.gz`, and you'd like to quantify the transcripts in a *transcriptome* reference in the file `transcripts.fa`.
To accomplish this with oarfish, you can use either [alignment-based](index.md#alignment-based-input) or [read-based](index.md#read-based-input) mode.  Here we give a brief example
of each.  To use alignment-based mode, we assume you have [minimap2](https://github.com/lh3/minimap2) and [samtools](http://www.htslib.org/) installed.  

### aligment-mode example

You can quantify the transcript abundances in this sample using the following commands:

```{bash}
$ minimap2 -t 16 -ax map-ont transcripts.fa sample1_reads.fq.gz | samtools view -@4 -b -o alignments.bam
$ oarfish -j 16 -a alignments.bam -o sample1 --filter-group no-filters --model-coverage
```

This will produce several output files, as described [below](index.md#output).

### read-mode example

In read-based mode, you can quantify the transcript abundances in this sample using the following commands:

```{bash}
$ oarfish -j 16 --reads sample1_reads.fq.gz --annotated transcripts.fa --seq-tech ont-cdna -o sample1 --filter-group no-filters --model-coverage
```

If you are going to quantify more than one sample against these reference transcripts, it makes sense to save the minimap2 index that the above
command creates.  This can be done using the following command:

```{bash}
$ oarfish -j 16 --reads sample1_reads.fq.gz --annotated transcripts.fa --index-out transcripts.mmi --seq-tech ont-cdna -o sample1 --filter-group no-filters --model-coverage
```

Then, in subsequent runs (say when quantifying `sample2_reads.fq.gz`), you can directly provide the `minimap2` index in place of the reference to
speed up quantification.  That command would look like the following:

```{bash}
$ oarfish -j 16 --reads sample2_reads.fq.gz --index transcripts.mmi --seq-tech ont-cdna -o sample2 --filter-group no-filters --model-coverage
```

As with alignment-based mode, these commands will produce several output files, as described [below](index.md#output).


## Input to `oarfish`

`Oarfish` can accept as input either a `bam` file containing reads aligned to the transcriptome as specified [below](index.md#alignment-based-input), or
raw sequencing reads themselves (along with a reference transcriptome), which are then mapped to the reference using [minimap2-rs](https://github.com/jguhlin/minimap2-rs)
and subsequently processed with `oarfish`.  With equivalent alignment options, the results of these input modes should be equivalent, so which to use is therefore
based on the preference of the user.


### Read-based input

The read-based input mode takes as input reference transcript sequences (specified with the `--annotated` and `--novel` arguments) which are `FASTA` files containing transcriptome sequence.  The `--annotated` and `--novel` flags take care of the source of the underlying transcripts, as their provenance is tracked separately. It is recommended that you provide transcripts from known reference annotations (e.g. gencode) using the `--annotated` option, while you provide novel transcripts that may have beeen assembled from your samples using the `--novel` option. **Importantly**, how the transcripts are split between `--annotated` and `--novel` will have no effect on how the final quantification is performed, as the transcripts from both sources are joined and indexed together.  However, a separate sequence signature is kept and propagated to the output for each source, and mixing novel transcripts into the `--annotated` source may complicate attempts to automatically detect the reference annotation used in downstream tools.

Alternatively, you can provide `oarfish` with an index (built from a previous run of `oarfish`) to avoid re-indexing the same reference. You can also provide a pre-built `minimap2` index, though such an index will not be able to separately track `--annotated` and `--novel` transcripts.

Finally, you provide `orafish` with a set of reads (specified with the `--reads` argument) which should be a `FASTQ` file (possibly gzipped) or a `uBAM` file, and a `--seq-tech` argument specifying the sequencing technology 
type of the reads to be mapped.

The mapping between the potential values that can be passed to `oarfish`'s `--seq-tech` argument and the `minimap2` presets is as follows:

  - `oarfish` seq-tech `ont-cdna` corresponds to `minimap2` preset `map-ont`
  - `oarfish` seq-tech `ont-drna` corresponds to `minimap2` preset `map-ont`
  - `oarfish` seq-tech `pac-bio` corresponds to `minimap2` preset `map-pb`
  - `oarfish` seq-tech `pac-bio-hifi` corresponds to `minimap2` preset `map-hifi`

Given these inputs, `oarfish` will either load the pre-built `minimap2` index, or build one according to the parameter specified by `--seq-tech`, and will then align
the reads to this index using [`minimap2-rs`](https://github.com/jguhlin/minimap2-rs).  Optionally, the maximum multimapping rate (i.e. the number of secondary alignments 
corresponding to the `minimap2` parameter `-N`) can be specified with the command line parameter `--best-n`. The default value of this parameter is 100.

#### Read-based input formats

`oarfish` is capable of taking input in either `FASTA` format `FASTQ` format, or unaligned `BAM` (`uBAM`) format.  When you pass the raw reads to `oarfish` via the `--reads` flag, `oarfish` will attempt to infer the type of the input by looking at the file suffix.  If it matches one of `.fa`, `.fasta`, `.FA`, `.FASTA`, `.fq`, `.fastq`, `.FQ`, `.FASTQ`, `.fa.gz`, `.fasta.gz`, `.FA.GZ`, `.FASTA.GZ`, `.fq.gz`, `.fastq.gz`, `.FQ.GZ`, or `.FASTQ.GZ`, then the input file will be assumed to be an (appropriately compressed) `FASTA` or `FASTQ` format. Otherwise, if it ends in `.bam` or `.ubam` or `.BAM` or `.UBAM`, it will be assumed to be in `uBAM` format. If  the format cannot be inferred via the file suffix (e.g. if the file is being provided via process substitution), then an attempt will be made to parse it as a (possibly compressed) `FASTA`/`FASTQ` format file.

### Alignmment-based input

In alignment-based mode, `oarfish` processes pre-computed alignments of the read to the transcriptome. The input should be a `bam` format file, with reads aligned using [`minimap2`](https://github.com/lh3/minimap2) against the _transcriptome_. That is, `oarfish` does not currently handle spliced alignment to the genome. Further, the output alignments should be name sorted (the default order produced by `minimap2` should be fine). _Specifically_, `oarfish` relies on the existence of the `AS` tag in the `bam` records that encodes the alignment score in order to obtain the score for each alignment (which is used in probabilistic read assignment), and the score of the best alignment, overall, for each read. 

### Choosing `minimap2` alignment options 

Since the purpose of `oarfish` is to estimate transcript abundance from a collection of alignments to the target transcriptome, it is important that the alignments are generated in a fashion that is compatible with this goal.  Primarily, this means that the aligner should be configured to report as many optimal (and near-optimal) alignments as exist, so that `oarfish` can observe all of this information and determine how to allocate reads to transcripts.  We recommend using the following options with `minimap2` when aligning data for later processing by `oarfish` * For ONT data (either dRNA or cDNA): please use the flags `--eqx -N 100 -ax map-ont` For PacBio data: please use the flags `--eqx -N 100 -ax pacbio` **Note (1)**: It may be worthwile using an even larger `N` value (e.g. the [TranSigner manuscript](https://www.biorxiv.org/content/10.1101/2024.04.13.589356v1.full) recommends `-N 181`). A larger value should not diminish the accuracy of `oarfish`, but it may make alignment take longer and produce a larger `bam` file.

**Note (2)**: For very high quality PacBio data, it may be most appropriate to use the `-ax map-hifi` flag in place of `-ax pacbio`.  We are currently evaluating the effect of this option, and also welcome feedback if you have experiences to share on the use of data aligned with these different flags with `oarfish`.

## Other notes on `oarfish` parameters

The parameters above should be explained by their relevant help option, but the `-d`/`--strand-filter` is worth noting explicitly. By default, alignments to both strands of a transcript will be considered valid.  You can use this option to allow only alignments in the specified orientation; for example `-d fw` will allow only alignments in the forward orientation and `-d rc` will allow only alignments in the reverse-complement orientation and `-d both` (the default) will allow both.  The `-d` filter, if explicitly provided, overrides the orientation filter in any provided "filter group" so e.g. passing `--filter-group no-filters -d fw` will disable other filters, but will still only admit alignments in the forward orientation.

**In general**, if you apply a `filter-group`, the group options will be applied first and then any explicitly provided options given will override the corresponding option in the `filter-group`.

### Read-level assignment probabilities

`oarfish` has the ability to output read-level assignment probabilities.  That is, for each input read, what is the probability, conditioned on the final estimate of transcript abundances, that the read was sequenced from each transcript to which it aligned. By default, this information is not recorded (as it's not required, or commonly used, for most standard analyses). To enable this output, you should pass the `--write-assignment-probs` option to `oarfish`.  Optionally, you may also pass `--write-assignment-probs=compressed` to write the output to a compressed ([lz4](https://github.com/lz4/lz4)) stream --- the default
output is to an uncompressed text file.

The format of the read assignment probabilities is as follows --- where all fields below on a single line are `\t` delimited:

```
<m> <n>
<tname_1>
<tname_2>
...
<tname_m>
<rname_1> <k_1> <tid_11> <tid_21> ... <tid_{k_1}1> <p_11> <p_21> ... <p_{k_1}1>
...
<rname_n> <k_1> <tid_1n> <tid_2n> ... <tid_{k_n}n> <p_1n> <p_2n> ... <p_{k_n}n>
```

Here, `<m>` is the number of transcripts in the reference, `<n>` is the number of *mapped* reads. The following `m` lines consist of the names of the transcripts in the order they will be referred to in the file. The following `n` lines after that provide the actual alignment information and assignment probabilities for each read.

The format of each of these lines is as follows; `<rname>` is the name of the read, `<k>` is the number of alignments for which probabilities are reported (if it is determined an alignment is invalid under the model, it may not be reported). Subsequently, there is a list of `k` integers, and `k` floating point numbers. Each of the `k` integers is the index of some transcript in the list of `m` transcripts given at the start of the file, and the subsequent list of `k` floating point numbers are the assignment probabilities of this read to each of the transcripts.

For example:

```
5 3
txpA
txpB
txpC
txpD
txpE
readX 2 0 2 0.4 0.6
readY 3 1 3 4 0.1 0.2 0.7
readZ 1 4 1.0
```
 
This file provides an example with 5 reference transcripts and 3 mapped reads. The first read (readX) maps to transcripts 0 and 2 (so txpA and txpC) with probabilities 0.4 and 0.6 respectively. The next read (readY) maps to 3 transcripts, txpB, txpD and txpE with probabilities 0.1, 0.2, and 0.7 respectively. Finally, the last read (readZ) maps uniquely to transcript txpE with probability 1.

The compressed output (i.e. what is generated if one passes `--write-assignment-probs=compressed`) is exactly the same format, except instead of residing in a plain text file, it is written to an lz4 compressed text file.  You can either decompress this file first with an lz4 decompressor, or decompress it on-the-fly as you are parsing the file using the lz4 library in your favorite language.

## Notes about single-cell mode

Starting with version 0.6.1 `oarfish` incorporates the first single-cell quantification capabilities. Given a `bam` file, **collated by cell barcode and with already (UMI) deduplicated reads**, this mode, enabled with the `--single-cell` flag, will allow `oarfish` to produce a single-cell quantification matrix. Currently, this mode can not be used with read-based mode, and the input `bam` file should be properly formatted for this purpose. 

**Formatting requirements of BAM input in single-cell mode**: All alignment records for the same cell barcode should be adjacent in the `bam` file, and a count will be obtained for each read record, so UMI de-duplication should have been performed if those are the counts you want. In the future, counting UMIs directly may be supported, and some of these other restrictions may be lifted.

## Inferential Replicates

`oarfish` has the ability to compute [_inferential replicates_](https://academic.oup.com/nar/article/47/18/e105/5542870) of its quantification estimates. This is performed by bootstrap sampling of the original read mappings, and subsequently performing inference under each resampling.  These inferential replicates allow assessing the variance of the point estimate of transcript abundance, and can lead to improved differential analysis at the transcript level, if using a differential testing tool that takes advantage of this information. The generation of inferential replicates is controlled by the `--num-bootstraps` argument to `oarfish`.  The default value is `0`, meaning that no inferential replicates are generated.  If you set this to some value greater than `0`, the the requested number of inferential replicates will be generated. It is recommended, if generating inferential replicates, to run `oarfish` with multiple threads, since replicate generation is highly-parallelized. Finally, if replicates are generated, they are written to a [`Parquet`](https://parquet.apache.org/), starting with the specified output stem and ending with `infreps.pq`.

## Output

The `--output` option passed to `oarfish` corresponds to a path prefix (this prefix can contain the path separator character and if it refers to a directory that does not yeat exist, that directory will be created). Based on this path prefix, say `P`, `oarfish` will create 2 files:

  * `P.meta_info.json` - a JSON format file containing information about relevant parameters with which `oarfish` was run, and other relevant inforamtion from the processed sample apart from the actual transcript quantifications.
  * `P.quant` - a tab separated file listing the quantified targets, as well as information about their length and other metadata. The `num_reads` column provides the estimate of the number of reads originating from each target.
  * `P.infreps.pq` - a [`Parquet`](https://parquet.apache.org/) table where each row is a transcript and each column is an inferential replicate, containing the estimated counts for each transcript under each computed inferential replicate.
  * `P.ambig_info.tsv` - a tab separated file listing, for each transcript (in the same order in which they appear in `P.quant`) the number of uniquely mapped, ambiguously mapped, and total reads.  The quantification estimate for each transcript, in general, should reside between the number of uniquely aligned reads and the total number of reads (i.e. these provide, respectively lower and upper bounds for the number of reads assigned to each transcript).  Note that the total in this file is the total number of reads that align to this transcript with a sufficiently high alignment score --- it is _not_, in general, an estimate of the number of reads originating from this transcript as many of those reads can be multimapping and, in fact, potentially better described by other transcripts.
  * `P.prob[.lz4]` - a file encoding the assignment probability of each read to each transcript to which it had a valid alignment (optionally compressed using [`lz4`](https://github.com/lz4/lz4)). This file is optional and is generated only if `--write-assignment-probs` is passed to `oarfish`.

## References

[^Gleeson]: Josie Gleeson, Adrien Leger, Yair D J Prawer, Tracy A Lane, Paul J Harrison, Wilfried Haerty, Michael B Clark, Accurate expression quantification from nanopore direct RNA sequencing with NanoCount, Nucleic Acids Research, Volume 50, Issue 4, 28 February 2022, Page e19, [https://doi.org/10.1093/nar/gkab1129](https://doi.org/10.1093/nar/gkab1129)

[^preprint]: Zahra Zare Jousheghani, Rob Patro. Oarfish: Enhanced probabilistic modeling leads to improved accuracy in long read transcriptome quantification, bioRxiv 2024.02.28.582591; doi: [https://doi.org/10.1101/2024.02.28.582591](https://doi.org/10.1101/2024.02.28.582591)


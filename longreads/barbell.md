[![crates.io](https://img.shields.io/crates/v/barbell.svg)](https://crates.io/crates/barbell)
[![Conda version](https://img.shields.io/conda/v/bioconda/barbell?label=bioconda)](https://anaconda.org/bioconda/barbell)
[![biorXiv preprint](https://img.shields.io/badge/biorXiv-10.1101/2025.10.22.683865-green)](https://doi.org/10.1101/2025.10.22.683865)

# 🦀 Barbell — Pattern aware demux


## Why Barbell?

- **>1000× fewer trimming errors** compared to Dorado.
- Equivalent or **better assemblies**.
- **Contamination-free** assemblies by removing artefact reads.
- Easily applicable to **custom experiments**.
- Still **very fast**.

If you have any issues or if something is unclear, just create an [issue](https://github.com/rickbeeloo/barbell/issues).

---

## Quick links

- [Installing barbell](#installing-barbell)
- Workflow examples
  - [Quickstart using Nanopore kit](#quickstart)
  - [In-depth workflow for Nanopore kits](#in-depth-inspection-of-nanopore-kit-results)
  - [Custom experiment (simple)](#custom-experiment)
  - [Custom experiment (multi protocol)](#custom-experiment-with-mixed-sequences)
- [Understanding barbell](#understanding-barbell)
  - [What are barbell patterns?](#patterns)
  - [How to cut concat reads](#how-to-handle-concat-reads)
  - [Output column descriptions (annotate & filter)](#output-columns-annotate--filter)
- [Paper evals](#paper-evals)
- [Notes & tips](#notes--tips)

---

## Paper 
See the paper for more details on the Barbell scoring and comparisons with other tools:
> ### [Barbell Resolves Demultiplexing and Trimming Issues in Nanopore Data](https://doi.org/10.1101/2025.10.22.683865)
>
> **Rick Beeloo**, **Ragnar Groot Koerkamp**, **Xiu Jia**, **Marian J. Broekhuizen-Stins**, **Lieke van Ijken**, **Bas E. Dutilh**, **Aldert L. Zomer**  
> *bioRxiv*, 2025  
> [https://doi.org/10.1101/2025.10.22.683865](https://doi.org/10.1101/2025.10.22.683865)


---

## Installing Barbell
Barbell is written in Rust.

### Executables
Download the latest release from
[releases](https://github.com/rickbeeloo/barbell/releases). These are also
available via

``` bash
cargo binstall barbell
```
or via conda/mamba/pixi:

``` sh
conda install -c bioconda barbell
```

### From source (recommended)
Check whether Rust is installed:

```bash
rustc --version
```

If not install it via [rustup](https://rustup.rs/), more info in their
[docs](https://rust-lang.github.io/rustup/installation/index.html). Use `rustup
update` to get the latest stable version.

Then we can install Barbell:

```bash
RUSTFLAGS="-C target-cpu=native" cargo install barbell
```

See [here](https://github.com/ragnargrootkoerkamp/ensure_simd) for
details on `target-cpu=native`.

---

## 📸 Preview
<img src="data/barbell_example.gif" alt="Demo GIF" width="700">



---

## Quickstart

Barbell includes built-in kit *presets* for many Nanopore kits (most DNA kits; RNA and Twist kits are an exception). Presets let you run analyses quickly, but we recommend reading **Understanding barbell** to interpret the results correctly.

Basic command:

```bash
barbell kit -k <kit-name> -i <reads.fastq> -o <output_folder> --maximize
```

The `--maximize` option is recommended (e.g., for assembly) unless you need an ultra-strict barcode configuration.

### Native barcoding example (SQK-NBD114-96)

```bash
barbell kit -k SQK-NBD114-96 -i reads.fastq -o output_folder --maximize
```

This uses a conservative flank-based edit-distance cutoff. If many reads are missed during `annotate`, you can relax the flank error threshold, for example:

```bash
--flank-max-errors 5
```

—but always inspect the results after changing thresholds to avoid random matches (which show up as `Fflank` matches).

### Rapid barcoding example (SQK-RBK114-96)

```bash
barbell kit -k SQK-RBK114-96 -i reads.fastq -o output_folder --maximize
```

For a list of supported kits (see `data/supported_kits.txt`). Note that we thoroughly tested the rapid and native kits but not others, if you experience any issues please report them.
**Note**, there is an option `--use-extended` which enables searches for fusion points, and other artefacts. This is around 3 times slower, 
but worth it if quality is essential (i.e. generating consensus sequences).


### General Pointers

- **Too few annotated reads (many missed):**  
  Slightly increase `--flank-max-errors` (the automatically derived cutoff is reported).  

- **Too many `Fflank` matches:**  
  1. Check `annotation.tsv` to see if matches occur at unexpected locations (not near read ends).  
     - **Random locations:** Lower `--flank-max-errors`.  
     - **Non-random locations:** Adjust `--min-score-diff`.  
       > This is usually unnecessary as defaults are lenient; report an issue if it occurs.

- **Using a kit other than native or rapid** and observing unexpected annotations: Please report an issue.


---

## In-depth inspection of Nanopore kit results

Barbell's typical manual workflow: **annotate → inspect → filter → trim**.

### Annotate

Run `annotate` to find matches in reads and output an annotation table (TSV):

```bash
barbell annotate --kit SQK-RBK114-96 -i pass_sample.fastq -t 10 -o anno.tsv
```

(Using 10 threads.)

Example `anno.tsv` rows:

```
read_id read_len        rel_dist_to_end read_start_bar  read_end_bar    read_start_flank        read_end_flank   bar_start       bar_end match_type  flank_cost      barcode_cost    label   strand  cuts
c5f925b2-fc0b-4053-b615-d70950d41436    19783   14      14      104     14      104     0       0       Fflank   14      14      flank   Fwd
dbca7fb9-d6c8-4417-8ae7-bc32ebce9b27    2972    29      48      70      29      111     0       23      Ftag     13      7       BC29    Fwd
6c089f0a-50cd-4215-94f0-c7babb87f5fe    7599    27      51      74      27      121     0       23      Ftag     11      5       BC45    Fwd
..etc
```

For column descriptions see [Output columns (annotate & filter)](#output-columns-annotate--filter) below.

This file shows, per read, which barcodes/flanks were matched and with what costs. Use `inspect` next to summarize patterns.

### Inspect

Summarize patterns across the annotation file:

```bash
barbell inspect -i anno.tsv
```

By default `inspect` shows the top 10 pattern groups; use `-n <amount>` to increase.

Example summary:

```
Found 64 unique patterns
  Pattern 1: 82421 occurrences
    Ftag[fw, *, @left(0..250)]
  Pattern 2: 5003 occurrences
    Ftag[fw, *, @left(0..250)]__Ftag[fw, *, @right(0..250)]
  Pattern 3: 3545 occurrences
    Fflank[fw, *, @left(0..250)]
  ...
Showed 10 / 64 patterns
Inspection complete!
```

Some observations:
- `Ftag` on the left (`@left`) is the expected pattern for the rapid barcoding kit - that is good news.
- A contamination pattern can be a barcode on the left *and* another barcode on the right (`@right`). We can decide to just trim of the right side (see filtering later)
- `Fflank` indicates that flanks matched but no confident barcode was found.
- `@prev_left` indicates additional tags close to a previous element (e.g., double-barcode ligation).

#### Per-read patterns

To output the selected pattern per read:

```bash
barbell inspect -i anno.tsv -o pattern_per_read.tsv
```

Example `pattern_per_read.tsv` contents:

```
85ef... \t Ftag[fw, *, @left(0..250)]
2f67... \t Ftag[fw, *, @left(0..250)]__Ftag[fw, *, @prev_left(0..250)]
...
```

This is useful when you want to inspect a single "weird" read in detail.

### Filter

Create a `filters.txt` file listing the patterns you want to keep, one per line.
For example:

```
Ftag[fw, *, @left(0..250)]
Ftag[fw, *, @left(0..250)]__Ftag[fw, *, @right(0..250)]
Ftag[fw, *, @left(0..250)]__Ftag[fw, *, @prev_left(0..250)]
```

Then run:

```bash
barbell filter -i anno.tsv -f filters.txt -o filtered.tsv
```

The resulting `filtered.tsv` contains only reads that match the specified patterns.

#### Cutting / trimming metadata

Barbell needs to know *where* to cut reads for trimming. You mark cut positions by adding `>>` (cut **after** this element) or `<<` (cut **before** this element) inside the tag's bracket list. Where within the brackets does not matter.

Examples (note the comma-separated fields inside the brackets):

```text
Ftag[fw, *, @left(0..250), >>]
Ftag[fw, *, @left(0..250), >>]__Ftag[<<. fw, *, @right(0..250)]
Ftag[fw, *, @left(0..250)]__Ftag[fw, *, @prev_left(0..250), >>]
```

In the middle pattern we retain the read sequence between the left tag (cut after it) and the right tag (cut before it).

Run `filter` again (same command as above) to populate the `cuts` column in `filtered.tsv`. This is required before trimming.

---

## Trim

Trim reads using the `cuts` metadata produced by `filter`:

```bash
barbell trim -i filtered.tsv -r reads.fastq -o trimmed
```

Output files are organized by pattern-based folder/filenames, for example:

```
BC14_fw__BC14_fw.trimmed.fastq   BC31_fw__BC04_fw.trimmed.fastq  ...
```

If you prefer different filename conventions, use these flags:

```
  --no-label               Disable label in output filenames
  --no-orientation         Disable orientation in output filenames
  --no-flanks              Disable flanks in output filenames
  --sort-labels            Sort barcode labels in output filenames
  --only-side <left|right> Only keep left or right label in output filenames
```

Example to remove orientation and keep only the left label:

```bash
barbell trim -i filtered.tsv -r reads.fastq -o trimmed --no-orientation --only-side left
```

Gives:
```
BC01.trimmed.fastq  BC11.trimmed.fastq ...
```


## Custom experiment
We first create a Fasta, or multiple Fastas containing your queries depending on whether 
you have a single-end or dual-end experiment.


### Creating a query Fasta
If you have your own barcodes/primers/adapters, create FASTA files containing the full expected sequences. 
Note that each FASTA contains all sequences that <u>share the same prefix/suffix</u>, and are **unique**. 

The Fasta format should be as follows:
```text
>NB01
<left_flank_sequence><bar1_sequence><right_flank_sequence>
>NB02
<left_flank_sequence><bar2_sequence><right_flank_sequence>
...
```

Example (adapter + barcode + primer):

```
>NB01
TCGTTCAGTTACGTATTGCTCACAAAGACACCGACAACTTTCTTAGRGTTYGATYATGGCTCAG
>NB02
TCGTTCAGTTACGTATTGCTACAGACGACTACAAACGGAATCGAAGRGTTYGATYATGGCTCAG
```

Here:
```
TCGTTCAGTTACGTATTGCT CACAAAGACACCGACAACTTTCTT AGRGTTYGATYATGGCTCAG
    adapter               barcode                 primer
```

Barbell extracts the shared prefix (adapter) and shared suffix (primer) as flanks — only the barcode region should differ between FASTA entries.


### Single end
See above to create a fasta file, say `left.fasta` for single-end then we can run `annotate`:

```bash
barbell annotate -q left.fasta -b Ftag -i reads.fastq -o anno.tsv -t 10
```
After that you can follow the same `inspect → filter → trim` [steps described above](#inspect).


### Dual end
For dual-end, we create two FASTAs, `left.fasta` and `right.fasta` for example, then we run:

```bash
barbell annotate -q left.fasta,right.fasta -b Ftag,Rtag -i reads.fastq -o anno.tsv -t 10
```
Note: there must be **no spaces** between the comma-separated file list and the tag list: `-q left.fasta,right.fasta -b Ftag,Rtag`.


In case you have concatenated reads in your `inspect` also see [concat reads](#how-to-handle-concat-reads)

---



## Custom experiment with mixed sequences
Often we combine multiple samples together which share the same flanks, for example all rapid barcoding. 
But we could also combine completely different experiments, with different primers for example.
How do we demux that?

First go through "[custom experiment](#custom-experiment)" setup, then continue reading here how we adjust the query files.

That's quite simple. We create fasta files for all possible groups. 
Lets say we have:

**group1**
- group1_left.fasta: adapter1-barcode-primer1
- group1_right.fasta: primer1-barcode-adapter1

**group2**:
- group2_left.fasta: adapter2-barcode-primer2
- group2_right.fasta: primer2-barcode-adapter2

Then we <u>make sure our labels in the fasta have some unique substring</u>, like `group1` and `group2`:
for example:

`group1_left.fasta`:
```
>group1_bar1
AACGACA...
```
`group2_left.fasta`:
```
>group2_bar1
AGGGCAC...
```

We then run annotate like:

```
barbell annotate -q group1_left.fasta,group1_right.fasta,group2_left.fasta,group2_right.fasta -b Ftag,Rtag,Ftag,Rtag -i reads.fastq -o anno.tsv -t 10
```

**Note**: While you could run annotate separately for each query file, it’s generally better to combine all into a single annotate run (as mentioned here). This way, they are competing with one another.


Then in the filtering step we can create filtered files for each group:
(just check `inspect` first to see your patterns)


`group1_filters.txt`:
```
Ftag[fw, ~group1, @left(0..250), >>]__Rtag[<<, rc, ~group1, @right(0..250)]
```

`group2_filters.txt`:
```
Ftag[fw, ~group2, @left(0..250), >>]__Rtag[<<, rc, ~group2, @right(0..250)]
```

And pull them out!
```
barbell filter -i anno.tsv -f group1_filters.txt -o group1_reads.tsv
barbell filter -i anno.tsv -f group2_filters.txt -o group2_reads.tsv
```
and then we can just trim them to separate files:

```
barbell trim -i group1_reads.tsv -r reads.fastq -o group1_trimmed
barbell trim -i group2_reads.tsv -r reads.fastq -o group2_trimmed
```



---

## Output columns (annotate & filter)

- `read_id`: read identifier as in the provided FASTQ
- `read_len`: length of read in bp
- `rel_dist_to_end`: relative distance to the read end. `>= 0` means X bases from the **left** end; a negative value means X bases from the **right** end (e.g. `-10` is 10 bp from the right).
- `read_start_bar`: start position of the barcode match in the read
- `read_end_bar`: end position of the barcode match in the read
- `read_start_flank`: start position of the flank match in the read
- `read_end_flank`: end position of the flank match in the read
- `bar_start`, `bar_end`: coordinates where the barcode was aligned (previous partial-barcode matches are disabled; full barcode length is expected)
- `match_type`:
  - `Ftag`: forward barcode + flank matched
  - `Fflank`: forward flank matched (barcode undetectable)
  - `Rtag`: rear barcode + flank matched
  - `Rflank`: rear flank matched (barcode undetectable)

  *Note*: for some kits (e.g., rapid barcoding) there's effectively a single barcode; we still call this `Ftag`. For native dual barcoding both ends may use the same barcode set; orientation (forward/reverse complement) is available in the `strand` column.

- `flank_cost`: number of edits in the flank sequence (excluding the barcode)
- `barcode_cost`: number of edits in the barcode region
- `label`: label from your FASTA (or preset kit) — e.g., `BC14`, `RBK60`, etc.
- `strand`: orientation of the match (`fw` or `rc`)
- `cuts`: empty after `annotate`; populated after `filter` to inform `trim` where to cut

---



## Patterns

Patterns describe how elements are combined in a read. Single elements have the form:

```
<tag>[<orientation>, <label>, <relative position>, <optional cut specifier>]
```

Multiple elements are combined with `__` (double underscore):

```
<tag>[...]__<tag>[...]
```

Fields:
- `tag`: `Ftag`, `Fflank`, `Rtag`, `Rflank`, whether a sequence is `Ftag` or `Rtag` is user specified (or within the kit), see [custom experiment](#custom-experiment), the `Fflank,Rflank` are the "incomplete" forms where the barcode was undetectable.
- `orientation`: `fw` or `rc`.
- `label`: exact label (e.g. `NB01`), `*` for any label, or `~substring` to match headers containing `substring` (for an example see [custom exp. mixing](#custom-experiment-with-mixed-sequences)).
- `relative position`: e.g. `@left(0..250)`: to left side of read, `@right(0..250)`: to right side of read, `@prev_left(0..250)`: relative to the <u>previous</u> element.
- `cut specifier` (optional): `>>` (cut after this element) or `<<` (cut before this element).

Examples:

```
Ftag[fw, *, @left(0..250), >>]
Ftag[fw, *, @left(0..250), >>]__Ftag[<<, rc, *, @right(0..250)]
Ftag[fw, *, @left(0..100), >>]__Rtag[<<, fw, *, @prev_left(1500..1700)]
```
(for examples of concat reads see [concat reads](#how-to-handle-concat-reads) section)

These let you express typical cases such as single-barcode-left, left-and-right barcodes, or expected amplicon sizes via `@prev_left`.

---


### How to handle concat reads 
It is possible that you have concat reads like:

```
Ftag[fw, *, @left(0..250), >>]__Ftag[<<, rc, *, @pev_left(1500..1750)]__Ftag[fw, *, @prev_left(0..250), >>]__Ftag[<<, rc, *, @right(0..250)]
```
We always read the pattern from <u> left to right </u>, then we can deduce the read matches looked like this:
```
[Ftag,fw]---------[Ftag,rc][Ftag, fw]---------[Ftag, rc]
```
If we want to cut more than once we have to use **cut group identifiers**, we do this by placing a number <u> after </u> the `<<` or `>>`:

```
Ftag[fw, *, @left(0..250), >>1]__Ftag[<<1, rc, *, @pev_left(1500..1750)]__Ftag[fw, *, @prev_left(0..250), >>2]__Ftag[<<2, rc, *, @right(0..250)]
```
Note the `>>1, <<1, >>2, <<2`, now barbell knows exactly where you want the reads to be cut.

If the labels were: `NB01---NB01-NB02----NB02`, barbell will write the first read to the `NB01` folder and the second to `NB02`. 

#### Getting *all* concats

If concats are a big part of your read set (ideally they are not) their patterns will show up high in `inspect` anyway, and copying just those will 
probably be enough. If you really want *all* the concat reads out you could use the `-o` in `inspect` to write the patterns
per read. Then, get all unique patterns from there and use a regex or a python script to insert the `>>1` and `<<1`, you can just dump all of them 
to `filters.txt` and use that in `barbell filter`. 


---

## Paper evals
Since this involves substantial amount of extra code we moved these to the [paper-evals](https://github.com/rickbeeloo/barbell-evals) repo. All information on how to reproduce results and set up environments to do so can be found there. 

---

## Notes & tips

- Keep an eye on `Fflank` matches — these are often lower-confidence and may indicate reads with poor barcode sequence quality.
- Start with conservative filters to see how many reads match expected patterns, then relax thresholds if necessary. 
- When experimenting with custom FASTAs, keep queries clean (shared flanks, differing barcode region only).

---


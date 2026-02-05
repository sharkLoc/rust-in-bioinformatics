# gvcf_norm

**Command-line tool for [left-aligning and normalizing](https://genome.sph.umich.edu/wiki/Variant_Normalization#Algorithm_for_Normalization) gVCF variants**

**NOTICE: [DeepVariant v1.3.0+](https://github.com/google/deepvariant/releases/tag/v1.3.0) has a built-in option to ensure indel left-alignment, replacing this utility**. Enable it with `make_examples --normalize-reads` or `run_deepvariant --make_examples_extra_args normalize_reads=true`.

Same algorithm as `vt normalize` and `bcftools norm -f`, but tolerates gVCF's idioms: (i) ignores any symbolic alleles in variant records (`<NON_REF>`, `<*>`, `*`), and (ii) passes through reference bands unchanged.

Because variant records can be repositioned, *but not* reference bands, a repositioned variant record may end up in the middle of an overlapping reference band, with a small coverage gap between the reference bands. But at least the variant records are normalized.

**Build** 

[![CI](https://github.com/mlin/gvcf_norm/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/mlin/gvcf_norm/actions/workflows/build.yml)

```cargo build --release```

to build `target/release/gvcf_norm`

**Usage**

```bgzip -dc my.g.vcf.gz | ./gvcf_norm -r /ref/genome/dir/ - | bgzip -c > my.norm.g.vcf.gz```

where `/ref/genome/dir` is a directory with the reference genome sequences, one file per chromosome named as such, containing no whitespace (suitable for memory-mapped offset access into each sequence). Generate this directory from a reference genome FASTA using the [`unpack_fasta_dir.sh`](unpack_fasta_dir.sh) script, which uses [seqkit](https://bioinf.shenwei.me/seqkit/).

Memory usage grows with the uncompressed text of all gVCF records for the largest chromosome.

### Example 1

*(Some fields omitted for brevity)*

**Before**

```
chr21  29848774  T   <*>             END=29848778  GT:MIN_DP  0/0:30
chr21  29848779  AT  ATATATTT,T,<*>  .             GT:DP      1/2:32
chr21  29848781  T   <*>             END=29848791  GT:MIN_DP  0/0:19
```

**After**

```
chr21  29848774  T   <*>             END=29848778                    GT:MIN_DP  0/0:30
chr21  29848778  TA  TATATATT,T,<*>  gvcf_norm_originalPOS=29848779  GT:DP      1/2:32
chr21  29848781  T   <*>             END=29848791                    GT:MIN_DP  0/0:19
```

The single-nucleotide deletion chr21:29848778 TAT>TT was written as 29848779 AT>T but normalized to 29848778 TA>T, and the insertion padded to match. The pre-normalized position is recorded in a new INFO field. The new position overlaps with the preceding reference band, and there's a gap in reference band coverage.

### Example 2

**Before**

```
chr21  26193733  T       <*>      END=26193733  GT:MIN_DP  0/0:33
chr21  26193734  G       T,<*>    .             GT:DP      0/1:33
chr21  26193735  T       <*>      END=26193740  GT:MIN_DP  0/0:32
chr21  26193741  TTTTTT  T,<*>    .             GT:DP      0/1:32
chr21  26193747  T       <*>      END=26193751  GT:MIN_DP  0/0:22
```

**After**

```
chr21  26193733  T       <*>    END=26193733                    GT:MIN_DP  0/0:33
chr21  26193734  G       T,<*>  .                               GT:DP      0/1:33
chr21  26193734  GTTTTT  G,<*>  gvcf_norm_originalPOS=26193741  GT:DP      0/1:32
chr21  26193735  T       <*>    END=26193740                    GT:MIN_DP  0/0:32
chr21  26193747  T       <*>    END=26193751                    GT:MIN_DP  0/0:22
```

The deletion chr21:26193741 TTTTTT>T moved some distance upstream to 26193734 GTTTTT>G. The record order changed to remain sorted by position. The new position coincides with another variant record, which wasn't merged, and also hangs over a passed-through reference band. There's a gap in reference band coverage at the old position.

The tool doesn't have enough information to fix up the reference bands. We hope the tool will not be needed for long.


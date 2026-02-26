kanpig - Kmer ANalysis of PIleups for Genotyping
<img src="https://github.com/ACEnglish/kanpig/raw/develop/imgs/icon.png/" style="width:100px;" align="right" style="vertical-align: middle;"> 
------
A fast tool for genotyping structural variants with long-reads.

📝 Read [the paper](https://www.nature.com/articles/s41467-025-58577-w) for more details.

# 📥 Install
Binaries are available in [releases](https://github.com/ACEnglish/kanpig/releases).

Alternatively, build from source with:
```bash
git clone https://github.com/ACEnglish/kanpig
cd kanpig
cargo build --release
# executable in ./target/release/kanpig
```

# 🚀 Quick Start
```bash
kanpig gt --input variants.vcf.gz \
          --reads alignments.bam \
          --reference genome.fa \
          --out output.vcf
```
See `kanpig -h` for all available parameters, most of which are detailed below.

Kanpig can also create a pileup index from a bam that is smaller and faster for the genotyper to parse. This is useful
for long-term projects or multiple reanalysis operations like N+1 for a cohort.

```bash
kanpig plup --bam alignments.bam | bedtools sort -header | bgzip > alignments.plup.gz
tabix -p bed alignments.plup.gz
```

Other available genotyping modes are `kanpig trio` and `kanpig mosaic`.

# 📝 Annotations

The `SAMPLE` column fields populated by kanpig are:

| Field   | Description |
|---------|-------------|
| **FT**  | Bit flag for properties of the variant's genotyping |
| **SQ**  | Phred scaled likelihood variant alternate is present in the sample |
| **GQ**  | Phred scale difference between most and second-most likely genotypes |
| **PS**  | Phase set pulled from haplotagged reads for long-range phasing or Neighborhood id of variants evaluated together for short-range phasing |
| **DP**  | Read coverage over the region |
| **AD**  | Read coverage supporting the reference and alternate alleles |
| **KS**  | [Kanpig score](https://github.com/ACEnglish/kanpig/wiki/Scoring-Function) |

Details of `FT`
| Bit   | Description |
|--------|-------------|
| 0x1    | The genotype observed from variants paths matching is not equal to the genotype observed from measuring the proportions of reads supporting the two alleles. |
| 0x2    | The genotype quality is less than 5 |
| 0x4    | The depth (DP) is less than 5 |
| 0x8    | The sample quality (SQ) is less than 5 (only present on non-ref variants) |
| 0x16   | The number of reads supporting the alternate allele less than 5 (only present on non-ref variants) |
| 0x32   | The best scoring path through the variant graph only used part of the haplotype. This may be indicative of a false-negative in the variant graph. |
| 0x64   | The variant is supported by reads from a non-germline haplotype clustering (mosaic mode only) |

# 🔌 Compute Resources

Kanpig is highly parallelized and will fully utilize all threads it is given. However, hyperthreading doesn't seem to
help and therefore the number of threads should probably be limited to the number of physical processors available. For
memory, giving kanpig 2GB per-core is usually more than enough.

Note that kanpig is predominantly I/O limited and may not benefit from more than ~4-8 cores.

The actual runtime and memory usage of kanpig run will depend on the read coverage and the number of SVs in the input
VCF. As a example of kanpig's resource usage with 16 cores available, genotyping a 30x long-read bam against a 2,199
sample VCF (4.3 million SVs) took 13 minutes with a maximum memory usage of 12GB. Converting the bam to a plup file took
4 minutes (8GB of memory) and genotyping with this plup file took 3 minutes (12GB memory). 

While genotyping against a plup file is usually faster, bam to plup conversion is most useful for:
* genotyping a large VCF or super-high (>50x) coverage bam.
* a sample that will be genotyped multiple times (e.g. N+1 pipelines) 
* long-term access to reads (a plup file is up to ~2,000x smaller than a bam)

# 🔧 Core Parameter Details

These parameters are universal to all the genotyping modes and handle how variant graphs are built or how haplotypes are
applied to the graphs. The default parameters work generally well for most use cases. The optimal parameters for a
particular experiment will depend on things such as number of samples in the VCF and the merging strategy of the variants.

### `--neighdist`
Kanpig will build local variant graphs from groups of variants in a 'neighborhood'. These neighborhoods are determined by 
making the maximum end position of an upstream neighborhood's variants at least `neighdist` base-pairs away from the next 
neighborhood's variants' minimum start position.

This distance also determines the region over which read pileups are generated. Only reads with at least `mapq` mapping quality, 
passing the `mapflag` filter, and which fully span the neighborhood are considered.

This is an important parameter because too small of a `neighdist` may not recruit distant read pileups which support variants.
Similarly, too large of a value may create long neighborhoods for reads to fully-span or with many SVs.

### `--sizemin` and `--sizemax`
Variant sizes are determined by `abs(length(ALT) - length(REF))` or `END - POS` for `<DEL>`. Genotypes of variants not 
within the size boundaries are set to missing (`./.`).

Read pileups also must be within this sizemin and sizemax. Some SVs with sizes around these thresholds may not be
consistent between alignments/variants. For example, the VCF may describe a 50bp variant while the alignments have a
49bp or split 10bp and 40bp variant. These problematic regions can sometimes benefit from a lower `--sizemin`, however this is
not a magic fix for all cases.

### `--sizesim` and `--seqsim`
When applying a haplotype to a variant graph, only paths above these two thresholds are allowed. If there are multiple
paths above the threshold, the one with the highest score is kept. Generally, `0.90` is well balanced
whereas lower thresholds will boost recall at the cost of precision and vice versa for higher thresholds.

### `--gpenalty` and `--fpenalty`
The similarity of a path to the graph is used to to compute a score and the highest score kept. The scoring formula is

```
Score(P) = ((SS + SZ) / 2) − (λg ⋅ ∣L(P)−E∣) - (λf ⋅ N)
``` 

where `SS` and `SZ` are sequence and size similarity,  `L(P)` is the number of nodes in the path, and `E` is the number of 
pileups in the haplotype, and `N` is the number of putative false-negatives in the variant graph. 

The penalty factor `λg` helps reduce paths with split variant representations. The penalty factor `λf` helps penalizes
false-negatives in the variant graph. Details on the scoring penalties are in [the wiki](https://github.com/ACEnglish/kanpig/wiki/Scoring-Function).

### `--maxpaths`
When performing path-finding, this threshold limits the number of paths which are checked. A lower `maxpaths` will
speed up runtime but may come at a cost of recall. A higher `maxpaths` is slower and may come at a cost to
specificity.

### `--maxnodes`
If a neighborhood has too many variants, its graph will become large in memory and slow to traverse. This parameter 
will turn off path-finding in favor of `--one-to-one` haplotype to variant comparison, reducing runtime and memory usage. 
This may reduce recall in regions with many SVs, but these regions are problematic anyway.

### `--one-to-one`
Instead of performing the path-finding algorithm to apply a haplotype to the variant graph, perform a 1-to-1 
comparison of the haplotype to each node in the variant graph. If a single node matches above `sizesim` and `seqsim`, 
the haplotype is applied to it. 

This parameter will boost the specificity, increase speed, and lower memory usage of kanpig at the cost of recall.

### `--squish`
By default, the `--gpenalty` is applied to the scoring function as the difference between a path's node count and a 
haplotype's variant count. With `--squish` the score is weighed by the path's node count minus one. This means paths
with fewer nodes are preferred over paths with a consistent representation to the alignment. This parameter is useful
for multi-sample VCFs where consistency between variants' genotypes is more important than preserving the exact set of
variants that best reflect those described by the alignments.

# 🛏️ Bed Files

### `--bed`
A sorted bed file (`bedtools sort`) that restricts kanpig to only analyzing variants with starts and ends within a 
single bed entry.

### `--ploidy-bed`
This bed file informs kanpig of special regions within chromosomes that should have non-diploid genotypes. For example, 
a female human sample shouldn't have any genotypes on chrY. A male human sample should have hemizygous genotypes on chrY 
and the non-pseudoautosomal regions of chrX. The [ploidy_beds/](https://github.com/ACEnglish/kanpig/tree/develop/ploidy_beds)
directory  has example bed files for GRCh38. All regions not within the `--ploidy-bed` (or if no bed is provided) are 
assumed to be diploid.

# 🧬 Germline Mode

Original use case of SV Genotyping.

### `--hapsim`
After performing kmedoid clustering on reads to determine the two haplotypes, if the two haplotypes have a size similarity 
above `hapsim`, they are consolidated into a homozygous allele. This is useful for when input SVs over a certain 
size/sequence sequence similarity have already been merged (see [truvari collapse](https://github.com/ACEnglish/truvari)).

### `--ab`
In loci where reads cluster into a potentially compound heterozygous site, the proportion of reads supporting the
haplotype with lower coverage must have at least `--ab` fraction of the reads. Otherwise, we assume that the
lower-covered haplotype is a mapping/sequencing anaomaly and treat its reads as supporting the reference. This parameter
at 0.20 boosts specificity and genotype concordance at the cost of (a little bit less) recall.

### `--hps-weight`
Informatin from haplotagged reads (PS and HP tags) can be used to improve clustering. The weight serves to make reads
from different HPs have a higher distance inside the matrix sent to kmedoid clustering.

# 👪 Trio Mode

A proband along with their mother and father can be joint genotyped simultaneously with `kanpig trio`. The goal of a 
separate module is to increase genotyping accuracy in the proband as well as consistently applying shared haplotypes
to the same paths through the variant graph, thus decreasing mendelian errors and more precisely identifying de novo SVs. 

This mode works by running a MeanShift clustering on haplotype lengths to determine the value of K for Kmedoids clustering.
After the haplotypes are clustered, the genotyper tests the likelihood of all possible inheritance patterns given each
haplotype's coverage.

### `--msmin`
When performing MeanShift clustering, this controls the minimum number of reads inside each bin.

### `--maxclust`
The maximum number of clusters (i.e. highest K) allowed. This defaults to 5 to allow for the possibility of compound
heterozygous in both parents and one denovo variant in the proband.

### `--hps-weight` & `--len-weight`
When building the distance matrix for kmedoid clustering, reads with different haplotagging HPs or in different
MeanShift clusters will have the distance increased by `*= 1+weight`.

# 🎨 Mosaic Mode

Reads of samples from a single individual are pooled together and genotyped with the expectation that germline and
somatic alleles are present. The germline variants will be genotyped as heterozygous or homozygous alt whereas the
somatic variants will have the `FMT/FT` SOMATIC flag (0x64) populated. If multiple sets of input reads are provided
(e.g. multiple tissues across a single individual), each sample will have an output `SAMPLE` column. However, all 
reads are pooled together during the clustering and up to `--maxclust` allowed. 

Some of mosaic mode's parameters are shared with trio mode and documented above.

### `--bandwidth`
When performing MeanShift clustering, length-based clusters must be at least `--bandwidth` base-pairs different in
length. 

### `--alpha`, `--beta`, & `--soma-vaf`
These parameters are for the modeling of somatic events. The defaults work well for benchmarking against the artificial
HapMap Mix provided by the SMaHT network and their MIMS SV benchmark. In practical samples, with different VAF
distributions of somatic events, these parameters may need to be tweaked. See XYZ for a detailed tutorial on how to
these parameters impact the modeling.

# ⚠️ Current Limitations
* Kanpig expects sequence resolved or `<DEL>` SVs. Other SVs with symbolic alts (e.g. `<DUP>`) and BNDs are not parsed.
* Kanpig only looks at read pileups and does not consider split or soft-clipped alignment information. This means
  variants above ~10kbp should be skipped with the `--sizemax` parameter unless you have reason to believe the reads are
  aligned continuously over larger SVs (e.g. genotyping from assembly alignments).
* As a VCF becomes more complex (e.g. a project-level VCF), kanpig's precision may drop. This is because as more
  SVs/neighborhoods are added to the graph, the chances of spurious reads in a given sample being picked up
  and applied to the graph increase. One way to counter this is to [post-filter genotypes](https://github.com/ACEnglish/kanpig/wiki/Filtering-Genotypes)
  for minimum read support. Additionally, genotyping results in regions with an absurd number of candidates SVs caused by 
  limitations of alignment-based SV discovery should generally not be trusted.

# 🐍 Python bindings
Minimal python bindings are available for plup parsing. These can be installed via `maturin develop --release --features python`
and used from python with `import kanpig`.

# 🎛️GQ Calibration
Genotype quality scores produced by kanpig v1 were broken.  As part of the refactoring in v2 that fixed the genotyper's
default behavior, we also provide procedures for calibrating GQs.
See [Genotype Quality Calibration](gqcalibration/README.md) for details.



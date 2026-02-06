# Test Data for RUST-BIO-KIT

This directory contains robust, lightweight test datasets for verifying the functionality of bioinformatics tools in this repository. The data is a mix of synthetic files (generated to specification) and small subsets of real biological data (publicly available).

## Generation

To regenerate this data, run:

```bash
python3 scripts/generate_test_data.py
bash scripts/fetch_public_data.sh
```

## Directory Content

### `dna/`
- **`random.fa`**: Synthetic FASTA file with random sequences (ACGT).
- **`edge_cases.fa`**: Synthetic FASTA with edge cases (N bases, lowercase, variable lengths).
- **`sars_cov_2.fna.gz`**: Real SARS-CoV-2 genome (RefSeq NC_045512.2), compressed.
- **`random.gff3`**: Synthetic GFF3 annotation file.
- **`random.bed`**: Synthetic BED file.

### `fastq/`
- **`random.fq`**: Synthetic FASTQ file (Phred+33 quality scores).
- **`random.fq.gz`**: Gzip-compressed version of synthetic FASTQ.

### `bam/`
- **`random.sam`**: Synthetic SAM file with mapped and unmapped reads. Useful for converting to BAM or testing alignment parsers.

### `vcf/`
- **`random.vcf`**: Synthetic VCF v4.2 file with random SNPs/indels and genotypes.
- **`example.vcf`**: Small VCF subset from `bcftools` test suite.

### `csv/`
- **`random.csv`**: Synthetic CSV file with mixed data types and quoted fields.

### `longreads/`
- **`random_long.fq`**: Synthetic long-read FASTQ (simulating Nanopore/PacBio read lengths).

### `proteomics/`
- **`random.faa`**: Synthetic Protein FASTA file (amino acids).
- **`1CRN.pdb`**: Structure of Crambin (small protein) from RCSB PDB.

### `pangenomics/`
- **`random.gfa`**: Synthetic GFA (Graphical Fragment Assembly) file representing a small graph.

### `phylogenomics/`
- **`random.nwk`**: Synthetic Newick tree file.

### `singlecell/`
- **`random.mtx`**: Synthetic Matrix Market file representing a sparse gene-cell count matrix.

### `rna/`
- **`transcripts.fa`**: Synthetic FASTA file representing transcripts.
- **`counts.tsv`**: Synthetic gene expression table (gene_id, counts, TPM).

### `metagenomics/`
- **`contigs.fa`**: Synthetic FASTA file representing metagenomic contigs.
- **`taxonomy.tsv`**: Synthetic table mapping reads to taxonomy IDs.
- **`mock_community.fna`**: Real biological data; concatenation of SARS-CoV-2 and PhiX genomes.

## Usage

Use these files in your test suites or CI pipelines. They are small enough to be committed if necessary, but generating them via scripts is preferred to keep the repo light.

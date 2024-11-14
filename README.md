### rust in bioinformatics

A collection of genomics software tools written in Rust



### index section

##### bam
- [alignoth](https://github.com/alignoth/alignoth) : Creating alignment plots from bam files
- [best](https://github.com/google/best) : Bam Error Stats Tool (best): analysis of error types in aligned reads
- [modkit](https://github.com/nanoporetech/modkit) : A bioinformatics tool for working with modified bases
- [mapAD](https://github.com/mpieva/mapAD) : An aDNA aware short-read mapper
- [perbase](https://github.com/sstadick/perbase) : Per-base per-nucleotide depth analysis
- [rustybam](https://github.com/mrvollger/rustybam) : bioinformatics toolkit in rust

##### csv

- [csview](https://github.com/wfxr/csview) : 📠 Pretty and fast csv viewer for cli with cjk/emoji support
- [csvlens](https://github.com/YS-L/csvlens) : csvlens is a command line CSV file viewer. It is like less but made for CSV.
- [madato](https://github.com/inosion/madato) : Markdown Cmd Line, Rust and JS library for Excel to Markdown Tables
- [tabiew](https://github.com/shshemi/tabiew) : A lightweight TUI app to view and query CSV files
- [tv](https://github.com/alexhallam/tv) : 📺(tv) Tidy Viewer is a cross-platform CLI csv pretty printer that uses column styling to maximize viewer enjoyment.
- [xan](https://github.com/medialab/xan) : The CSV magician
- [xsv](https://github.com/BurntSushi/xsv) : A fast CSV command line toolkit written in Rust.  
- [xtab](https://github.com/sharkLoc/xtab) : CSV command line utilities

##### dna

- [fakit](https://github.com/sharkLoc/fakit) : fakit: a simple program for fasta file manipulation
- [filterx](https://github.com/dwpeng/filterx) : process any file in tabular format. Fasta/fastq/GTF/GFF/VCF/SAM/BED
- [fq](https://github.com/stjude-rust-labs/fq) : Command line utility for manipulating Illumina-generated FASTQ files.
- [gsearch](https://github.com/jean-pierreboth/gsearch) : Approximate nearest neighbour search for microbial genomes based on hash metric
- [kfc](https://github.com/lrobidou/KFC) : KFC (K-mer Fast Counter) is a fast and space-efficient k-mer counter based on hyper-k-mers.
- [ngs](https://github.com/stjude-rust-labs/ngs) : Command line utility for working with next-generation sequencing files.
- [nail](https://github.com/TravisWheelerLab/nail) : Nail is an Alignment Inference tooL
- [poasta](https://github.com/broadinstitute/poasta) : Fast and exact gap-affine partial order alignment
- [rust-bio-tools](https://github.com/rust-bio/rust-bio-tools) : A set of command line utilities based on Rust-Bio.
- [skc](https://github.com/mbhall88/skc) : Shared k-mer content between two genomes
- [sketchy](https://github.com/esteinig/sketchy) : Genomic neighbor typing of bacterial pathogens using MinHash 🐀
- [tidk](https://github.com/tolkit/telomeric-identifier) : Identify and find telomeres, or telomeric repeats in a genome.
- [xgt](https://github.com/Ebedthan/xgt) : Efficient and fast querying and parsing of GTDB's data

##### fastq

- [fasten](https://github.com/lskatz/fasten) : 👷 Fasten toolkit, for streaming operations on fastq files
- [faster](https://github.com/angelovangel/faster) :  A (very) fast program for getting statistics about a fastq file, the way I need them, written in Rust
- [fqgrep](https://github.com/fulcrumgenomics/fqgrep) : Grep for FASTQ files
- [fqkit](https://github.com/sharkLoc/fqkit) : 🦀 Fqkit: A simple and cross-platform program for fastq file manipulation  
- [fqtk](https://github.com/fulcrumgenomics/fqtk) : Fast FASTQ sample demultiplexing in Rust.
- [rasusa](https://github.com/mbhall88/rasusa) : Randomly subsample sequencing reads

#### format
- [bigtools](https://github.com/jackh726/bigtools) : A high-performance BigWig and BigBed library in Rust
- [d4tools](https://github.com/38/d4-format) : The D4 Quantitative Data Format
- [gia](https://github.com/noamteyssier/gia) : gia: Genomic Interval Arithmetic
- [intspan](https://github.com/wang-q/intspan) : Command line tools for IntSpan related bioinformatics operations
- [thirdkind](https://github.com/simonpenel/thirdkind) : Drawing reconciled phylogenetic trees allowing 1, 2 or 3 reconcillation levels


##### gff3

- [atg](https://github.com/anergictcell/atg) : A Rust library and CLI tool to handle genomic transcripts   
- [gffkit](https://github.com/sharkloc/gffkit) : a simple program for gff3 file manipulation

##### longreads

- [chopper](https://github.com/wdecoster/chopper) : Rust implementation of [NanoFilt](https://github.com/wdecoster/nanofilt)+[NanoLyse](https://github.com/wdecoster/nanolyse), both originally written in Python. This tool, intended for long read sequencing such as PacBio or ONT, filters and trims a fastq file.
- [herro](https://github.com/lbcb-sci/herro) : HERRO is a highly-accurate, haplotype-aware, deep-learning tool for error correction of Nanopore R10.4.1 or R9.4.1 reads (read length of >= 10 kbps is recommended).
- [HiPhase](https://github.com/PacificBiosciences/HiPhase) : Small variant, structural variant, and short tandem repeat phasing tool for PacBio HiFi reads
- [longshot](https://github.com/pjedge/longshot) : diploid SNV caller for error-prone reads
- [nextpolish2](https://github.com/Nextomics/NextPolish2) : Repeat-aware polishing genomes assembled using HiFi long reads
- [nanoq](https://github.com/esteinig/nanoq) : Minimal but speedy quality control for nanopore reads in Rust 🐻
- [smrest](https://github.com/jts/smrest) : Tumour-only somatic mutation calling using long reads
- [trgt](https://github.com/PacificBiosciences/trgt) : Tandem repeat genotyping and visualization from PacBio HiFi data

##### metagenomics

- [coverm](https://github.com/wwood/CoverM) : Read coverage calculator for metagenomics
- [kmertools](https://github.com/anuradhawick/kmertools) : kmer based feature extraction tool for bioinformatics, metagenomics, AI/ML and more
- [nohuman](https://github.com/mbhall88/nohuman) : Remove human reads from a sequencing run
- [skani](https://github.com/bluenote-1577/skani) : Fast, robust ANI and aligned fraction for (metagenomic) genomes and contigs.
- [sourmash](https://github.com/sourmash-bio/sourmash) : Quickly search, compare, and analyze genomic and metagenomic data sets.
- [sylph](https://github.com/bluenote-1577/sylph) : ultrafast genome querying and taxonomic profiling for metagenomic samples by abundance-corrected minhash.
- [vircov](https://github.com/esteinig/vircov) : Viral genome coverage evaluation for metagenomic diagnostics 🩸

##### pangenomics

- [impg](https://github.com/pangenome/impg) : implicit pangenome graph
- [panacus](https://github.com/marschall-lab/panacus) : Panacus is a tool for computing statistics for GFA-formatted pangenome graphs

##### phylogenomics

- [nextclade](https://github.com/nextstrain/nextclade) : Viral genome alignment, mutation calling, clade assignment, quality checks and phylogenetic placement
- [segul](https://github.com/hhandika/segul) : An ultrafast and memory efficient tool for phylogenomics

##### proteomics

- [foldmason](https://github.com/steineggerlab/foldmason) : Foldmason builds multiple alignments of large structure sets.
- [sage](https://github.com/lazear/sage) : Proteomics search & quantification so fast that it feels like magic

##### rna
- [oarfish](https://github.com/COMBINE-lab/oarfish) : long read RNA-seq quantification
- [rnapkin](https://github.com/ukmrs/rnapkin) : drawing RNA secondary structure with style; instantly
- [R2Dtool](https://github.com/comprna/R2Dtool) : R2Dtool is a set of genomics utilities for handling, integrating, and viualising isoform-mapped RNA feature data.
- [squab](https://github.com/zaeleus/squab) : Alignment-based gene expression quantification

##### singlecell

- [alevin-fry](https://github.com/COMBINE-lab/alevin-fry) : 🐟 🔬🦀 alevin-fry is an efficient and flexible tool for processing single-cell sequencing data, currently focused on single-cell transcriptomics and feature barcoding.
- [cellranger](https://github.com/10XGenomics/cellranger) : 10x Genomics Single Cell Analysis
- [precellar](https://github.com/regulatory-genomics/precellar) : Single-cell genomics preprocessing package
- [SnapATAC2](https://github.com/kaizhang/SnapATAC2) : Single-cell epigenomics analysis tools

##### slurm

- [ssubmit](https://github.com/mbhall88/ssubmit) : Submit slurm sbatch jobs without the need to create a script

##### vcf

- [echtvar](https://github.com/brentp/echtvar) : using all the bits for echt rapid variant annotation and filtering
- [mehari](https://github.com/varfish-org/mehari): VEP-like tool for sequence ontology and HGVS annotation of VCF files
- [vcf2parquet](https://github.com/natir/vcf2parquet) : Convert vcf in parquet
- [vcfexpress](https://github.com/brentp/vcfexpress) : expressions on VCFs

##### other
- [htsget-rs](https://github.com/umccr/htsget-rs) : A server implementation of the htsget protocol for bioinformatics in Rust
- [sufr](https://github.com/TravisWheelerLab/sufr) : Parallel Construction of Suffix Arrays in Rust

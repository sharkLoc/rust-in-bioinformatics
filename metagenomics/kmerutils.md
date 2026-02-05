# Some Kmer counting utilities

The package is mainly devoted as designed to be library to the crate [gsearch](https://crates.io/crates/gsearch), to classify prokaryotic genomes.

It provides the following tools :

* Simple representation of Kmers up to 32 bases with compressed representation on 2 or 4 bits stored in u32 or u64 for simplicity and efficacity.
  
* Basic Kmer threaded counting tools with Bloom and Cuckoo filters.

* Sketching of sequences with up to date various sensitive hashing see *module sketching* and the crate [probminhash](https://crates.io/crates/probminhash)  

* A quality server.
  The binary executable *qualityloader* loads qualities from a Fastq file and runs as a server, answering
  basic requests as returning a quality sequence of given sequence number , or a block of a sequence or simply the base at a given pos  in a sequence given its rank. This enables storing qualities on a different machine.

* some basic statistics dumps  such as base distributions, read length distributions.

It has a Julia companion providing interactive access to dumped statistics or interactive inspection of sequences
of bases and qualities.

## Kmer Compression and Counting

The bases are presently encoded on 2 bits.  
Kmer can be stored 32-bit or 64-bit words thus providing compressed representation up to 32 bases with the 2-bit alphabet.  
Kmer and compressed Kmer are represented respectively by trait *KmerT* and *CompressedKmerT*.
A kmer is identified with its reverse complement in the counting methods.  

Kmer counting is multi-threaded and filters unique kmer in a cuckoo filter to spare memory.
Unique kmers are dumped in a separate file with the coordinates (sequence and position in sequence).
Multiple kmers, stored in a Bloom filter, are dumped in another file with their multiplicity. See module *kmercount*

## Hashing and Sketching of data

Similarity between sequences can be estimated by counting common Kmers between sequences with :
  - superminhash, probminhash and hyperloglog algorithms as described in Ertl's papers and implemented in [probminhash](https://github.com/jean-pierreBoth/probminhash).
  - optimal densification from Shrivastava [(pmlr-2017)](https://proceedings.mlr.press/v70/shrivastava17a.html) or "reverse" optimal densification from Mai and al. [(pmlr-2020)](http://proceedings.mlr.press/v115/mai20a/mai20a.pdf)

* A probability Jaccard index taking into account Kmer multiplicity is provided with the Probminhash family algorithm associated with the probability Jaccard index.
For very long sequences where keeping the count of large Kmer costs too much memory it is possible to fallback on the SetSketch (based on HyperLogLog) sketcher or SuperMinHash algorithms also
provided in the **probminhash** crate using the usual Jaccard metric.

* The probminhash algorithm is used to provide a complete sketching of a datafile where each sequence has its signature
dumped in a file. This file can be reprocessed to examine neighborhood of a read in term of the Probability Jaccard index. see module *seqsketchjaccard.rs* or *seqblocksketch*.  
For example it takes 51s on a 8 (hyperthreaded i7 @2.3Ghz) core laptop, to read , generate 8 base kmers and sketch 746333 long reads from a 4.38 Gbases ONT fastq file (Cf [FAB49164_rel3](https://github.com/nanopore-wgs-consortium/NA12878/blob/master/nanopore-human-genome/rel_3_4.md)), asking for 200 sketches by read.

* The signatures obtained can be sent in an Ann to study read proximity according to the Jaccard Probability metric.
  See the (minimal) executable *datasketcher* in this crate and the crate [*hnsw_rs*](https://crates.io/crates/hnsw_rs)

Some others standard tools such :

* Nthash : This is a recursive hashing described in: **"ntHash: recursive nucleotide hashing"**  
     Mohamadi Chu Birol BioInformatics 2016.
It is implemented on all our compressed kmer types.

## A minimal module aautils

This module provides an uncompressed representation of Amino Acid sequences along with generation of compressed Kmer (up to a size of 12 amino acids, 5 bits bases encoded in a u64).  
This module is, in present state, minimal. It provides sketching of AA sequences in the same way as DNA sequences.

## Some basic statistics on sequences

1. Read length distributions.  
    A file giving the number of reads in function of length.  

2. Base distributions.  
    a matrix (100, 4) giving for row i and column j in (1,2,3,4) the number of reads
    where a base (a,c,g,t) corresponding to column j in this order occurs at percentage i.

This file can be reloaded by Julia package Genomics (cf BaseDistribution.jl)

## Quality

Qualities are re-mapped to values between in [0..7] so that they need only 3 bits of storage and are
stored in a wavelet matrix.
The mapping is non uniform and maps the range  [0x25,0x37] to  [1,6].  
The quality part of data are stored in a process serving quality requests described below:

### Quality Server

The server is launched on the server machine by the command:  
 **qualityloader -f filename [ -p portnum] [ --wavelet]**.

The server listens by default to port 4766, the option "--wavelet" asks for wavelet compression.

## Installation

Just download from crates.io. The qualityloader target relies on libzmq (and libsodium) which are provided by
the witzmq feature. To get the whole compiled , use cargo build --release --features="withzmq


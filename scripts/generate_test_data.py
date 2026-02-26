#!/usr/bin/env python3
import os
import random
import gzip
import datetime

# Configuration
OUTPUT_DIR = "test_data"
SEED = 42

random.seed(SEED)

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_random_seq(length, alphabet="ACGT"):
    return "".join(random.choices(alphabet, k=length))

def get_random_qual(length):
    # Phred+33 scores mostly between 30 and 40 (I to J)
    # But let's vary them a bit more: ! (33) to I (73)
    return "".join(random.choices("!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghi", k=length))

def write_fasta(filepath, num_seqs=10, min_len=50, max_len=100, wrap=80, alphabet="ACGT"):
    print(f"Generating FASTA: {filepath}")
    with open(filepath, "w") as f:
        for i in range(1, num_seqs + 1):
            length = random.randint(min_len, max_len)
            seq = get_random_seq(length, alphabet)
            f.write(f">seq_{i} description_random_length_{length}\n")
            if wrap > 0:
                for j in range(0, len(seq), wrap):
                    f.write(seq[j:j+wrap] + "\n")
            else:
                f.write(seq + "\n")

def write_fastq(filepath, num_reads=100, read_len=150, error_rate=0.01):
    print(f"Generating FASTQ: {filepath}")
    is_gz = filepath.endswith(".gz")
    opener = gzip.open if is_gz else open
    mode = "wt" if is_gz else "w"
    
    with opener(filepath, mode) as f:
        for i in range(1, num_reads + 1):
            seq = get_random_seq(read_len)
            # Inject errors? For now just random seq
            qual = get_random_qual(read_len)
            f.write(f"@read_{i}\n{seq}\n+\n{qual}\n")

def write_sam(filepath, num_records=50):
    print(f"Generating SAM: {filepath}")
    header = "@HD\tVN:1.6\tSO:unsorted\n"
    refs = [f"ref_{i}" for i in range(1, 4)]
    for ref in refs:
        header += f"@SQ\tSN:{ref}\tLN:10000\n"
    
    with open(filepath, "w") as f:
        f.write(header)
        for i in range(1, num_records + 1):
            qname = f"read_{i}"
            flag = random.choice([0, 4, 16]) # mapped, unmapped, reverse
            rname = random.choice(refs) if flag != 4 else "*"
            pos = random.randint(1, 9000) if flag != 4 else 0
            mapq = random.randint(0, 60) if flag != 4 else 0
            cigar = "100M" if flag != 4 else "*"
            rnext = "*"
            pnext = 0
            tlen = 0
            seq = get_random_seq(100)
            qual = get_random_qual(100)
            
            f.write(f"{qname}\t{flag}\t{rname}\t{pos}\t{mapq}\t{cigar}\t{rnext}\t{pnext}\t{tlen}\t{seq}\t{qual}\n")

def write_vcf(filepath, num_variants=50):
    print(f"Generating VCF: {filepath}")
    header = """##fileformat=VCFv4.2
##fileDate={date}
##source=synthetic
##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">
##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read Depth">
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tsample1\tsample2
""".format(date=datetime.date.today().strftime("%Y%m%d"))
    
    chroms = [f"chr{i}" for i in range(1, 4)]
    
    with open(filepath, "w") as f:
        f.write(header)
        pos = 0
        for i in range(1, num_variants + 1):
            chrom = random.choice(chroms)
            pos += random.randint(100, 1000)
            ref = random.choice("ACGT")
            alt = random.choice([b for b in "ACGT" if b != ref])
            qual = random.randint(30, 999)
            dp = random.randint(10, 100)
            af = round(random.random(), 3)
            info = f"DP={dp};AF={af}"
            fmt = "GT:DP"
            
            # Simple genotypes
            gt1 = random.choice(["0/0", "0/1", "1/1"])
            dp1 = random.randint(5, dp)
            s1 = f"{gt1}:{dp1}"
            
            gt2 = random.choice(["0/0", "0/1", "1/1"])
            dp2 = random.randint(5, dp)
            s2 = f"{gt2}:{dp2}"
            
            f.write(f"{chrom}\t{pos}\t.\t{ref}\t{alt}\t{qual}\tPASS\t{info}\t{fmt}\t{s1}\t{s2}\n")

def write_gff(filepath, num_features=20):
    print(f"Generating GFF3: {filepath}")
    with open(filepath, "w") as f:
        f.write("##gff-version 3\n")
        chroms = [f"chr{i}" for i in range(1, 4)]
        source = "synthetic"
        
        for i in range(1, num_features + 1):
            seqid = random.choice(chroms)
            type_ = random.choice(["gene", "mRNA", "exon", "CDS"])
            start = random.randint(1, 5000)
            end = start + random.randint(100, 2000)
            score = "."
            strand = random.choice(["+", "-"])
            phase = "."
            attrs = f"ID=feat_{i};Parent=gene_{random.randint(1,5)}"
            
            f.write(f"{seqid}\t{source}\t{type_}\t{start}\t{end}\t{score}\t{strand}\t{phase}\t{attrs}\n")

def write_bed(filepath, num_regions=20):
    print(f"Generating BED: {filepath}")
    with open(filepath, "w") as f:
        chroms = [f"chr{i}" for i in range(1, 4)]
        for i in range(1, num_regions + 1):
            chrom = random.choice(chroms)
            start = random.randint(0, 10000)
            end = start + random.randint(50, 500)
            name = f"region_{i}"
            score = random.randint(0, 1000)
            strand = random.choice(["+", "-"])
            f.write(f"{chrom}\t{start}\t{end}\t{name}\t{score}\t{strand}\n")

def write_csv(filepath, num_rows=20):
    print(f"Generating CSV: {filepath}")
    with open(filepath, "w") as f:
        f.write("id,name,value,category,notes\n")
        categories = ["A", "B", "C"]
        for i in range(1, num_rows + 1):
            name = f"item_{i}"
            val = random.randint(1, 100)
            cat = random.choice(categories)
            # Add some special chars or quotes to test robustness
            note = f"note for {i}"
            if i % 5 == 0:
                note = f'"note, with comma {i}"'
            f.write(f"{i},{name},{val},{cat},{note}\n")

def write_gfa(filepath, num_nodes=10):
    print(f"Generating GFA: {filepath}")
    with open(filepath, "w") as f:
        f.write("H\tVN:Z:1.0\n")
        # Nodes
        for i in range(1, num_nodes + 1):
            seq = get_random_seq(50)
            f.write(f"S\tnode_{i}\t{seq}\n")
        # Links
        for i in range(1, num_nodes):
            f.write(f"L\tnode_{i}\t+\tnode_{i+1}\t+\t10M\n")

def write_newick(filepath):
    print(f"Generating Newick: {filepath}")
    with open(filepath, "w") as f:
        f.write("((A:0.1,B:0.2):0.3,(C:0.4,D:0.5):0.6);\n")

def write_mtx(filepath, num_genes=100, num_cells=20):
    print(f"Generating MTX: {filepath}")
    with open(filepath, "w") as f:
        f.write("%%MatrixMarket matrix coordinate integer general\n")
        f.write("%\n")
        num_entries = num_genes * num_cells // 5 # sparsity
        f.write(f"{num_genes} {num_cells} {num_entries}\n")
        seen = set()
        for _ in range(num_entries):
            while True:
                g = random.randint(1, num_genes)
                c = random.randint(1, num_cells)
                if (g, c) not in seen:
                    seen.add((g, c))
                    count = random.randint(1, 100)
                    f.write(f"{g} {c} {count}\n")
                    break

def write_expression_table(filepath, num_genes=20):
    print(f"Generating Expression Table: {filepath}")
    with open(filepath, "w") as f:
        f.write("gene_id\tcounts\ttpm\n")
        for i in range(1, num_genes + 1):
            count = random.randint(0, 5000)
            tpm = round(random.random() * 100, 2)
            f.write(f"gene_{i}\t{count}\t{tpm}\n")

def write_taxonomy_table(filepath, num_taxa=10):
    print(f"Generating Taxonomy Table: {filepath}")
    with open(filepath, "w") as f:
        f.write("read_id\ttax_id\n")
        for i in range(1, 101):
            tax_id = random.randint(1, num_taxa)
            f.write(f"read_{i}\t{tax_id}\n")

def main():
    ensure_dir(OUTPUT_DIR)
    
    # DNA
    ensure_dir(os.path.join(OUTPUT_DIR, "dna"))
    write_fasta(os.path.join(OUTPUT_DIR, "dna/random.fa"), num_seqs=20, min_len=100, max_len=1000)
    write_fasta(os.path.join(OUTPUT_DIR, "dna/edge_cases.fa"), num_seqs=5, min_len=10, max_len=50, alphabet="ACGTNn")
    
    # FASTQ
    ensure_dir(os.path.join(OUTPUT_DIR, "fastq"))
    write_fastq(os.path.join(OUTPUT_DIR, "fastq/random.fq"), num_reads=50, read_len=100)
    write_fastq(os.path.join(OUTPUT_DIR, "fastq/random.fq.gz"), num_reads=50, read_len=100)
    
    # BAM/SAM
    ensure_dir(os.path.join(OUTPUT_DIR, "bam"))
    write_sam(os.path.join(OUTPUT_DIR, "bam/random.sam"), num_records=50)
    
    # VCF
    ensure_dir(os.path.join(OUTPUT_DIR, "vcf"))
    write_vcf(os.path.join(OUTPUT_DIR, "vcf/random.vcf"), num_variants=20)
    
    # CSV/TSV
    ensure_dir(os.path.join(OUTPUT_DIR, "csv"))
    write_csv(os.path.join(OUTPUT_DIR, "csv/random.csv"), num_rows=50)
    
    # Proteomics
    ensure_dir(os.path.join(OUTPUT_DIR, "proteomics"))
    write_fasta(os.path.join(OUTPUT_DIR, "proteomics/random.faa"), num_seqs=20, min_len=50, max_len=400, alphabet="ACDEFGHIKLMNPQRSTVWY")
    
    # Longreads
    ensure_dir(os.path.join(OUTPUT_DIR, "longreads"))
    write_fastq(os.path.join(OUTPUT_DIR, "longreads/random_long.fq"), num_reads=10, read_len=5000)
    
    # Pangenomics
    ensure_dir(os.path.join(OUTPUT_DIR, "pangenomics"))
    write_gfa(os.path.join(OUTPUT_DIR, "pangenomics/random.gfa"))

    # Phylogenomics
    ensure_dir(os.path.join(OUTPUT_DIR, "phylogenomics"))
    write_newick(os.path.join(OUTPUT_DIR, "phylogenomics/random.nwk"))

    # Singlecell
    ensure_dir(os.path.join(OUTPUT_DIR, "singlecell"))
    write_mtx(os.path.join(OUTPUT_DIR, "singlecell/random.mtx"))

    # RNA
    ensure_dir(os.path.join(OUTPUT_DIR, "rna"))
    write_fasta(os.path.join(OUTPUT_DIR, "rna/transcripts.fa"), num_seqs=10, min_len=200, max_len=2000)
    write_expression_table(os.path.join(OUTPUT_DIR, "rna/counts.tsv"))

    # Metagenomics
    ensure_dir(os.path.join(OUTPUT_DIR, "metagenomics"))
    write_fasta(os.path.join(OUTPUT_DIR, "metagenomics/contigs.fa"), num_seqs=20, min_len=500, max_len=5000)
    write_taxonomy_table(os.path.join(OUTPUT_DIR, "metagenomics/taxonomy.tsv"))
    
    # Annotation (GFF/BED) - put in dna or generic? 
    # The prompt structure has csv/, dna/, etc. GFF usually goes with DNA or generic "format" folder if one existed.
    # I'll put GFF/BED in `dna/` or `csv/`? The structure lists `gff3` section in README but directory is `dna/` or `csv/`?
    # Checking `ls -F` output earlier: `csv/`, `dna/`, `fastq/`, `vcf/`. 
    # The README shows `gff3` as a section. But `ls` output didn't show `gff3/` directory.
    # Ah, `ls -F` output showed directories: `bam/`, `csv/`, `dna/`, `fastq/`, `longreads/`, `metagenomics/`, `pangenomics/`, `phylogenomics/`, `proteomics/`, `rna/`, `singlecell/`, `vcf/`.
    # I'll put GFF in `dna/` as it relates to features on DNA.
    write_gff(os.path.join(OUTPUT_DIR, "dna/random.gff3"), num_features=20)
    write_bed(os.path.join(OUTPUT_DIR, "dna/random.bed"), num_regions=20)

    print("Synthetic data generation complete.")

if __name__ == "__main__":
    main()

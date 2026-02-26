# Convert vcf in parquet 🧬 💻

[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/natir/vcf2parquet/blob/master/LICENSE)
![CI](https://github.com/natir/vcf2parquet/workflows/CI/badge.svg)
[![Documentation](https://github.com/natir/vcf2parquet/workflows/Documentation/badge.svg)](https://natir.github.io/vcf2parquet/vcf2parquet)
[![CodeCov](https://codecov.io/gh/natir/vcf2parquet/vcf2parquetanch/master/graph/badge.svg)](https://codecov.io/gh/natir/vcf2parquet)


## Install

```
mamba install vcf2parquet
```

## Usage

```
vcf2parquet-bin

USAGE:
    vcf2parquet [OPTIONS] --input <INPUT> <SUBCOMMAND>

OPTIONS:
    -b, --batch-size <BATCH_SIZE>      Batch size (default 100,000)
    -c, --compression <COMPRESSION>    Compression method (default snappy) [possible values:
                                       uncompressed, snappy, gzip, lzo, brotli, lz4]
    -h, --help                         Print help information
    -i, --input <INPUT>                Input path

SUBCOMMANDS:
    convert    Convert a vcf in a parquet
    help       Print this message or the help of the given subcommand(s)
    split      Convert a vcf in multiple parquet file each file contains `batch_size` record
```

Subcommand convert and split change how output is write.

```
vcf2parquet -i {input}.vcf.[gz|bz2|xz] convert -o {output}.parquet
vcf2parquet -i {input}.vcf.[gz|bz2|xz] -c lz4 -b 10000 convert -o {output}.parquet
vcf2parquet -i {input}.vcf.[gz|bz2|xz] split -f format_partition_{}.parquet
```

## Minimum supported Rust version

Currently the minimum supported Rust version is 1.74.1.


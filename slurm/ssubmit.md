# ssubmit

[![Rust CI](https://github.com/mbhall88/ssubmit/actions/workflows/ci.yaml/badge.svg)](https://github.com/mbhall88/ssubmit/actions/workflows/ci.yaml)
[![codecov](https://codecov.io/gh/mbhall88/ssubmit/branch/main/graph/badge.svg?token=4O7HTGKD6Q)](https://codecov.io/gh/mbhall88/ssubmit)
[![Crates.io](https://img.shields.io/crates/v/ssubmit.svg)](https://crates.io/crates/ssubmit)

Submit sbatch jobs without having to create a submission script

- [Motivation](#motivation)
- [Install](#install)
- [Usage](#usage)


## Motivation

This project is motivated by the fact that I want to just be able to submit commands as
jobs and I don't want to fluff around with making a submission script.

`ssubmit` wraps that whole process and lets you live your best lyf #blessed.

## Install

**tl;dr**

```shell
curl -sSL install.ssubmit.mbh.sh | sh
# or with wget
wget -nv -O - install.ssubmit.mbh.sh | sh
```

You can pass options to the script like so

```
$ curl -sSL install.ssubmit.mbh.sh | sh -s -- --help
install.sh [option]

Fetch and install the latest version of ssubmit, if ssubmit is already
installed it will be updated to the latest version.

Options
        -V, --verbose
                Enable verbose output for the installer

        -f, -y, --force, --yes
                Skip the confirmation prompt during installation

        -p, --platform
                Override the platform identified by the installer [default: apple-darwin]

        -b, --bin-dir
                Override the bin installation directory [default: /usr/local/bin]

        -a, --arch
                Override the architecture identified by the installer [default: x86_64]

        -B, --base-url
                Override the base URL used for downloading releases [default: https://github.com/mbhall88/ssubmit/releases]

        -h, --help
                Display this help message
```


### Cargo

```shell
$ cargo install ssubmit
```

### Build from source

```shell
$ git clone https://github.com/mbhall88/ssubmit.git
$ cd ssubmit
$ cargo build --release
$ target/release/ssubmit -h
```

## Usage

Submit an rsync job named "foo" and request 350MB of memory and a one week time limit

```shell
$ ssubmit -m 350m -t 1w foo "rsync -az src/ dest/"
```

Submit a job that needs 8 CPUs

```shell
$ ssubmit -m 16g -t 1d align "minimap2 -t 8 ref.fa query.fq > out.paf" -- -c 8
```

The basic anatomy of a `ssubmit` call is

```
ssubmit [OPTIONS] <NAME> <COMMAND> [-- <REMAINDER>...]
```

`NAME` is the name of the job (the `--job-name` parameter in `sbatch`).

`COMMAND` is what you want to be executed by the job. It **must** be quoted (single or
double).

`REMAINDER` is any (optional) [`sbatch`-specific options](https://slurm.schedmd.com/sbatch.html#lbAG) you want to pass on. These
must follow a `--` after `COMMAND`.

### Memory

Memory (`-m,--mem`) is intended to be a little more user-friendly than the `sbatch
--mem` option. For example, you can pass `-m 0.5g` and `ssubmit` will interpret and
convert this as 500M. However, `-m 1.7G` will be rounded up to 2G. One place where this
option differs from `sbatch` is that if you don't give units, it will be interpreted as
bytes - i.e., `-m 1000` will be converted to 1K. Units are case insensitive.

### Time

As with memory, time (`-t,--time`) is intended to be simple. If you want a time limit of
three days, then just pass `-t 3d`. Want two and a half hours? Then `-t 2h30m` works. If
you want to just use the default limit of your cluster, then just pass `-t 0`. You can
also just pass the [time format `sbatch` uses](https://slurm.schedmd.com/sbatch.html#OPT_time) and this will be seamlessly passed on. For
a full list of supported time units, check out the
[`duration-str`](https://github.com/baoyachi/duration-str) repo.

### Dry run

You can see what `ssubmit` would do without actually submitting a job using dry run
(`-n,--dry-run`). This will print the `sbatch` command and also the submission script
that would have been provided.

```shell
$ ssubmit -n -m 4g -t 1d dry "rsync -az src/ dest/" -- -c 8
[2022-01-19T08:58:58Z INFO  ssubmit] Dry run requested. Nothing submitted
sbatch -c 8 <script>
=====<script>=====
#!/usr/bin/env bash
#SBATCH --job-name=dry
#SBATCH --mem=4G
#SBATCH --time=24:0:0
#SBATCH --error=%x.err
#SBATCH --output=%x.out
set -euxo pipefail

rsync -az src/ dest/
=====<script>=====
```

### Script settings

The default shebang for the script is `#!/usr/bin/env bash`. However, if you'd prefer
something else, pass this with `-S,--shebang`.

Additionally, we use `set -euxo pipefail` by default, which will exit when a command exits with a
non-zero exit code (`e`), error when trying to use an unset variable (`u`), print
all commands that were run to stderr (`x`), and exit if a command in a pipeline fails 
(`-o pipefail`). You can change these setting with `-s,--set`. You can turn this off 
by passing `-s ''`.

### Log files

By default, the stderr and stdout of the job are sent to `%x.err` and `%x.out`,
respectively. `%x` is a filename pattern for job name. So if the job name is foo, the
stderr file will be `foo.err`. You can see all available patterns in
[the docs](https://slurm.schedmd.com/sbatch.html#SECTION_%3CB%3Efilename-pattern%3C/B%3E).
You don't have to use patterns of course.

### Full usage

```shell
$ ssubmit --help
ssubmit 0.2.0
Michael Hall <michael@mbh.sh>
Submit sbatch jobs without having to create a submission script

-----------
# EXAMPLES
-----------

Submit a simple rsync command with a 600MB memory limit.

$ ssubmit -m 600m rsync_my_data "rsync -az src/ dest/"

Submit a command that involves piping the output into another command. sbatch options
are passed after a `--`.

$ ssubmit -m 4G align "minimap2 -t 8 ref.fa reads.fq | samtools sort -o sorted.bam" -- -c 8

USAGE:
    ssubmit [OPTIONS] <NAME> <COMMAND> [-- <REMAINDER>...]

ARGS:
    <NAME>
            Name of the job

            See `man sbatch | grep -A 2 'job-name='` for more details.

    <COMMAND>
            Command to be executed by the job

    <REMAINDER>...
            Options to be passed on to sbatch

OPTIONS:
    -e, --error <ERROR>
            File to write job stderr to. (See `man sbatch | grep -A 3 'error='`)

            Run `man sbatch | grep -A 37 '^filename pattern'` to see available patterns.

            [default: %x.err]

    -h, --help
            Print help information

    -m, --mem <size[units]>
            Specify the real memory required per node. e.g., 4.3kb, 7G, 9000, 4.1MB

            Note, floating point numbers will be rounded up. e.g., 10.1G will request 11G. This is
            because sbatch only allows integers. See `man sbatch | grep -A 4 'mem='` for the full
            details.

            [default: 1G]

    -n, --dry-run
            Print the sbatch command and submission script would be executed, but do not execute
            them

    -o, --output <OUTPUT>
            File to write job stdout to. (See `man sbatch | grep -A 3 'output='`)

            Run `man sbatch | grep -A 37 '^filename pattern'` to see available patterns.

            [default: %x.out]

    -s, --set <SET>
            Options for the set command in the shell script

            For example, to exit when the command exits with a non-zero code and to treat unset
            variables as an error during substitution, pass 'eu'. Pass '' or "" to set nothing

            [default: "euxo pipefail"]

    -S, --shebang <SHEBANG>
            The shell shebang for the submission script

            [default: "#!/usr/bin/env bash"]

    -t, --time <TIME>
            Time limit for the job. e.g. 5d, 10h, 45m21s (case insensitive)

            Run `man sbatch | grep -A 7 'time=<'` for more details.

            [default: 1w]

    -T, --test-only
            Return an estimate of when the job would be scheduled to run given the current queue. No
            job is actually submitted. [sbatch --test-only]

    -V, --version
            Print version information
```


[releases]: https://github.com/mbhall88/ssubmit/releases
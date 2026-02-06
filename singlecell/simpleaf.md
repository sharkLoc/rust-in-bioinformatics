# simpleaf

`simpleaf` is a `rust` framework to make using `alevin-fry` _even_ simpler. `simpleaf` encapsulates the process of creating an expanded reference for quantification into a single command (`index`) and the quantification of a sample into a single command (`quant`).  It also exposes various other functionality, and is actively being developed and expanded.

The `simpleaf` program can be installed from source, from [crates.io](https://crates.io/crates/simpleaf), or via [bioconda](https://bioconda.github.io/recipes/simpleaf/README.html). `simpleaf` requires, [`alevin-fry`](https://github.com/COMBINE-lab/alevin-fry), and either [`piscem`](https://github.com/COMBINE-lab/piscem) or [`salmon`](https://github.com/COMBINE-lab/salmon) (or both, if you prefer), as well as [`wget`](https://www.gnu.org/software/wget/).

**Note**: We recommend using [`piscem`](https://github.com/COMBINE-lab/piscem) as the back-end mapper, rather than `salmon`, as it is substantially more resource-frugal, faster, and is a larger focus of current and future development.  If you have any difficulty related to building an index using `piscem`, before you file an issue on GitHub, please make sure you try to increase your file handle limit (e.g. as is described [here](https://github.com/COMBINE-lab/cuttlefish/blob/master/README.md#note)).

Check out the detailed documentation [here](https://simpleaf.readthedocs.io/en/latest/), and read on below to learn more about the background and motivation behind `simpleaf`.

## Note(s)

- **Please ensure that the user file handle limit is set to 2048**.  This may already be set (and should be fine already on OSX), but you can accomplish this by executing:

```
$ ulimit -n 2048
```

before running `simpleaf`.

- **If you are using `simpleaf` to build an index on a compute cluster or a machine with a networked file system** (NFS), be sure to set the **output** directory and the **working** directory to be on a **local** disk (e.g. a scratch or temp disk not mounted via the networked file system). The index construction creates many small files to control memory usage, this represents an adversarial scenario for networked file systems, and running the index construction using an NSF attached location as the working directory may slow the process down incredibly (by an order of magnitude or more).  In such a scenario, it is recommended to set the working and output directories to be on local disk, and then to simply copy the resulting index over to the desired location on the NFS if you will be accessing it from multiple nodes.

## Introduction & motivation 

 * **Q(s)** : What is the purpose of `simpleaf`? Isn't its functionality covered by the constituent programs (e.g. `salmon`, `alevin-fry`, `piscem`, etc.)? Can't I make those tools do the same things `simpleaf` does?

 * **A** : Yes! It is, of course, possible to replicate the functionality of `simpleaf` by building a script or workflow around the underlying tools. However, `simpleaf` is designed to make the most common use cases simpler, while also retaining critical flexibility where necessary.  Further, `simpleaf` also provides some extra functionality that one would have to build themselves if wrapping the underlying tools, and simplifies the use of different mapping backends (i.e. `salmon` or `piscem`). For more details, read on below.

The relevant tools that drive `simpleaf` (i.e. {`salmon` \| `piscem`} and `alevin-fry`) are all command-line tools meant to be used together. For those who are very comfortable with the command-line, these tools are designed to be straightforward to use.  Further, they are designed to be highly-configurable, so that they can be run in different ways, with different configurations, based upon what the user wants to accomplish.  In fact, many users of `alevin-fry` have crafted their own scripts or pipelines chaining these tools together using `bash` scripts, custom `python` scripts, or specially-built pipeline tools like `snakemake` and `nextflow`.

While this mode of interaction makes a lot of sense for folks who are very comfortable with the command line and scripting, and who need maximum control over how each aspect of the tools is run, it can seem a bit daunting when one is performing a common task without the need for more exotic configurations.  In that case, it should be possible to further simplify the interface to provide a simple command akin to something like [`cellranger count`](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/using/count). 

Initially, we designed a Nextflow workflow ([quantaf](https://github.com/COMBINE-lab/quantaf)) for wrapping these tools and processing data based on a simple spreadsheet of input.  While that approach works well when one needs to process a lot of data, and is easily scalable to many different compute environments thanks to `Nextflow`, it is a somewhat heavyweight solution.  Further, accounting for some current and future directions of development, we also sought a solution where we might selectively employ programmatic (i.e. library-level), rather than file or channel-based communication between the different underlying components. 

Therefore, inspired by the flexible yet simple-to-use interface of tools like [`cellranger`](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/what-is-cell-ranger) (developed by 10X Genomics) and [`kb-python`](https://github.com/pachterlab/kb_python) (developed by the Pachter lab at Caltech), we decided that it made sense to build a stand-alone tool to provide a simplified but flexible interface for our underlying workflows.  We also sought to allow some of the modularity provided by tools such as [nf-core's scrnaseq](https://nf-co.re/scrnaseq) pipeline by allowing the use of more than one mapping backend.

While a scripting language like [`ruby`](https://www.ruby-lang.org/en/), [`python`](https://www.python.org/) or [`perl`](https://www.perl.org/) is a natural choice for such an intelligent "wrapper" or "pipeline" tool, we chose to develop `simpleaf` in [`rust`](https://www.rust-lang.org/), which actually turns out to work quite well for tasks such as this.  While there are several reasons for this decision, a major motivation for this choice is that, as we develop new tools with and transition other functionality over to `rust`, having `simpleaf` written in `rust` will allow for direct programmatic (i.e. library-level) interaction between some of the tools, rather than relying on independent process management and communication.

Finally, while `simpleaf` is ready-to-use (we use it regularly to process single-cell data), it is still under active development, with new features and capabilities being added.  If you have feature suggestions or feedback on directions in which you'd like to see `simpleaf` grow, please let us know in the [issues](https://github.com/COMBINE-lab/simpleaf/issues) or [discussions](https://github.com/COMBINE-lab/simpleaf/discussions).


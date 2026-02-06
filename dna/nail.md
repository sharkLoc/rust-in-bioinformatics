# nail workspace

## About

This is a cargo workspace for nail, which is a profile Hidden Markov Model (pHMM) biological sequence alignment tool.
Using the fast [MMseqs2](https://github.com/soedinglab/MMseqs2) search pipeline to produce candidate alignment seeds, nail computes a fast approximation of the [HMMER3](http://hmmer.org/) Forward/Backward (F/B) sequence alignment algorithm.
Currently, nail only supports amino acid search, with nucleotide search coming in a future update.

The nail preprint paper can be found on bioRxiv (doi: https://doi.org/10.1101/2024.01.27.577580).

### What's here
There are two sub-projects in the nail workspace:
1. `nail`: this is the command line tool
2. `libnail`: this is a Rust library that contains the implementation of nail's sparse alignment algorithms

### Example input files

A few example input files may be found under the `fixtures/` directory at the root of this repository.
    
    $ ls fixtures/
    query.fa  target.fa  query.hmm

## Dependencies

The `nail search` pipeline uses the `mmseqs search` tool as an alignment prefilter.
In the future, we will replace this with our own prefiltering strategies.

nail has been tested with [MMseqs2 Release 15-6f452](https://github.com/soedinglab/MMseqs2/releases/tag/15-6f452).
We have not tested nail against other versions of MMseqs2, but they may work.

To run the `nail search` pipeline, `mmseqs search` must be available in your system path.

## Installation

You can find precompiled binaries for various platforms on the [latest release page](https://github.com/TravisWheelerLab/nail/releases/tag/nail-v0.4.0).

### Building from source

To install nail from source, you'll need the Rust development tooling, which means you'll need to install the Rust compiler and Cargo.
The easiest way to do that is to use [rustup](https://rustup.rs/).

Once you've done that, you can clone this repository and build the project with Cargo:

    git clone https://github.com/TravisWheelerLab/nail
    cd nail/
    cargo build --release

You'll then find the compiled binary at: `target/release/nail`

For example, try running:

    target/release/nail -h

## Usage

The nail command line interface uses subcommands. 

Currently, there is only one subcommand: `search` 

*Note: that may seem a little strange, but we will be adding subcommands in the near future

### nail search

The `nail search` command runs the entire nail pipeline, including running MMseqs2 to find alignment seeds.

The input to `nail search` is a query file (p7HMM or FASTA) and a target sequence database file (FASTA).

By default, the search results will be written to `./results.tbl` in a tabular format, and alignment output is written to stdout.
In addition, a collection of temporary files required to run `mmseqs search`, will be written to the `./tmp/` directory.

For example, when running nail search, you'll see something like:

    $ nail search query.hmm target.fa 
    reading query database...   done (0.00s)
    indexing target database... done (0.00s)
    running mmseqs...           done (0.44s)
    running nail pipeline...    done (0.16s)    

Checking the `results.tbl` will look something like:

    $ head -n 15 results.bl
    #                                                                         target target query query       comp         cell  
    # target                                                  query           start  end    start end   score bias evalue  frac  
    # ------------------------------------------------------- --------------- ------ ------ ----- ----- ----- ---- ------- ----- 
    F1MV99|reviewed|Somatostatin                              7tm_1-consensus 58     306    1     260   175.8 7.5  1.0e-53 0.066
    O08858|reviewed|Somatostatin                              7tm_1-consensus 54     303    1     260   173.0 7.8  7.7e-53 0.069
    C3ZQF9|reviewed|QRFP-like                                 7tm_1-consensus 64     326    1     260   149.3 8.6  1.3e-45 0.070
    O02813|reviewed|Neuropeptide                              7tm_1-consensus 56     319    1     260   147.9 5.4  3.5e-45 0.070
    O08565|reviewed|C-X-C                                     7tm_1-consensus 52     299    1     260   145.8 5.3  1.5e-44 0.076
    O02835|reviewed|Neuropeptide                              7tm_1-consensus 57     320    1     260   145.7 6.8  1.6e-44 0.071
    A0T2N3|reviewed|Apelin                                    7tm_1-consensus 51     316    1     260   145.0 4.3  2.6e-44 0.077
    O08726|reviewed|Galanin                                   7tm_1-consensus 42     292    1     260   144.9 4.2  2.8e-44 0.073
    O08556|reviewed|C-C                                       7tm_1-consensus 49     299    1     260   144.3 5.3  4.4e-44 0.073
    F1R332|reviewed|Galanin                                   7tm_1-consensus 35     286    1     260   143.3 3.8  8.9e-44 0.077
    D4A7K7|reviewed|G-protein                                 7tm_1-consensus 44     304    1     260   142.7 4.3  1.3e-43 0.073
    E7F7V7|reviewed|Galanin                                   7tm_1-consensus 43     294    1     260   142.6 1.7  1.4e-43 0.073


nail can also produce alignment output if you supply an `--ali-out` argument:

    $ nail search --ali-out results.ali query.hmm target.fa 


Checking the `results.ali` will look something like:

    $ head -n 70 results.ali
    query:        7tm_1
    target:       O08892|reviewed|5-hydroxytryptamine
    query start:  2
    query end:    260
    target start: 66
    target end:   368
    score:        257.7
    comp bias:    9.3
    E-value:      6.3e-79
    cell frac:    0.094
    
    ==
    
                                  7tm_1     2 NllVilvilrnkklrtptnifllnLavaDllvlllvlpfslvyallegdwvfgevlCklvtaldvvnltasillltaisi 81   
                                              N +Vi++++r++kl+tp+n+++ +La++Dllv++lv+p+s++y++ +g+w++g++lC+++ + d++++tasi++l++i++
    O08892|reviewed|5-hydroxytryptamine    66 NAFVIATVYRTRKLHTPANYLIASLAFTDLLVSILVMPISTMYTV-TGRWTLGQALCDFWLSSDITCCTASIMHLCVIAL 144  
                                              9********************************************06*********************************
    
                                  7tm_1    82 DRYlaIvkplkykrirtkrralvlilvvWvlalllslppllfsgtktesaekeetvClidfpeeestwevsytlllsvlg 161  
                                              DRY+aI+ ++ y+++rt+rra+ +i++vWv+++++slpp+++++ k e   +e+  Cl+++++      v yt++++ ++
    O08892|reviewed|5-hydroxytryptamine   145 DRYWAITDAVGYSAKRTPRRAAGMIALVWVFSICISLPPFFWRQAKAE---EEVLDCLVNTDH------VLYTVYSTGGA 215  
                                              *****************************************777666500099******99990000009**********
    
                                  7tm_1   162 fllpllvilvcyvrilrtlrksakkeks.................................................... 189  
                                              f+lp+l+++ +y ri+ ++r++  k++                                                     
    O08892|reviewed|5-hydroxytryptamine   216 FYLPTLLLIALYGRIYVEARSRILKQTPNKTGKRLTRAQLITDSPGSTSSVTSINSRAPEVPCDSGSPVYVNQVKVRVSD 295  
                                              ***********************9999899999999999999999999********************************
    
                                  7tm_1   190 ....rkkksarkerkalktllvvvvvfvlcwlPyfilllldsllkeceseklve.tallitlllayvnsclNPiiY 260  
                                                  +kk +a++erka+ktl+v++++f++cwlP+fi++l++ +   c++ +  + ++++++++l+y+ns++NPiiY
    O08892|reviewed|5-hydroxytryptamine   296 ALLEKKKLMAARERKATKTLGVILGAFIVCWLPFFIISLVMPI---CKDACWFHMAIFDFFTWLGYLNSLINPIIY 368  
                                              ***9999************************************000777666551666******************
    
    //
    
    query:        7tm_1
    target:       O02666|reviewed|Alpha-1D
    query start:  1
    query end:    260
    target start: 118
    target end:   407
    score:        255.6
    comp bias:    5.5
    E-value:      2.8e-78
    cell frac:    0.061
    
    ==
    
                       7tm_1     1 gNllVilvilrnkklrtptnifllnLavaDllvlllvlpfslvyallegdwvfgevlCklvtaldvvnltasillltais 80   
                                   gNllVil +++n++l+t+tn+f++nLavaDll++++vlpfs++ ++l g w fg+++C+++ a+dv+++tasil+l+ is
    O02666|reviewed|Alpha-1D   118 GNLLVILSVACNRHLQTVTNYFIVNLAVADLLLSATVLPFSATMEVL-GFWAFGRAFCDVWAAVDVLCCTASILSLCTIS 196  
                                   8*********************************************70********************************
    
                       7tm_1    81 iDRYlaIvkplkykrirtkrralvlilvvWvlalllslppllfsgtktesaekeetvClidfpeeestwevsytlllsvl 160  
                                   +DRY+ + + lky++i+t r+a++++++ W++al++s+ pll  g+k+  +  +e++C i+ +         y++++s++
    O02666|reviewed|Alpha-1D   197 VDRYVGVRHSLKYPAIMTERKAAAILALLWAVALVVSMGPLL--GWKEPVP-PDERFCGITEEV-------GYAVFSSLC 266  
                                   ******************************************00677776609*******87650000000*********
    
                       7tm_1   161 gfllpllvilvcyvrilrtlrksakkeks............................................rkkksar 196  
                                   +f+lp+ vi+v+y+r++  +r++ ++ +                                              +  +++
    O02666|reviewed|Alpha-1D   267 SFYLPMAVIVVMYCRVYVVARSTTRSLEAGVKRERGKASEVVLRIHCRGAASGADGAPGTRGAKGHTFRSSLSVRLLKFS 346  
                                   ***************************99999999999999999999999999999999999999999999986677778
    
                       7tm_1   197 kerkalktllvvvvvfvlcwlPyfilllldsllkeceseklvetallitlllayvnsclNPiiY 260  
                                   +e+ka+ktl++vv+vfvlcw+P+f++l l sl    ++ k +e +++++ +l+y+nsc+NP+iY
    O02666|reviewed|Alpha-1D   347 REKKAAKTLAIVVGVFVLCWFPFFFVLPLGSL---FPQLKPSEGVFKVIFWLGYFNSCVNPLIY 407  
                                   899*****************************0009****************************
    
    //
    
    ...
    ...
    ...

### nail seeds

If you run `nail search --only-seed` command, nail will run MMseqs2, produce a `seeds.json` file, and terminate.
This may be useful if you would like to experiment with different nail settings using the same seeds.

For example:

    $ nail search --only-seed query.hmm target.fa

You can also save the seeds from a full run of the `nail search` pipeline by supplying a `--seeds-out` argument:

    $ nail search --seeds-out seeds.json query.hmm target.fa

Seeds can be provided to `nail search` using the `--seeds <seeds.json>` flag, which will skip the seed step in the search pipeline.

    $ nail search --seeds seeds.json query.hmm target.fa

In practice, these seeds may be produced from any source as long as they are formatted in the following way:

```
{
  "query1": {
    "target1": {
      "seq_start": 48, //  <-  these are the positions from which
      "seq_end": 287,  //  <   nail will begin the cloud search
      "prf_start": 1, //  <   
      "prf_end": 259, //  <
      "score": 168.0      //  <---  the score field is used to pick between
    },                              seeds that compete with each other
    "target2": {
      "seq_start": 72,
      "seq_end": 343,
      "prf_start": 23,
      "prf_end": 259,
      "score": 106.0
    },
  "query2": {
    "target3": {
      "seq_start": 56,
      "seq_end": 303,
      "prf_start": 1,
      "prf_end": 259,
      "score": 125.0
    },
  }
  ...
}
```

We plan to make the use of custom seeds more robust in the future.

## License

nail is licensed under the BSD-3-Clause license.

See `LICENSE` for details.

## Authors

Jack Roddy - jroddy@arizona.edu


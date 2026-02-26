# vcfexpress

> [!CAUTION]
> While the output of vcfexpress is tested and reliable, the error messages might be lacking. Please [report](https://github.com/brentp/vcfexpress/issues).

[![Rust](https://github.com/brentp/vcfexpress/actions/workflows/rust.yml/badge.svg)](https://github.com/brentp/vcfexpress/actions/workflows/rust.yml) [![DOI](https://zenodo.org/badge/786874644.svg)](https://doi.org/10.5281/zenodo.14756837)

This is an experiment on how to implement user-expressions
that can filter (and modify) a VCF and specify an output template.
It uses lua as the expression language. It is [fast](https://brentp.github.io/vcfexpress/speed.html)
Because of the speed and flexibility, we can, for example implement
[CSQ parsing](https://github.com/brentp/vcfexpress/blob/main/scripts/csq.lua) in lua,
just as a user could. The resulting functionality is as [fast or faster](https://brentp.github.io/vcfexpress/speed.html) than other tools
that have this built in.

For the optional output template, it uses [luau string templates](https://luau-lang.org/syntax#string-interpolation)
where luau is lua with some extensions and very good speed.

# Installation

+ For rust users: `cargo install vcfexpress`
+ Otherwise see [Releases](https://github.com/brentp/vcfexpress/releases) for a static linux binary

# Examples

Further examples are collected [here](examples/README.md) and we encourage users to suggest
helpful examples or snippets.

<details>
<summary>Short functionality examples</summary>

---
extract a single variant and output a bed of the variant:

```
vcfexpress filter -e "return variant.id == 'rs2124717267'" \
    --template '{variant.chrom}\t{variant.start}\t{variant.stop}' -o var.bed $vcf
```

---
filter based on INFO and write bcf:

```
vcfexpress filter -e "return variant:info('AN') > 3000" \
   -o high_an.bcf $input_vcf
```

---
check the sample fields to get variants where `all` samples have high DP.
`all` is defined by `vcfexpress` (`any`, `filter` are also available).
Users can load their own functions with `-p $lua_file`.

```
vcfexpress filter \
   -e 'return all(function (dp)  return dp > 10 end, variant:format("DP"))' \
   -o all-high-dp.bcf $input_vcf
```

---

Extract variants that are HIGH impact according to the `CSQ` field. This uses
user-defind code to parse the CSQ field in scripts/csq.lua.

```
vcfexpress filter \
   -e 'csqs = CSQS.new(variant:info("ANN"), desc); return csqs:any(function(c) return c["Annotation_Impact"] == "HIGH" end)' \
   -o all-high-impact.bcf $input_vcf \
   -p scripts/csq.lua -p scripts/pre.lua
```

---

get all of the FORMAT fields for a single sample into a lua table.
find variant that are high-quality hom-alts.

```
vcfexpress filter \
   -e 's=variant:sample("NA12878"); return s.DP > 10 and s.GQ > 20 and s.GT[1] == 1 and s.GT[2] == 1' \
   -o output.bcf \
   input.vcf
```

---

add a new info field (`af_copy`) and set it.

```
$ cat pre.lua
header:add_info({ID="af_copy", Number=1, Description="adding a single field", Type="Float"})
```

then run with:

```
vcfexpress filter -p pre.lua -e 'return variant:format("AD")[1][2] > 0' \
   -s 'af_copy=return variant:info("AF", 0)' \
   input.vcf > output.vcf
```

</details>

# speed

see [speed](https://brentp.github.io/vcfexpress/speed.html)

# Lua API

Full documentation of lua attributes and methods is [here](lua-api.md)

```lua
variant.chrom -> string
variant.REF (get/set) -> string
variant.ALT (get/set) -> vec<string>
variant.id (get/set) -> string
variant.start -> integer
variant.stop -> integer
variant.pos (get/set) -> integer -- 0-based
variant.qual (get/set) -> number
variant.filters (get/set) -> vec<string>
variant.FILTER (get/set) -> string (only first one reported)
variant.genotypes -> vec<Genotype>
variant:format("field_name") -> vec<string|number>
-- optional 0-based 2nd arg to info() gets just the desired index.
variant:info("field_name") -> number|string|bool|vec<number|string|bool>
-- useful to pprint(variant:sample("mysample")) to see available fields.
variant:sample("sample_name") -> table<string=any>
-- get all samples at once, more efficient than calling sample() multiple times
variant:samples() -> table<sample_name=table<string=any>> -- e.g. s = variant:samples(); s.NA12878.DP
tostring(variant) -> string -- tab-delimited vcf/variant output.

genotypes = variant.genotypes
genotype = genotypes[i] -- get single genotype for 1 sample
tostring(genotype) -- e.g. "0/1"
genotype.alts -- integer for number of non-zero, non-unknown alleles

allele = genotype[1]
allele.phased -> bool
allele.allele -> integer e.g. 0 for "0" allele

header.samples (set/get) -> vec<string> -- TODO: allow setting samples before iteration.
header:info_get("DP") -> table<string,string>
header:format_get("AD") -> table<string,string>

-- these header:add_* are available only in the prelude. currently only Number=1 is supported.
header:add_info({Type="Integer", Number=1, Description="asdf", ID="new field"})
header:add_format({Type="Integer", Number=1, Description="xyz", ID="new format field"})
header:add_filter({ID="LowQual", Description="Qual less than 50"})

sample = variant:sample("NA12878")
sample.DP -- any fields in the row are available. special case for GT. use pprint to see structure:
pprint(sample)
--[[
{  .GQ = 63,
  .DP = 23,
  .GT = { -- GT gives index into alt alles (or -1 for .)
    [1] = 0,
    [2] = 1},
  .AD = {
    [1] = 23,
    [2] = 0},
  .PL = {
    [1] = 0,
    [2] = 63,
    [3] = 945},
  -- this is the genotype phase.  so with GT, this is 0|1
  .phase = {
    [1] = false,
    [2] = true}}
--]]
```

# Usage

```
Filter a VCF/BCF and optionally print by template expression. If no template is given the output will be VCF/BCF

Usage: vcfexpress filter [OPTIONS] <PATH>

Arguments:
  <PATH>  Path to input VCF or BCF file

Options:
  -e, --expression <EXPRESSION>
          boolean Lua expression(s) to filter the VCF or BCF file
  -s, --set-expression <SET_EXPRESSION>
          expression(s) to set existing INFO field(s) (new ones can be added in prelude) e.g. --set-expression "AFmax=math.max(variant:info('AF'), variant:info('AFx'))"
  -t, --template <TEMPLATE>
          template expression in luau: https://luau-lang.org/syntax#string-interpolation. e.g. '{variant.chrom}:{variant.pos}'
  -p, --lua-prelude <LUA_PRELUDE>
          File(s) containing lua(u) code to run once before any variants are processed. `header` is available here to access or modify the header
  -o, --output <OUTPUT>
          Optional output file. Default is stdout
  -b, --sandbox
          Run lua code in https://luau.org/sandbox
  -h, --help
          Print help
```


# IBECS to OMTD Transformer

## Overview

This single-script command-line application allows the transformation of IBECS XML documents into the OMTD-SHARE corpus format. The script takes the IBECS XML document and the name of the OMTD corpus directory to create as inputs. It then proceeds to transform all IBECS documents into OMTD "full-text" docu ments (the abstracts) as well as OMTD metadata records (in OMTD-SHARE XML format). It approximately transforms 200 IBECS records per second, and takes around 15 minutes to transform the nearly 170,000 IBECS records found in the December 2017 version of IBECS.

## Usage

`ibecs-to-omtd-parser.py [options] IBECS_FILE OMTD_DIR`

Where:

- `IBECS` is the IBECS input XML file
- `OMTD_DIR` is the name of the output directory (to create)

In addition, the following optional arguments can be set:

```
  -h, --help            show this help message and exit
  -f, --force           overwrite the corpus if it exists
  --encoding ENCODING   text encoding for abstracts [UTF-8]
  --abstracts ABS_PATH  rel. path for abstracts [fulltext]
  --version             show program's version number and exit
  --verbose, -v         increase log level [WARN]
  --quiet, -q           decrease log level [WARN]
  --logfile FILE        log to file instead of <STDERR>
```

So a typical execution of the script might look as follows:

`python3 ibecs-to-omtd-parser.py -v IBECS.xml OMTD`

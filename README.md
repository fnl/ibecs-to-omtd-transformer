# IBECS to OMTD Transformer

## Overview

This Python 3.x command-line application allows the transformation of IBECS XML documents into an OMTD-SHARE corpus directory. The script takes the IBECS XML input document and the name of the OMTD corpus output directory as required command-line arguments. It then proceeds to transform every single abstract in the IBECS records into OMTD a "full-text" document, as well as at least one OMTD-SHARE XML metadata document per IBECS record, or minimally as many as there are abstracts. It approximately transforms 200 IBECS records per second, and takes around 15 minutes to transform nearly 170,000 IBECS records found in the December 2017 release of IBECS, on a 2.7 GHz machine, using a single processor core.

## Usage

`ibecs-to-omtd-parser.py [options] IBECS_FILE OMTD_DIR`

Where:

- `IBECS` is the IBECS input XML file
- `OMTD_DIR` is the name of the output directory (to create)

In addition, the following optional arguments can be set:

```
  -h, --help            show the help message and exit
  -f, --force           overwrite the corpus if it exists
  --encoding ENCODING   text encoding for the abstracts [default: UTF-8]
  --abstracts ABS_PATH  direcotry name for the abstracts [default: fulltext]
  --version             show the program's version number and exit
  --verbose, -v         increase log level [default: WARN]
  --quiet, -q           decrease log level [default: WARN]
  --logfile FILE        log to FILE instead of <STDERR>
```

## Delivering an OMTD corpus

A typical execution of the script will look as follows:

`python3 ibecs-to-omtd-parser.py -v IBECS.xml OMTD`

That will require that a proper Python 3 installation is available on the machine to execute the script, the `-v` option increases the logging verbosity (to INFO level), and the script will expect to read the IBECS records from a file called `IBECS.xml` that must be in the current directory, and will also create an output directory named `OMTD` that will contain the OMTD corpus, also in the current directory where this script is being executed.

After the transformation is complete (as said, for a full IBECS database and typical CPU that can take 15 minutes or more), the IBECS maintainer should manually verify the created corpus contains the same number of abstracts (in the "fulltext" directory) as are found in the IBECS database and the expected number of metadata records, while a license file in the "licence" directory should always be created by the script. Once all that has been verified, the directory should be zipped and the resulting archive provided to the OMTD maintainers using the agreed upon delivery channel.

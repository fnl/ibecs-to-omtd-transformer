#!/usr/bin/env python3

# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A
# PARTICULAR PURPOSE.
#
# This notice may not be removed from the software by any user thereof.
import hashlib
import logging
import os
import shutil
import sys
# noinspection PyPep8Naming
import xml.etree.ElementTree as et
from argparse import ArgumentParser
from datetime import date
from typing import Iterator, Tuple, Optional, NamedTuple
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement

__author__ = "Florian Leitner"
__version__ = "1"

# CONFIGURATION

ABSTRACTS_PATH = "fulltext"
ABSTRACTS_ENCODING = "UTF-8"

METADATA_PATH = "metadata"
METADATA_ENCODING = "UTF-8"

ACCESS_REF = "restrictedAccess"
LICENSE_PATH = "licence"
LICENSE_ENCODING = "UTF-8"
LICENSE_REF = "CC-BY-NC-4.0"
LICENSE_FILENAME = "CC-BY-NC"
LICENSE_TEXT = """
Attribution-NonCommercial 4.0 International

=======================================================================

Creative Commons Corporation ("Creative Commons") is not a law firm and
does not provide legal services or legal advice. Distribution of
Creative Commons public licenses does not create a lawyer-client or
other relationship. Creative Commons makes its licenses and related
information available on an "as-is" basis. Creative Commons gives no
warranties regarding its licenses, any material licensed under their
terms and conditions, or any related information. Creative Commons
disclaims all liability for damages resulting from their use to the
fullest extent possible.

Using Creative Commons Public Licenses

Creative Commons public licenses provide a standard set of terms and
conditions that creators and other rights holders may use to share
original works of authorship and other material subject to copyright
and certain other rights specified in the public license below. The
following considerations are for informational purposes only, are not
exhaustive, and do not form part of our licenses.

     Considerations for licensors: Our public licenses are
     intended for use by those authorized to give the public
     permission to use material in ways otherwise restricted by
     copyright and certain other rights. Our licenses are
     irrevocable. Licensors should read and understand the terms
     and conditions of the license they choose before applying it.
     Licensors should also secure all rights necessary before
     applying our licenses so that the public can reuse the
     material as expected. Licensors should clearly mark any
     material not subject to the license. This includes other CC-
     licensed material, or material used under an exception or
     limitation to copyright. More considerations for licensors:
     wiki.creativecommons.org/Considerations_for_licensors

     Considerations for the public: By using one of our public
     licenses, a licensor grants the public permission to use the
     licensed material under specified terms and conditions. If
     the licensor's permission is not necessary for any reason--for
     example, because of any applicable exception or limitation to
     copyright--then that use is not regulated by the license. Our
     licenses grant only permissions under copyright and certain
     other rights that a licensor has authority to grant. Use of
     the licensed material may still be restricted for other
     reasons, including because others have copyright or other
     rights in the material. A licensor may make special requests,
     such as asking that all changes be marked or described.
     Although not required by our licenses, you are encouraged to
     respect those requests where reasonable. More_considerations
     for the public: 
     wiki.creativecommons.org/Considerations_for_licensees

=======================================================================

Creative Commons Attribution-NonCommercial 4.0 International Public
License

By exercising the Licensed Rights (defined below), You accept and agree
to be bound by the terms and conditions of this Creative Commons
Attribution-NonCommercial 4.0 International Public License ("Public
License"). To the extent this Public License may be interpreted as a
contract, You are granted the Licensed Rights in consideration of Your
acceptance of these terms and conditions, and the Licensor grants You
such rights in consideration of benefits the Licensor receives from
making the Licensed Material available under these terms and
conditions.


Section 1 -- Definitions.

  a. Adapted Material means material subject to Copyright and Similar
     Rights that is derived from or based upon the Licensed Material
     and in which the Licensed Material is translated, altered,
     arranged, transformed, or otherwise modified in a manner requiring
     permission under the Copyright and Similar Rights held by the
     Licensor. For purposes of this Public License, where the Licensed
     Material is a musical work, performance, or sound recording,
     Adapted Material is always produced where the Licensed Material is
     synched in timed relation with a moving image.

  b. Adapter's License means the license You apply to Your Copyright
     and Similar Rights in Your contributions to Adapted Material in
     accordance with the terms and conditions of this Public License.

  c. Copyright and Similar Rights means copyright and/or similar rights
     closely related to copyright including, without limitation,
     performance, broadcast, sound recording, and Sui Generis Database
     Rights, without regard to how the rights are labeled or
     categorized. For purposes of this Public License, the rights
     specified in Section 2(b)(1)-(2) are not Copyright and Similar
     Rights.
  d. Effective Technological Measures means those measures that, in the
     absence of proper authority, may not be circumvented under laws
     fulfilling obligations under Article 11 of the WIPO Copyright
     Treaty adopted on December 20, 1996, and/or similar international
     agreements.

  e. Exceptions and Limitations means fair use, fair dealing, and/or
     any other exception or limitation to Copyright and Similar Rights
     that applies to Your use of the Licensed Material.

  f. Licensed Material means the artistic or literary work, database,
     or other material to which the Licensor applied this Public
     License.

  g. Licensed Rights means the rights granted to You subject to the
     terms and conditions of this Public License, which are limited to
     all Copyright and Similar Rights that apply to Your use of the
     Licensed Material and that the Licensor has authority to license.

  h. Licensor means the individual(s) or entity(ies) granting rights
     under this Public License.

  i. NonCommercial means not primarily intended for or directed towards
     commercial advantage or monetary compensation. For purposes of
     this Public License, the exchange of the Licensed Material for
     other material subject to Copyright and Similar Rights by digital
     file-sharing or similar means is NonCommercial provided there is
     no payment of monetary compensation in connection with the
     exchange.

  j. Share means to provide material to the public by any means or
     process that requires permission under the Licensed Rights, such
     as reproduction, public display, public performance, distribution,
     dissemination, communication, or importation, and to make material
     available to the public including in ways that members of the
     public may access the material from a place and at a time
     individually chosen by them.

  k. Sui Generis Database Rights means rights other than copyright
     resulting from Directive 96/9/EC of the European Parliament and of
     the Council of 11 March 1996 on the legal protection of databases,
     as amended and/or succeeded, as well as other essentially
     equivalent rights anywhere in the world.

  l. You means the individual or entity exercising the Licensed Rights
     under this Public License. Your has a corresponding meaning.


Section 2 -- Scope.

  a. License grant.

       1. Subject to the terms and conditions of this Public License,
          the Licensor hereby grants You a worldwide, royalty-free,
          non-sublicensable, non-exclusive, irrevocable license to
          exercise the Licensed Rights in the Licensed Material to:

            a. reproduce and Share the Licensed Material, in whole or
               in part, for NonCommercial purposes only; and

            b. produce, reproduce, and Share Adapted Material for
               NonCommercial purposes only.

       2. Exceptions and Limitations. For the avoidance of doubt, where
          Exceptions and Limitations apply to Your use, this Public
          License does not apply, and You do not need to comply with
          its terms and conditions.

       3. Term. The term of this Public License is specified in Section
          6(a).

       4. Media and formats; technical modifications allowed. The
          Licensor authorizes You to exercise the Licensed Rights in
          all media and formats whether now known or hereafter created,
          and to make technical modifications necessary to do so. The
          Licensor waives and/or agrees not to assert any right or
          authority to forbid You from making technical modifications
          necessary to exercise the Licensed Rights, including
          technical modifications necessary to circumvent Effective
          Technological Measures. For purposes of this Public License,
          simply making modifications authorized by this Section 2(a)
          (4) never produces Adapted Material.

       5. Downstream recipients.

            a. Offer from the Licensor -- Licensed Material. Every
               recipient of the Licensed Material automatically
               receives an offer from the Licensor to exercise the
               Licensed Rights under the terms and conditions of this
               Public License.

            b. No downstream restrictions. You may not offer or impose
               any additional or different terms or conditions on, or
               apply any Effective Technological Measures to, the
               Licensed Material if doing so restricts exercise of the
               Licensed Rights by any recipient of the Licensed
               Material.

       6. No endorsement. Nothing in this Public License constitutes or
          may be construed as permission to assert or imply that You
          are, or that Your use of the Licensed Material is, connected
          with, or sponsored, endorsed, or granted official status by,
          the Licensor or others designated to receive attribution as
          provided in Section 3(a)(1)(A)(i).

  b. Other rights.

       1. Moral rights, such as the right of integrity, are not
          licensed under this Public License, nor are publicity,
          privacy, and/or other similar personality rights; however, to
          the extent possible, the Licensor waives and/or agrees not to
          assert any such rights held by the Licensor to the limited
          extent necessary to allow You to exercise the Licensed
          Rights, but not otherwise.

       2. Patent and trademark rights are not licensed under this
          Public License.

       3. To the extent possible, the Licensor waives any right to
          collect royalties from You for the exercise of the Licensed
          Rights, whether directly or through a collecting society
          under any voluntary or waivable statutory or compulsory
          licensing scheme. In all other cases the Licensor expressly
          reserves any right to collect such royalties, including when
          the Licensed Material is used other than for NonCommercial
          purposes.


Section 3 -- License Conditions.

Your exercise of the Licensed Rights is expressly made subject to the
following conditions.

  a. Attribution.

       1. If You Share the Licensed Material (including in modified
          form), You must:

            a. retain the following if it is supplied by the Licensor
               with the Licensed Material:

                 i. identification of the creator(s) of the Licensed
                    Material and any others designated to receive
                    attribution, in any reasonable manner requested by
                    the Licensor (including by pseudonym if
                    designated);

                ii. a copyright notice;

               iii. a notice that refers to this Public License;

                iv. a notice that refers to the disclaimer of
                    warranties;

                 v. a URI or hyperlink to the Licensed Material to the
                    extent reasonably practicable;

            b. indicate if You modified the Licensed Material and
               retain an indication of any previous modifications; and

            c. indicate the Licensed Material is licensed under this
               Public License, and include the text of, or the URI or
               hyperlink to, this Public License.

       2. You may satisfy the conditions in Section 3(a)(1) in any
          reasonable manner based on the medium, means, and context in
          which You Share the Licensed Material. For example, it may be
          reasonable to satisfy the conditions by providing a URI or
          hyperlink to a resource that includes the required
          information.

       3. If requested by the Licensor, You must remove any of the
          information required by Section 3(a)(1)(A) to the extent
          reasonably practicable.

       4. If You Share Adapted Material You produce, the Adapter's
          License You apply must not prevent recipients of the Adapted
          Material from complying with this Public License.


Section 4 -- Sui Generis Database Rights.

Where the Licensed Rights include Sui Generis Database Rights that
apply to Your use of the Licensed Material:

  a. for the avoidance of doubt, Section 2(a)(1) grants You the right
     to extract, reuse, reproduce, and Share all or a substantial
     portion of the contents of the database for NonCommercial purposes
     only;

  b. if You include all or a substantial portion of the database
     contents in a database in which You have Sui Generis Database
     Rights, then the database in which You have Sui Generis Database
     Rights (but not its individual contents) is Adapted Material; and

  c. You must comply with the conditions in Section 3(a) if You Share
     all or a substantial portion of the contents of the database.

For the avoidance of doubt, this Section 4 supplements and does not
replace Your obligations under this Public License where the Licensed
Rights include other Copyright and Similar Rights.


Section 5 -- Disclaimer of Warranties and Limitation of Liability.

  a. UNLESS OTHERWISE SEPARATELY UNDERTAKEN BY THE LICENSOR, TO THE
     EXTENT POSSIBLE, THE LICENSOR OFFERS THE LICENSED MATERIAL AS-IS
     AND AS-AVAILABLE, AND MAKES NO REPRESENTATIONS OR WARRANTIES OF
     ANY KIND CONCERNING THE LICENSED MATERIAL, WHETHER EXPRESS,
     IMPLIED, STATUTORY, OR OTHER. THIS INCLUDES, WITHOUT LIMITATION,
     WARRANTIES OF TITLE, MERCHANTABILITY, FITNESS FOR A PARTICULAR
     PURPOSE, NON-INFRINGEMENT, ABSENCE OF LATENT OR OTHER DEFECTS,
     ACCURACY, OR THE PRESENCE OR ABSENCE OF ERRORS, WHETHER OR NOT
     KNOWN OR DISCOVERABLE. WHERE DISCLAIMERS OF WARRANTIES ARE NOT
     ALLOWED IN FULL OR IN PART, THIS DISCLAIMER MAY NOT APPLY TO YOU.

  b. TO THE EXTENT POSSIBLE, IN NO EVENT WILL THE LICENSOR BE LIABLE
     TO YOU ON ANY LEGAL THEORY (INCLUDING, WITHOUT LIMITATION,
     NEGLIGENCE) OR OTHERWISE FOR ANY DIRECT, SPECIAL, INDIRECT,
     INCIDENTAL, CONSEQUENTIAL, PUNITIVE, EXEMPLARY, OR OTHER LOSSES,
     COSTS, EXPENSES, OR DAMAGES ARISING OUT OF THIS PUBLIC LICENSE OR
     USE OF THE LICENSED MATERIAL, EVEN IF THE LICENSOR HAS BEEN
     ADVISED OF THE POSSIBILITY OF SUCH LOSSES, COSTS, EXPENSES, OR
     DAMAGES. WHERE A LIMITATION OF LIABILITY IS NOT ALLOWED IN FULL OR
     IN PART, THIS LIMITATION MAY NOT APPLY TO YOU.

  c. The disclaimer of warranties and limitation of liability provided
     above shall be interpreted in a manner that, to the extent
     possible, most closely approximates an absolute disclaimer and
     waiver of all liability.


Section 6 -- Term and Termination.

  a. This Public License applies for the term of the Copyright and
     Similar Rights licensed here. However, if You fail to comply with
     this Public License, then Your rights under this Public License
     terminate automatically.

  b. Where Your right to use the Licensed Material has terminated under
     Section 6(a), it reinstates:

       1. automatically as of the date the violation is cured, provided
          it is cured within 30 days of Your discovery of the
          violation; or

       2. upon express reinstatement by the Licensor.

     For the avoidance of doubt, this Section 6(b) does not affect any
     right the Licensor may have to seek remedies for Your violations
     of this Public License.

  c. For the avoidance of doubt, the Licensor may also offer the
     Licensed Material under separate terms or conditions or stop
     distributing the Licensed Material at any time; however, doing so
     will not terminate this Public License.

  d. Sections 1, 5, 6, 7, and 8 survive termination of this Public
     License.


Section 7 -- Other Terms and Conditions.

  a. The Licensor shall not be bound by any additional or different
     terms or conditions communicated by You unless expressly agreed.

  b. Any arrangements, understandings, or agreements regarding the
     Licensed Material not stated herein are separate from and
     independent of the terms and conditions of this Public License.


Section 8 -- Interpretation.

  a. For the avoidance of doubt, this Public License does not, and
     shall not be interpreted to, reduce, limit, restrict, or impose
     conditions on any use of the Licensed Material that could lawfully
     be made without permission under this Public License.

  b. To the extent possible, if any provision of this Public License is
     deemed unenforceable, it shall be automatically reformed to the
     minimum extent necessary to make it enforceable. If the provision
     cannot be reformed, it shall be severed from this Public License
     without affecting the enforceability of the remaining terms and
     conditions.

  c. No term or condition of this Public License will be waived and no
     failure to comply consented to unless expressly agreed to by the
     Licensor.

  d. Nothing in this Public License constitutes or may be interpreted
     as a limitation upon, or waiver of, any privileges and immunities
     that apply to the Licensor or You, including from the legal
     processes of any jurisdiction or authority.

=======================================================================

Creative Commons is not a party to its public
licenses. Notwithstanding, Creative Commons may elect to apply one of
its public licenses to material it publishes and in those instances
will be considered the "Licensor." The text of the Creative Commons
public licenses is dedicated to the public domain under the CC0 Public
Domain Dedication. Except for the limited purpose of indicating that
material is shared under a Creative Commons public license or as
otherwise permitted by the Creative Commons policies published at
creativecommons.org/policies, Creative Commons does not authorize the
use of the trademark "Creative Commons" or any other trademark or logo
of Creative Commons without its prior written consent including,
without limitation, in connection with any unauthorized modifications
to any of its public licenses or any other arrangements,
understandings, or agreements concerning use of licensed material. For
the avoidance of doubt, this paragraph does not form part of the
public licenses.

Creative Commons may be contacted at creativecommons.org.
""".strip()

OMTD_SHARE_XML_NAMESPACE = "http://www.meta-share.org/OMTD-SHARE_XMLSchema"

XML_NAMESPACE_SETUP = {
    "xsi:schemaLocation":
        "http://www.meta-share.org/OMTD-SHARE_XMLSchema "
        "http://www.meta-share.org/OMTD-SHARE_XMLSchema/v302/OMTD-SHARE-Publications.xsd",
    "xmlns": OMTD_SHARE_XML_NAMESPACE,
    "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
}

MONTHS = {"ene": 1, "eme": 1, "feb": 2, "mar": 3, "abr": 4,
          "may": 5, "jun": 6, "jul": 7, "ago": 8,
          "sep": 9, "set": 9, "oct": 10, "nov": 11, "no": 11, "dic": 12}

ID_LANG_SEP = "_"

# TYPES

ETreeIterator = Iterator[Tuple[str, Element]]


class Arguments(NamedTuple):
    ibecs_file_path: str
    output_dir_path: str
    license_text: str


class Encodings(NamedTuple):
    abstracts: str
    metadata: str
    license: str


class Paths(NamedTuple):
    abstracts: str
    metadata: str
    license: str


class IbecsToOmtdParserException(Exception):
    pass


class OutputDirStructureCreationFailure(IbecsToOmtdParserException):
    pass


class InputFileOpeningError(IbecsToOmtdParserException):
    pass


class CorpusWritingError(IbecsToOmtdParserException):
    pass


class MissingLicenseException(IbecsToOmtdParserException):
    pass


class DateParsingException(IbecsToOmtdParserException):
    pass


# CLASSES

class CorpusDataWriter:
    def __init__(self, encoding: str, path: str, suffix: str):
        self.path = path
        self.encoding = encoding
        self.suffix = suffix

    def write(self, file_id: str, lang: str, text: str, md5_digest: bool = False) -> str:
        file_name = f"{file_id}{ID_LANG_SEP}{lang}{self.suffix}"
        path = os.path.join(self.path, file_name)
        logging.debug(path)

        try:
            with open(path, mode='w', encoding=self.encoding) as handle:
                # noinspection PyTypeChecker
                print(text, file=handle)
        except Exception as e:
            error_message = f"could not write {file_name} to {self.path}: {e}"
            raise CorpusWritingError(error_message) from e

        if md5_digest:
            try:
                md5 = hashlib.md5()
                md5.update(text.encode(self.encoding))
                md5.update(b'\n')
                return md5.hexdigest()
            except Exception as e:
                error_message = f"could not hash {file_name} at {self.path}: {e}"
                raise CorpusWritingError(error_message) from e

        return "NAN"

    def write_file_without_language_infix(self, file_id: str, text: str) -> None:
        file_name = f"{file_id}{self.suffix}"
        path = os.path.join(self.path, file_name)
        logging.debug(path)

        try:
            with open(path, mode='w', encoding=self.encoding) as handle:
                # noinspection PyTypeChecker
                print(text, file=handle)
        except Exception as e:
            error_message = f"could not write {file_name} to {self.path}: {e}"
            raise CorpusWritingError(error_message) from e


class IbecsDocument:
    handler: Optional[CorpusDataWriter] = None
    counter: int = 0

    def __init__(self):
        self.ibecs_id = None
        self._abstract_id = None
        self.data = {}
        self.localized_data = {}

    @property
    def abstract_id(self):
        if not self._abstract_id:
            abs_id = self.ibecs_id if self.ibecs_id else str(IbecsDocument.counter + 1)
            self._abstract_id = abs_id.strip().replace(' ', '_')

        return self._abstract_id

    def handle_field(self, name: str, value: str) -> None:
        if name == "id":
            if not self.ibecs_id:
                self.ibecs_id = value
            else:
                logging.error("multiple IDs for document %s: %s", self.ibecs_id, value)

        elif name.startswith("ab_"):
            if value != "No disponible":
                lang = self._make_lang(name)
                self._write_abstract(lang, value)

        elif name.startswith("ti_"):
            lang = self._make_lang(name)
            self._save_localized_data("ti", lang, value)

        else:
            self._save_data(name, value)

    @staticmethod
    def _make_lang(name):
        return name[3:]

    def _write_abstract(self, lang: str, text: str) -> None:
        if not lang:
            logging.warning("no language found for %s; defaulting to 'es'", self.ibecs_id)
            lang = "es"

        if text != "No disponible":
            digest = IbecsDocument.handler.write(self.abstract_id, lang, text, md5_digest=True)
            self._save_data("lang", lang)
            self._save_localized_data("hashkey", lang, digest)

    def serialize_metadata(self, lang: str) -> str:
        today = str(date.today()) + "Z"
        root = Element("documentMetadataRecord", attrib=XML_NAMESPACE_SETUP)
        add_leaf = IbecsDocument._add_xml_leaf

        # header & document
        header = SubElement(root, "metadataHeaderInfo")
        document = SubElement(root, "document")
        lang_suffix = ID_LANG_SEP + lang if lang else ""
        add_leaf(header, "metadataRecordIdentifier", self.abstract_id + lang_suffix,
                 metadataIdentifierSchemeName="other")
        add_leaf(header, "metadataCreationDate", today)
        add_leaf(header, "metadataLastDateUpdated", today)

        # publication
        publication = SubElement(document, "publication")
        add_leaf(publication, "documentType",
                 "withAbstractOnly" if lang else "bibliographicRecordOnly")
        add_leaf(publication, "publicationType", "journalArticle")

        # identifiers
        identifiers = SubElement(publication, "identifiers")
        add_leaf(
            identifiers, "publicationIdentifier", self.abstract_id,
            publicationIdentifierSchemeName="other",
            schemeURI="http://api.openaire.eu/vocabularies/dnet:pid_types/UNKNOWN")

        # titles
        titles = SubElement(publication, "titles")

        for locale in self.localized_data:
            if "ti" in self.localized_data[locale]:
                for title in self.localized_data[locale]["ti"]:
                    if not lang or locale == lang:
                        add_leaf(titles, "title", title, lang=locale)
                    else:
                        add_leaf(titles, "title", title, lang=locale, titleType="translatedTitle")

        # authors
        if "au" in self.data:
            authors = SubElement(publication, "authors")

            for full_name in self.data["au"]:
                if "," in full_name:
                    surname, given_name = full_name.split(",", 1)
                    author = SubElement(authors, "author")
                    add_leaf(author, "surname", surname.strip())
                    add_leaf(author, "givenName", given_name.strip())

        # publication date
        if "dp" in self.data:
            pub_date = SubElement(publication, "publicationDate")
            date_string = self.data['dp'][0]

            try:
                month, year = date_string.split(" ", 1)
            except ValueError:
                if looks_like_a_year(date_string):
                    month, year = "ene.", date_string  # Fallback to first month of year
                else:
                    try:
                        month, year = date_string.split(".", 1)
                    except ValueError:
                        msg = f"could not split '{date_string}' of {self.abstract_id}"
                        raise DateParsingException(msg)

            add_leaf(pub_date, "day", "1")
            add_leaf(pub_date, "month", str(month_name_to_int(month.strip())))
            add_leaf(pub_date, "year", year.strip())

        # journal [title]
        if "is" in self.data or "ta" in self.data:
            journal = SubElement(publication, "journal")
            journal_titles = SubElement(journal, "journalTitles")

            if "is" in self.data:
                journal_identifiers = SubElement(journal, "identifiers")
                add_leaf(
                    journal_identifiers, "journalIdentifier", self.data["is"][0],
                    journalIdentifierSchemeName='ISSN')

            for jt in self.data["ta"]:
                add_leaf(journal_titles, "journalTitle", jt, lang='es')

        # distributions
        distributions = SubElement(publication, "distributions")
        dd_info = SubElement(distributions, "documentDistributionInfo")

        if "ur" in self.data:
            for url in self.data["ur"]:
                add_leaf(dd_info, "distributionLocation", url)
        else:
            add_leaf(dd_info, "distributionLocation", "http://ibecs.isciii.es")

        if lang in self.localized_data and "hashkey" in self.localized_data[lang]:
            add_leaf(dd_info, "hashkey", self.localized_data[lang]["hashkey"][0])
        else:
            add_leaf(dd_info, "hashkey", "NAN")

        # rights/licensing
        rights = SubElement(publication, "rightsInfo")
        licenses = SubElement(rights, "licenceInfos")
        license_data = SubElement(licenses, "licenceInfo")
        add_leaf(license_data, "licence", LICENSE_REF)
        add_leaf(rights, "rightsStatement", ACCESS_REF)

        # languages
        if lang:
            languages = SubElement(publication, "documentLanguages")
            add_leaf(languages, "documentLanguage", lang)

        # keywords
        if "limit" in self.data or "clinical_aspect" in self.data:
            keywords = SubElement(publication, "keywords")

            if "limit" in self.data:
                for kw in self.data["limit"]:
                    add_leaf(keywords, "keyword", kw)

            if "clinical_aspect" in self.data:
                for kw in self.data["clinical_aspect"]:
                    add_leaf(keywords, "keyword", kw)

            return IbecsDocument._prettyxml(root)

    @staticmethod
    def _add_xml_leaf(parent: Element, name: str, value: str, **attrs: str) -> SubElement:
        sub = SubElement(parent, name, attrs)
        sub.text = value
        return sub

    @staticmethod
    def _prettyxml(root: Element) -> str:
        compact = et.tostring(root, "unicode")
        expat_doc = minidom.parseString(compact)
        return expat_doc.toprettyxml(indent="  ")

    def _save_data(self, name, value) -> None:
        if name in self.data:
            self.data[name].append(value)
        else:
            self.data[name] = [value]

    def _save_localized_data(self, name, lang, value) -> None:
        if lang not in self.localized_data:
            self.localized_data[lang] = {}

        data = self.localized_data[lang]

        if name in data:
            data[name].append(value)
        else:
            data[name] = [value]


# PROGRAM

def run(arguments: Arguments,
        encodings: Encodings,
        directories: Paths,
        overwrite_corpus: bool = False) -> int:
    input_stream = open_xml_stream(arguments.ibecs_file_path)
    paths = create_output_directory_structure(
        directories, arguments.output_dir_path, overwrite_corpus)
    write_license_text(paths.license)
    return convert(input_stream, encodings, paths)


def open_xml_stream(infile: str) -> ETreeIterator:
    try:
        return et.iterparse(infile)
    except Exception as e:
        error_message = f"could not open the IBECS XML input file: {e}"
        raise InputFileOpeningError(error_message) from e


def create_output_directory_structure(
        directories: Paths,
        output_dir: str,
        overwrite_corpus: bool) -> Paths:
    norm_output_dir = os.path.normpath(output_dir)
    # noinspection PyArgumentList
    paths = Paths(
        os.path.join(norm_output_dir, directories.abstracts),
        os.path.join(norm_output_dir, directories.metadata),
        os.path.join(norm_output_dir, directories.license))
    logging.debug("normalized output dir. path: %s", norm_output_dir)

    try:
        os.makedirs(output_dir, mode=0o770, exist_ok=True)

        if overwrite_corpus:
            for path in paths:
                if os.path.isdir(path):
                    shutil.rmtree(path)

        # noinspection PyProtectedMember
        for name, path in paths._asdict().items():
            create_subdir(name, path, overwrite_corpus)
    except Exception as e:
        error_message = f"could not create the output directory structure: {e}"
        raise OutputDirStructureCreationFailure(error_message) from e

    return paths


def create_subdir(name, path, overwrite_corpus):
    os.makedirs(path, mode=0o770, exist_ok=overwrite_corpus)
    logging.debug("created %s directory: %s", name, path)


def write_license_text(license_path):
    file_path = os.path.join(license_path, LICENSE_FILENAME)

    try:
        with open(file_path, 'w') as handle:
            print(LICENSE_TEXT, file=handle)
    except Exception as e:
        msg = f"failed to write license to {file_path}: {e}"
        raise MissingLicenseException(msg) from e


def convert(ibecs_xml_stream: ETreeIterator,
            encodings: Encodings,
            paths: Paths) -> int:
    logging.info("beginning conversion")
    IbecsDocument.handler = CorpusDataWriter(encodings.abstracts, paths.abstracts, ".txt")
    metadata_handler = CorpusDataWriter(encodings.metadata, paths.metadata, ".xml")
    doc = IbecsDocument()

    for _, element in ibecs_xml_stream:
        if element.tag == 'doc':
            if not doc.abstract_id:
                logging.error("no abstract ID created from %s", element)
            elif "lang" not in doc.data:
                # only metadata, no abstract
                metadata_text = doc.serialize_metadata("")
                metadata_handler.write_file_without_language_infix(doc.abstract_id, metadata_text)
                IbecsDocument.counter += 1
            else:
                for lang in doc.data["lang"]:
                    metadata_text = doc.serialize_metadata(lang)
                    metadata_handler.write(doc.abstract_id, lang, metadata_text)

                IbecsDocument.counter += 1

            doc = IbecsDocument()

        elif element.tag == 'field':
            name = element.get("name", "")
            doc.handle_field(name.lower().strip(), element.text.strip())

    return IbecsDocument.counter


def month_name_to_int(name: str) -> int:
    try:
        return MONTHS[name.lower()[:3]]
    except KeyError as e:
        return 1  # Fallback to the first month


def looks_like_a_year(s: str) -> bool:
    return str.isnumeric(s) and 1900 < int(s) < 2100


def configure_logging(args):
    log_adjust = max(min(args.quiet - args.verbose, 2), -2) * 10
    logging.basicConfig(filename=args.logfile, level=logging.WARNING + log_adjust,
                        format='%(levelname)-8s %(asctime)-15s %(funcName)s: %(message)s')
    logging.info('INFO  verbosity activated')
    logging.debug('DEBUG verbosity activated')


def main():
    parser = ArgumentParser(
        usage='%(prog)s [options] IBECS_FILE OMTD_DIR',
        description=__doc__, epilog=None,
        prog=os.path.basename(sys.argv[0])
    )

    parser.add_argument('infile', metavar='IBECS',
                        help='IBECS input XML file')
    parser.add_argument('output_dir', metavar='OMTD_DIR',
                        help='output directory [STDOUT]')
    parser.add_argument('-f', '--force', action='store_true',
                        help='overwrite the corpus if it exists')
    parser.add_argument('--encoding', metavar='ENCODING', default=ABSTRACTS_ENCODING,
                        help='text encoding for abstracts [%(default)s]')
    parser.add_argument('--abstracts', metavar='ABS_PATH', default=ABSTRACTS_PATH,
                        help='rel. path for abstracts [%(default)s]')
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--verbose', '-v', action='count', default=0,
                        help='increase log level [WARN]')
    parser.add_argument('--quiet', '-q', action='count', default=0,
                        help='decrease log level [WARN]')
    parser.add_argument('--logfile', metavar='FILE',
                        help='log to file instead of <STDERR>')

    args = parser.parse_args()
    configure_logging(args)

    # noinspection PyArgumentList
    encodings = Encodings(args.encoding, METADATA_ENCODING, LICENSE_ENCODING)
    # noinspection PyArgumentList
    directories = Paths(args.abstracts, METADATA_PATH, LICENSE_PATH)

    logging.info("input file path: %s", args.infile)
    logging.info("corpus output dir. path: %s", args.output_dir)
    logging.info("abstract text encoding: %s", encodings.abstracts)
    logging.info("abstracts dir. path: %s", directories.abstracts)

    try:
        license_text = LICENSE_TEXT

        if not license_text:
            raise MissingLicenseException("license is empty/undefined")

        # noinspection PyArgumentList
        arguments = Arguments(args.infile, args.output_dir, license_text)
        n_docs = run(arguments, encodings, directories, overwrite_corpus=args.force)
        logging.info("converted %d abstracts", n_docs)
    except IbecsToOmtdParserException as e:
        logging.error(e)
        logging.critical("aborting conversion; job failed")
        sys.exit(1)
    except Exception as unk:
        logging.exception("unexpected error: %s", unk)
        logging.critical("aborting conversion; job failed")
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()

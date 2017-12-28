import argparse
import collections
import logging
import os

from lxml import etree

# http://www.anc.org/penn.html
POS_TAGS = {
    "noun": ["NN"],
    "adjective": ["JJ"],
}

logger = logging.getLogger()

def main(dir, pos_tags=None, output_filename=""):
    if not pos_tags:
        logger.error("part of speech tag improperly configured")
        return
    if not output_filename:
        logger.error("Output filename needs to be specified")
        return

    xpath_for_pos_tag = {t: ".//{*}f[@name='msd'][@value='%s']" % t for t in pos_tags}
    words = collections.Counter()
    for root, dirs, files in os.walk(dir):
        for filename in files:
            if not filename.endswith("-penn.xml"):
                continue
            print(os.path.join(root, filename))
            for event, ele in etree.iterparse(os.path.join(root,filename), events=("end",), tag="{*}fs"):
                for pos_tag, xpath in xpath_for_pos_tag.items():
                    if ele.find(xpath) is None:
                        continue
                    for e in ele:
                        v = e.attrib.get("value", "")
                        if e.attrib.get("name", "") == "base" and len(v) >= 3 and v.isalpha():
                            words[v.lower()] += 1
                ele.clear()
    with open(output_filename, "w") as f:
        for w, c in words.most_common():
            f.write("%s %s\n" % (w, c))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Creates word lists from the given MASC data. Data can be found at http://www.anc.org/data/masc/downloads/data-download/")
    parser.add_argument("-d", "--dir", default=".", help="The directory ")
    parser.add_argument("-t", "--type", required=True, choices=["adjective", "noun"], help="The type (part of speech) to extract and use to create a word list")
    parser.add_argument("-o", "--output", required=True, help="Where to save word list")
    args = parser.parse_args()
    pos_tags = POS_TAGS.get(args.type, None)
    main(dir=args.dir, pos_tags=pos_tags, output_filename=args.output)

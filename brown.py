import argparse
import collections
import logging
import os

# http://www.anc.org/penn.html
POS_TAGS = {
    "noun": ["nn"],
    "adjective": ["jj"],
}

logger = logging.getLogger()

def main(dir, pos_tags=None, output_filename=""):
    if not pos_tags:
        logger.error("part of speech tag improperly configured")
        return
    if not output_filename:
        logger.error("Output filename needs to be specified")
        return

    words = collections.Counter()
    for root, dirs, files in os.walk(dir):
        for filename in files:
            if not filename.startswith("c"):
                continue
            with open(os.path.join(root, filename)) as f:
                data = f.read()
                for tok in data.split():
                    try:
                        word, tag = tok.split("/", 2)
                        if len(word) < 3:
                            continue
                        if not word.isalpha():
                            continue
                        if tag not in pos_tags:
                            continue
                        words[word.lower()] += 1
                    except ValueError:
                        pass
    with open(output_filename, "w") as f:
        for w, c in words.most_common():
            f.write("%s %s\n" % (w, c))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Creates word lists from the given brown data. Data can be found at https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/brown.zip")
    parser.add_argument("-d", "--dir", default=".", help="The directory ")
    parser.add_argument("-t", "--type", required=True, choices=["adjective", "noun"], help="The type (part of speech) to extract and use to create a word list")
    parser.add_argument("-o", "--output", required=True, help="Where to save word list")
    args = parser.parse_args()
    pos_tags = POS_TAGS.get(args.type, None)
    main(dir=args.dir, pos_tags=pos_tags, output_filename=args.output)

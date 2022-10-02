import os
import re
from helpers import paper_path, header_file

default_header_file = header_file
default_abstract_file = os.path.join(paper_path, 'abstract.tex')
target_abstract_file = os.path.join(paper_path, 'ci-output/abstract.txt')


def sanitize(abstract, replace_defs):
    # replace abstract environment if existing
    abstract = abstract.replace("\\begin{abstract}", "")
    abstract = abstract.replace("\\end{abstract}", "")
    
    # replace according to header definitions
    for key, text in replace_defs.items():
        abstract = abstract.replace(key,text)
    
    # replace math
    abstract = abstract.replace('$', '')
    
    # remove tilde (non-breaking whitespace)
    abstract = abstract.replace("~", " ")
    
    # replace %, ~
    abstract = abstract.replace("\\%", "<<PERCENT>>")   # to disambiguate with comments
    abstract = abstract.replace("\\textasciitilde ", "~")   # with space
    abstract = abstract.replace("\\textasciitilde", "~")    # without space
    
    # remove comments
    abstract = re.sub(r"\n%[^\n]*", r"", abstract, re.M)
    abstract = re.sub(r'%(.*)', '', abstract)
    abstract = abstract.replace("<<PERCENT>>", "%")   # re-introduce percent characters
    
    # remove hard wraps
    abstract = re.sub(r"\n[\n]+", "<<PARAGRAPH>>", abstract)
    abstract = abstract.replace("\n", " ")

    # add markdown for emphasis
    abstract = re.sub(r'\\emph{([0-9a-zA-Z-\' ]+)}', r"_\1_", abstract)
    
    # remove xspace
    abstract = abstract.replace("\\xspace ", " ")
    abstract = abstract.replace("\\xspace.", ".")
    abstract = abstract.replace("\\xspace,", ",")
    # (xspace results in warning in other cases)
    
    # strip whitespace
    abstract = abstract.strip()
    
    # re-introduce paragraphs
    abstract = abstract.replace("<<PARAGRAPH>>", "\n\n")
    
    # check if there are any non-replaced latex commands and add a warning if so
    if (abstract.find("\\") != -1):
        abstract = "\n** WARNING: NOT ALL COMMANDS COULD BE REPLACED, INSPECT MANUALLY **\n\n" + abstract
    
    return abstract + "\n"


# seeks the header file for simple replace definitions and extracts information
def extract_replace_defs(header):
    repl = {}
    pattern = re.compile(r'\\newcommand{(\\[a-zA-Z]+)}(?:\[0\])?{(\\emph{[0-9a-zA-Z\., -\\]+}|[0-9a-zA-Z\., -\\]+)(\\xspace)?}')
    for (cmd, text, xspace) in re.findall(pattern, header):
        repl[cmd] = text.strip() + xspace
    return repl


def create(abstract_file=default_abstract_file, header_file=default_header_file):
    with open(abstract_file, 'r', encoding='iso-8859-1') as f:
        abstract = f.read()
        
    with open(header_file, 'r', encoding='iso-8859-1') as f:
        header = f.read()

    replace_defs = extract_replace_defs(header)
    abstract = sanitize(abstract, replace_defs)

    with open(target_abstract_file, 'w', encoding='iso-8859-1') as f:
        f.write(abstract)


if __name__ == "__main__":
    create()

import os
import sys
import glob
import re
from helpers import paper_path, dir_path, get_short_filename, eprint, eprint_lines, get_list, header_file, ci_output_dir, iterate_nonheader_tex_lines

# forbidden text
forbidden_text_file = os.path.join(dir_path, 'forbidden_text_list.txt')
forbidden_text = get_list(forbidden_text_file)

# override
override_text = '% ignore forbidden'

# ignore hyphtenation
ignore_hyphtenation_file = os.path.join(dir_path, 'ignore_hyphtenation_list.txt')
ignore_hyphtenation_list = get_list(ignore_hyphtenation_file)

def get_forbidden(line):
    return [a for a in forbidden_text if a in line]

# - make everything lowercase
# - exclude labels, references, inputs, ...
def normalize_line(line):
    txt = re.sub(r"\\label{.*}", "", line)
    txt = re.sub(r"\\ref{.*}", "", txt)
    txt = re.sub(r"\\cref{.*}", "", txt)
    txt = re.sub(r"\\eqref{.*}", "", txt)
    txt = re.sub(r"\\input{.*}", "", txt)
    txt = re.sub(r"\\bibliographystyle{.*}", "", txt)
    txt = re.sub(r"\\cite{.*}", "", txt)
    return txt.lower()


def collect_hyphtenated(filename, linenum, linetext, hyphtenated_words):
    for w in re.findall(r"[a-zA-Z][a-zA-Z]+-[a-zA-Z][a-zA-Z]+", normalize_line(linetext)):
        if (w[-1] == "s"):
            w = w[:-1]  # normalize to singular form
        if not (w.lower() in ignore_hyphtenation_list):
            hyphtenated_words.append((filename, linenum, linetext, w.lower()))


def check_forbidden_text(hyphtenated_words):
    bad_lines = []
    for filename, i, line in iterate_nonheader_tex_lines():
        forbidden = get_forbidden(line)
        if len(forbidden) > 0 and override_text not in line:
            bad_lines.append((get_short_filename(filename), i, forbidden, line))
        collect_hyphtenated(filename, i, line, hyphtenated_words)    # remember all hypthenated words

    n_bad_lines = len(bad_lines)
    if n_bad_lines > 0:
        eprint('\n[ERROR]:', n_bad_lines, 'occurrences of forbidden text:')
        for file, i, forbidden, line in bad_lines:
            eprint('> {} (line {}) contains {}:'.format(file, i, ', '.join(forbidden)))
            eprint('> \t' + line.strip())
        eprint('[SOLUTION]:')
        solutions = [
            '1) Remove forbidden text from {}, most likely replacing it by a command from {}.'.format(
                get_short_filename(forbidden_text_file), get_short_filename(header_file)
            ),
            '2) Add the string "{}" to any line listed above to ignore errors for that line.'.format(override_text)
        ]
        eprint_lines(solutions, '> ')
        return False

    return True


def check_inconsistent_hyphtenation(hyphtenated_words):
    # generate inconsistent names
    forbidden_seq = []
    seen = {}
    for t in hyphtenated_words:
        w = t[3]
        if w in seen:
            continue
        seen[w] = 1
        parts = w.split("-")
        # forbidden: non-separated, space-separated, and plural forms
        forbidden = (" ".join(parts), "".join(parts), " ".join(parts) + "s", "".join(parts) + "s")
        forbidden_seq.append((t[0], t[1], t[2], w, forbidden))
        
    # search for occurrences
    for filename, i, line in iterate_nonheader_tex_lines():
        normalized_line = normalize_line(line)
        for t in forbidden_seq:
            for f in t[4]:
                if f in normalized_line:
                    eprint('\n[ERROR]: Inconsistent hypthenation of "{}" vs "{}"'.format(t[3], f))
                    eprint('> {} (line {}) contains "{}"'.format(t[0], t[1], t[3]))
                    eprint('> \t' + t[2].strip())
                    eprint('> {} (line {}) contains "{}"'.format(filename, i, f))
                    eprint('> \t' + line.strip())
                    eprint('[SOLUTION]:')
                    solutions = [
                        '1) Make hypthenation consistent by renaming either of the two occurrences.',
                        '2) Add the string "{}" to the file {}.'.format(t[3], get_short_filename(ignore_hyphtenation_file))
                    ]
                    eprint_lines(solutions, '> ')
                    return False
    return True

    
def check():
    hyphtenated_words = []
    ok_forbidden = check_forbidden_text(hyphtenated_words)
    ok_hyphtenation = check_inconsistent_hyphtenation(hyphtenated_words)
    return ok_forbidden and ok_hyphtenation


if __name__ == "__main__":
    ok = check()
    if not ok:
        sys.exit(1)

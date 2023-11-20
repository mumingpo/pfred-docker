from collections import Counter

def reynolds_filter(sequences: dict[str, str]):
    stretches = dict()
    reynolds_score = dict()
    reynolds_descriptors = dict()

    for key in sequences.keys():
        seq = sequences[key]
        
        # quintuple codons
        # FIXME: the variable names in the original script indicates that
        # they are looking for counts. However, the way it is implemented lets
        # it return 1 when found and 0 when not found.
        # original implementation is used here, while "correct" implementation is
        # provided below in comments for reference
        AAAAA_count = int("AAAAA" in seq)
        CCCCC_count = int("CCCCC" in seq)
        GGGGG_count = int("GGGGG" in seq)
        UUUUU_count = int("UUUUU" in seq)

        # "correct" implementation: find number of A with 4 succeeding As
        # AAAAA_count = len(re.findall('A(?=A{4})', seq))
        # CCCCC_count = len(re.findall('C(?=C{4})', seq))
        # GGGGG_count = len(re.findall('G(?=G{4})', seq))
        # UUUUU_count = len(re.findall('U(?=U{4})', seq))

        stretches[key] = (AAAAA_count, CCCCC_count, GGGGG_count, UUUUU_count)

        # num of G and C codons before the last 2 codons
        gc_count = 0
        gc_score = 0

        num_codons = Counter(seq[:-2].upper())

        gc_count = num_codons.get('C', 0) + num_codons.get('G', 0)
        gc_content = gc_count / 19 * 100

        if (gc_content >= 30 and gc_content <= 52):
            gc_score += 1

        # num of A and U codons in the first 5 codons
        num_codons = Counter(seq[:5].upper())
        au_count = num_codons.get('A', 0) + num_codons.get('U', 0)

        tm_score = 0

        u_p1 = int(seq[0].upper() == 'U')
        u_p17 = int(seq[16].upper() == 'U')
        a_p10 = int(seq[9].upper() == 'A')
        gc_p1 = int(seq[0].upper() in "CG")
        # FIXME: judging from the variable name,
        # shouldn't it include 'G' as well?
        gc_p7 = int(seq[6].upper() == 'C')

        seq_string = [
            gc_content,
            au_count,
            tm_score,
            u_p1,
            u_p17,
            a_p10,
            gc_p1,
            gc_p7,
        ]

        r_score = gc_score + tm_score + u_p1 + u_p17 + a_p10 + au_count - gc_p1 - gc_p7
        reynolds_score[key] = (r_score, gc_content, gc_score)
        reynolds_descriptors[key] = seq_string
    
    return reynolds_score, reynolds_descriptors, stretches
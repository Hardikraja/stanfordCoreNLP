from pycorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP('http://localhost:9000')


def resolve(corenlp_output):
    """ Transfer the word form of the antecedent to its associated pronominal anaphor(s) """
    for coref in corenlp_output['corefs']:
        mentions = corenlp_output['corefs'][coref]
        antecedent = mentions[0]  # the antecedent is the first mention in the coreference chain
        for j in range(1, len(mentions)):
            mention = mentions[j]
            if mention['type'] == 'PRONOMINAL':
                # get the attributes of the target mention in the corresponding sentence
                target_sentence = mention['sentNum']
                target_token = mention['startIndex'] - 1
                # transfer the antecedent's word form to the appropriate token in the sentence
                corenlp_output['sentences'][target_sentence - 1]['tokens'][target_token]['word'] = antecedent['text']


def print_resolved(corenlp_output):
    """ Print the "resolved" output """
    possessives = ['hers', 'his', 'their', 'theirs']
    for sentence in corenlp_output['sentences']:
        for token in sentence['tokens']:
            output_word = token['word']
            # check lemmas as well as tags for possessive pronouns in case of tagging errors
            if token['lemma'] in possessives or token['pos'] == 'PRP$':
                output_word += "'s"  # add the possessive morpheme
            output_word += token['after']
            print(output_word, end='')





text = "Tom and Jane are good friends. They are cool. He knows a lot of things and so does she. His car is red, but hers is blue. It is older than hers. The big cat ate his dinner."


output = nlp.annotate(text, properties= {'annotators':'dcoref','outputFormat':'json','ner.useSUTime':'false'})

resolve(output)

print('Original:', text)
print('Resolved: ', end='')
print_resolved(output)

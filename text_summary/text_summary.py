from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import math, string, re

from Postings import Postings

def create_frequency_table(content:str) -> dict:
    stopWords = set(stopwords.words("english"))
    tokens = word_tokenize(content)
    ps = PorterStemmer()

    freqTable = dict()
    for token in tokens:
        # apply stemming 
        token = ps.stem(token)
        # remove stopwords 
        if token in stopWords:
            continue
        if token in freqTable:
            freqTable[token] += 1
        else:
            freqTable[token] = 1

    return freqTable

# score each sentence -- weight frequency
def score_sentences(sentences:list, freqTable:dict) -> dict:
    sentenceScore = dict()
    for sentence in sentences:
        word_count_in_sentence = (len(word_tokenize(sentence)))
        for wordScore in freqTable:
            # term appears in sentence --> add score to the sentence 
            if wordScore in sentence.lower():
                if sentence[:10] in sentenceScore:
                    sentenceScore[sentence[:10]] += freqTable[wordScore]

                else:
                    sentenceScore[sentence[:10]] = freqTable[wordScore]


        # preventing longer sentences to get high score than shorter sentences 
        sentenceScore[sentence[:10]] = sentenceScore[sentence[:10]] // word_count_in_sentence

    
    return sentenceScore



# define the threshold -->one method is to use average score of the sentences as a threshold
def get_average_score(sentenceScores:dict()) -> float:
    sum = 0
    for entry in sentenceScores:
        sum += sentenceScores[entry]

    # Average value of a sentence from original text
    average = float(sum / len(sentenceScores))

    return average
    

def get_text_summary(sentences:list, sentenceScores:dict, threshold:float) -> str:
    sentence_count = 0
    summary = ''
    for sentence in sentences:
        if sentence[:10] in sentenceScores and sentenceScores[sentence[:10]] > (threshold):
            summary += " " + sentence
            sentence_count += 1

    return summary

# summarize text 
def text_summarization(content:str):
    summary = ''
     # split text into sentences 
    sentences = sent_tokenize(content)
    # content = re.sub(r'[^\w\s]', '', content)
    freqTable = create_frequency_table(content)
    sentenceScores = score_sentences(sentences,freqTable)
    averageScore = get_average_score(sentenceScores)

    summary = get_text_summary(sentences, sentenceScores, 1.5 * averageScore)
    return summary

    



if __name__ == "__main__": 

    content = "Call me Ishmael. Some years ago--never mind how long precisely--having\
    little or no money in my purse, and nothing particular to interest me on\
    shore, I thought I would sail about a little and see the watery part of\
    the world. It is a way I have of driving off the spleen and regulating\
    the circulation. Whenever I find myself growing grim about the mouth;\
    whenever it is a damp, drizzly November in my soul; whenever I find\
    myself involuntarily pausing before coffin warehouses, and bringing up\
    the rear of every funeral I meet; and especially whenever my hypos get\
    such an upper hand of me, that it requires a strong moral principle to\
    prevent me from deliberately stepping into the street, and methodically\
    knocking people's hats off--then, I account it high time to get to sea\
    as soon as I can. This is my substitute for pistol and ball. With a\
    philosophical flourish Cato throws himself upon his sword; I quietly\
    take to the ship. There is nothing surprising in this. If they but knew\
    it, almost all men in their degree, some time or other, cherish very\
    nearly the same feelings towards the ocean with me.\
    There now is your insular city of the Manhattoes, belted round by\
    wharves as Indian isles by coral reefs--commerce surrounds it with\
    her surf. Right and left, the streets take you waterward. Its extreme\
    downtown is the battery, where that noble mole is washed by waves, and\
    cooled by breezes, which a few hours previous were out of sight of land.\
    Look at the crowds of water-gazers there.\
    Circumambulate the city of a dreamy Sabbath afternoon. Go from Corlears\
    Hook to Coenties Slip, and from thence, by Whitehall, northward. What\
    do you see?--Posted like silent sentinels all around the town, stand\
    thousands upon thousands of mortal men fixed in ocean reveries. Some\
    leaning against the spiles; some seated upon the pier-heads; some\
    looking over the bulwarks of ships from China; some high aloft in the\
    rigging, as if striving to get a still better seaward peep. But these\
    are all landsmen; of week days pent up in lath and plaster--tied to\
    counters, nailed to benches, clinched to desks. How then is this? Are\
    the green fields gone? What do they here? As most young candidates for the pains and penalties of whaling stop at this same New Bedford, thence to embark on their voyage, it may as well\
    be related that I, for one, had no idea of so doing. For my mind was made up to sail in no other than a Nantucket craft, because there was a fine, boisterous something about everything connected with that famous\
    old island, which amazingly pleased me. Besides though New Bedford has\
    of late been gradually monopolising the business of whaling, and though\
    in this matter poor old Nantucket is now much behind her, yet Nantucket\
    was her great original--the Tyre of this Carthage;--the place where the\
    first dead American whale was stranded. Where else but from Nantucket\
    did those aboriginal whalemen, the Red-Men, first sally out in canoes to\
    give chase to the Leviathan? And where but from Nantucket, too, did that\
    first adventurous little sloop put forth, partly laden with imported\
    cobblestones--so goes the story--to throw at the whales, in order to\
    discover when they were nigh enough to risk a harpoon from the bowsprit?"
    
    print(text_summarization(content))
  
 

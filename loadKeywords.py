from application import db
from application import Contest
import csv
import codecs
import keyPhraseExtract
from itertools import izip

def to_file(keywordlist, filename):
    f = open(filename, 'w')
    for line in keywordlist:
        for word in line:
            if word:
                f.write(word + ' ')
        f.write('\n')
    f.close()

keywords_list = []
with codecs.open('./database/cartoonDescriptions.csv', 'r') as csvfile:
    next(csvfile)
    for index, line in izip(xrange(5),csvfile):
    # for index, line in enumerate(csvfile):
          args = [l.strip() for l in line.split(',')]
          encoded = [s.decode('utf8') for s in args]
          # encoded += [None, None]
          keywords = keyPhraseExtract.keyphrase_extract(encoded[8]) # current position of incongruity
          keywords_list.append(keywords[0])
          print keywords[0]
          to_file(keywords_list, 'keywords_file_1.txt')
        #   current_contest = Contest.query.filter_by(id=index).first()
        #   print index
        #   print current_contest
        #   current_contest.keyword_0 = keywords[0][0]
        #   current_contest.keyword_1 = keywords[0][1]
        #   db.session.commit()

      # contest = Contest(*encoded)
      # db.session.add(contest)

# db.session.commit()

# contests = Contest.query.all()
# print len(contests)

from application import db
from application import Contest
import csv
import codecs
import keyPhraseExtract

with codecs.open('./database/cartoonDescriptions.csv', 'r') as csvfile:
  next(csvfile)
  for line in csvfile:
      args = [l.strip() for l in line.split(',')]
      encoded = [s.decode('utf8') for s in args]
      # encoded += [None, None]
      keywords = keyPhraseExtract.keyphrase_extract(encoded[7])
      encoded += keywords[0]
      # print encoded
      contest = Contest(*encoded)
      db.session.add(contest)

db.session.commit()

contests = Contest.query.all()
print len(contests)

import sys
import os.path
import operator

class Ratings(object):
    DEFAULT_RATING = 1000
    K = 40
    def __init__(self, rf = None):
        self.ratings = {}
        self.games = {}
        if rf:
            with file(rf) as fp:
                for line in fp:
                    team, rating, games = line.strip().split()
                    self.ratings[int(team)] = int(rating)
                    self.games[int(team)] = int(games)
    def get(self, team):
        return self.ratings.get(team, Ratings.DEFAULT_RATING)

    def adjust(self, team, amount):
        current = self.get(team)
        self.ratings[team] = current + amount
        self.games[team] = 1 + self.games.get(team, 0)

    def getRatings(self):
        for team, rating in self.ratings.items():
            yield team, rating, self.games[team]



class Match(object):
    def __init__(self, red, blue, red_score, blue_score):
        self.red = red
        self.blue = blue
        self.red_score = red_score
        self.blue_score = blue_score

    def __repr__(self):
        return '<%s, %s, %d, %d>' % (':'.join(str(x) for x in self.red),
                                     ':'.join(str(x) for x in self.blue),
                                     self.red_score, self.blue_score)

    def redRating(self, r):
        return sum(r.get(x) for x in self.red) / len(self.red)

    def blueRating(self, r):
        return sum(r.get(x) for x in self.blue) / len(self.blue)

    def applyResults(self, r):
        rr, rb = self.redRating(r), self.blueRating(r)
        qr = pow(10, rr / 400)
        qb = pow(10, rb / 400)
        er = qr / (qr + qb)
        eb = qb / (qb + qr)
        for t in self.red:
            r.adjust(t, Ratings.K * (self.red_score - er))
        for t in self.blue:
            r.adjust(t, Ratings.K * (self.blue_score - eb))

def readMatches(tdir):
    with file(os.path.join(tdir, 'match_data.txt')) as fp:
        for line in fp:
            a = line.strip().split('|')
            if 2 > len(a):
                continue
            if a[2].startswith('QUALIFI'):
                red = [int(x) for x in a[3:5]]
                blue = [int(x) for x in a[6:8]]
            else:
                red = [int(x) for x in a[3:6]]
                blue = [int(x) for x in a[6:9]]
            if a[-1].endswith('R'):
                rs, bs = 1, -1
            elif a[-1].endswith('B'):
                rs, bs = -1, 1
            else:
                rs, bs = 0, 0
            yield Match(red, blue, rs, bs)


if '__main__' == __name__:
    if 2 < len(sys.argv):
        r = Ratings(sys.argv[2])
    else:
        r = Ratings()
    for match in readMatches(sys.argv[1]):
        match.applyResults(r)
    for team, rating, games in sorted(r.getRatings(), key = operator.itemgetter(1)):
        print '%d\t%d\t%d' % (team, rating, games)

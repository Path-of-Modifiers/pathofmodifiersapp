from redis import Redis


class PlotRateLimit:
    def __init__(self, upperLimit=5, ttl=60):
        self.upperLimit = 5
        self.ttl = 60
        self.remainingTries = 0

    def get_limit(self, userToken):
        r = Redis()

        if r.get(userToken) is None:
            self.remainingTries = self.upperLimit - 1

            r.setex(userToken, self.ttl, value=self.remainingTries)

        else:
            self.remainingTries = int(r.get(userToken).decode("utf-8")) - 1

            r.setex(userToken, r.ttl(userToken), value=self.remainingTries)

            self.ttl = r.ttl(userToken)

from globals import CONFIG


class VoteAct(object):

    def __init__(self, act, n_yeas):
        self.act = act
        self._n_yeas = n_yeas  # number of yeas required to act
        self._yeas = []  # list of users who've yea'd
        self._satisfied = False

    def __contains__(self, item):
        return item in self._yeas

    def is_satisfied(self):
        return self._satisfied

    def add_member(self, member):
        self._yeas.append(member)
        if len(self._yeas) >= self._n_yeas:
            self._satisfied = True

    @property
    def n_voters(self):
        return len(self._yeas)


class Counsel(object):

    def __init__(self):
        self.vote_acts = {}

    def try_vote_act(self, command, vote_act, cmd_root):
        if not command in self.vote_acts.keys():
            self.vote_acts[command] = VoteAct(vote_act, CONFIG['vote'][cmd_root])

    async def query(self, command, member, cmd_root, channel):

        vote_act = self.vote_acts[command]
        if member not in vote_act:
            vote_act.add_member(member)
        if vote_act.is_satisfied():
            await channel.send('Vote passed! Executing "{}"'.format(command))
            await vote_act.act()
        else:
            await channel.send('Vote status: {}/{} for "{}"'.format(vote_act.n_voters,
                                                                    CONFIG['vote'][cmd_root], command))


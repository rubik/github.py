from web import JSONModel, WebManager
from core import User


class GistsManager(WebManager):

    def public(self):
        return map(Gist, self.get('/gists/public'))
    
    #FIXME: Does not work.
    #def starred(self):
    #    return self.get('/gists/starred')

    def by_id(self, id):
        return Gist(self.get('/gists/%s' % (id)))


class GistFile(JSONModel):

    _fields = ('content', 'size', 'filename', 'raw_url')

    def __repr__(self):
        return '<GistFile [%s]>' % (self.filename)


class GistComment(JSONModel):

    _fields = ('body', 'created_at', 'updated_at', 'url', 'id')
    _ext = ('user',)

    def _extend(self, data):
        self.user = User(data['user'])

    @classmethod
    def from_id(cls, id):
        return map(cls, GistsManager().get('/gists/%s/comments' % (id)))

    def __repr__(self):
        return '<GistComment [%s]>' % (self.id)


class GistFork(JSONModel):

    _fields = ('url', 'created_at', 'id')
    _ext = ('user',)

    def _extend(self, data):
        self.user = User(data['user'])

    @ property
    def gist(self):
        return Gist.from_id(self.id)

    def __repr__(self):
        return '<GistFork [%s]>' % (self.id)


class Gist(JSONModel):

    _fields = ('id', 'url', 'html_url', 'git_push_url', 'git_pull_url', 'public',
               'description')
    _ext = ('files', 'user', 'forks', 'comments')

    def _extend(self, data):
        self._comments = data['comments']
        self.files = map(GistFile, data['files'].values())
        self.user = User(data['user'])
        self.forks = map(GistFork, data['forks'])

    @property
    def comments(self):
        if self._comments == 0 or isinstance(self._comments, list):
            return self._comments
        self._comments = GistComment.from_id(self.id)
        return self._comments

    @classmethod
    def from_id(cls, id):
        return cls(GistsManager().get('/gists/%s' % (id)))

    def __repr__(self):
        return '<Gist [%s]>' % (self.id)
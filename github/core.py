from web import JSONModel


class User(JSONModel):

    _fields = ('type', 'url', 'gravatar_url', 'blog', 'login', 'avatar_url',
               'public_gists', 'hireable', 'following', 'created_at', 'email',
               'company', 'bio', 'followers', 'location', 'public_repos',
               'html_url', 'name', 'id')

    def __repr__(self):
        return '<User %s [%s]>' % (self.id, self.login)


class ChangeStatus(JSONModel):

    _fields = ('additions', 'deletions', 'total')

    def __repr__(self):
        return '<ChangeStatus: +%s -%s>' % (self.additions, self.deletions)
from google.appengine.ext import ndb
import webapp2
import jinja2
import os
from models import User
from webapp2_extras import sessions

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class BaseHandler(webapp2.RequestHandler):              # taken from the webapp2 extrta session example
    def dispatch(self):                                 # override dispatch
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)       # dispatch the main handler
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

class WelcomeHandler(BaseHandler):
    def get(self):
        welcome_template = JINJA_ENVIRONMENT.get_template('templates/welcome.html')
        self.response.write(welcome_template.render())

    def post(self):
        email = self.request.get('email')
        password = self.request.get('password')

        if ((verification(email,password))):
            user = User.query().filter(User.email == email).fetch()[0]
            self.session['user']= email
            user_dict = {'user':user}
            self.response.write(JINJA_ENVIRONMENT.get_template('templates/dashboard.html').render(user_dict))
        else:
            pass
            #display error message in welcome

def verification(email,password):
    #verify email and password
    #return true if exists
    #return false if account doesnt exist with given input
    return True

class SignUpHandler(BaseHandler):
    def get (self):
        signup_template=JINJA_ENVIRONMENT.get_template('templates/signup.html')
        self.response.write(signup_template.render())
    def post(self):
        first_name = self.request.get('first_name')
        last_name = self.request.get('last_name')
        email = self.request.get('email')
        password = self.request.get('password')
        college = self.request.get('college')
        courses = self.request.get('courses') # list
        profile_pic = self.request.get('profile_pic')
        name = [first_name,last_name]
        new_user = User(name = name, email = email,
                        password = password, college = college,
                        profile_pic = profile_pic, college_pic = "",
                        friends=[],)
        new_user.put()
        self.session['user'] = email

        user_dict={'user':new_user}

        dashboard_template = JINJA_ENVIRONMENT.get_template('templates/dashboard.html')
        self.response.write(dashboard_template.render(user_dict))

class DashboardHandler(BaseHandler):
    def get(self): #get rid of eventually or check to see if signed in
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        user_dict={'user':user}
        dashboard_template = JINJA_ENVIRONMENT.get_template('templates/dashboard.html')
        self.response.write(dashboard_template.render(user_dict))


class UserProfileHandler(BaseHandler):
    def get (self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        user_dict={'user':user}
        userprofile_template = JINJA_ENVIRONMENT.get_template('templates/userprofile.html')
        self.response.write(profile_template.render(user_dict))

    def post(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        user_dict={'user':user}
        newsfeed_template = JINJA_ENVIRONMENT.get_template('templates/userprofile.html')

class HostConnectHandler(BaseHandler):
    def get(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        user_dict={'user':user}
        hostconnect_template = JINJA_ENVIRONMENT.get_template('templates/hostconnect.html')
        self.response.write(hostconnect_template.render(user_dict))

    def post(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        time = self.request.get('time')
        location = self.request.get('location')
        alert_time = self.request.get('alert_time')
        new_ConnectEvent = ConnectEvent(time = time,location = location,
                                        alert_time = alert_time)
        users = [user]
        new_UserConnectEvent = UserConnectEvent(users=users,
                                                connect_event=new_ConnectEvent)

class JoinConnectHandler(BaseHandler):
    def get(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        user_dict={'user':user}
        joinconnect_template = JINJA_ENVIRONMENT.get_template('templates/joinconnect.html')
        self.response.write(joinconnect_template.render(user_dict))

    def post(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]


class FriendsHandler(BaseHandler):
    def get(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        user_dict={'user':user}
        friends_template = JINJA_ENVIRONMENT.get_template('templates/friends.html')
        self.response.write(freinds_template.render(user_dict))

    def post(self):
        user = User.query().filter(User.email == self.session.get('user')).fetch()[0]
        # friend_added = self.request.get('friends_added') #if just one friend
        friends_added = self.request.get('friends_added')
        user.friends.extend(friend_added)




config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'some-secret-key',
}

app = webapp2.WSGIApplication([
    ('/', WelcomeHandler),
    ('/signup', SignUpHandler),
    ('/dashboard', DashboardHandler),
    ('/userprofile', UserProfileHandler),
    ('/hostconnect',HostConnectHandler),
    ('/joinconnect',JoinConnectHandler),
    ('/friends',FriendsHandler),
], debug=True, config=config)

#!/usr/bin/env python
import os
import jinja2
import webapp2
import random

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):

        return self.render_template("main.html")

    def post(self):

        random_number = 10

        guess = float(self.request.get("enter_guess"))

        def guesses(guess):
            if guess == random_number:
                return "You guessed the number."
            else:
                return "You haven't guessed the number."

        environment = dict()
        environment["guesses"] = guesses(guess)

        self.write("entered was: " + str(guess))

        return self.render_template("main.html", params=environment)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)

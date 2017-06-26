from __future__ import unicode_literals
from django.db import models
import re

EMAIL_REGEX =re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def makeUser(self,firstname, lastname, email, password, confirmpassword):

        errors =[]
        user_list = User.objects.filter(email=email)

        if len(firstname) < 2:
            errors.append("first name is too short")
        if len(lastname) < 2:
            errors.append("last name is too short")

        if len(email) < 2:
            errors.append("email not valid")
        if not EMAIL_REGEX.match(email):
            errors.append("email not valid")

        if len(password) < 8:
            errors.append("password is too short")
        elif password != confirmpassword:
            errors.append("Password does not match")

        if not errors:
            if email == User.objects.filter(email=email):
                errors.append("email not valid")
            else:
                user = User.objects.create(firstname=firstname, lastname=lastname, email=email, password=password)
            return {"status":True, "user": user_list[0]}

        else:
            return{"status": False, "user": errors}

    def log(self, email, password):
        error = False
        user_list = User.objects.filter(email=email)

        if len(user_list) < 1 :
            error = True
        elif user_list[0].password != password:
            error = True

        if not error:
            return {"status":True, "user": user_list[0]}
        else:
            return {"status": False}

class User(models.Model):
    firstname = models.CharField(max_length = 26)
    lastname = models.CharField(max_length = 26)
    email = models.CharField(max_length = 26)
    password = models.CharField(max_length = 26)
    confirmpassword = models.CharField(max_length = 26)
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

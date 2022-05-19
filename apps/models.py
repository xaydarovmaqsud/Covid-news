from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)

    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return f'{self.user.first_name} {self.user.last_name}'
        elif self.user.first_name:
            return self.user.first_name
        elif self.user.last_name:
            return self.user.last_name
        else:
            return self.user.username


class Author(models.Model):
    full_name = models.CharField(max_length=255)
    spesialist = models.CharField(max_length=255)
    bio = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.full_name


class Category(models.Model):
    name = models.CharField(max_length=30)
    descriptions = models.CharField(max_length=200)
    person = models.ForeignKey(Person,on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class New(models.Model):
    author = models.ForeignKey(Author, related_name='articles', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    autor = models.CharField(max_length=500)
    image = models.ImageField(null=True, blank=True)
    file = models.FileField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    view_count = models.IntegerField(default=0)

    @property
    def likes(self):
        return self.reactions.filter(reaction='likes').count()


    @property
    def dislikes(self):
        return self.reactions.filter(reaction='dislikes').count()

    def setcomment(self, person, comment):
        if comment:
            comment_obj = Comment.objects.create(
                new=self,
                person=person,
                comment=comment
            )
        print(comment)

    def setreaction(self, person, react):
        current_reacts = Reaction.objects.filter(person=person)
        current_react = current_reacts[0] if current_reacts else None
        if not current_react:
            reaction_obj = Reaction.objects.create(
                new=self,
                person=person,
                reaction=react
            )
        elif current_react.reaction != react:
            current_react.reaction = react
            current_react.save()
        else:
            current_react.delete()

    @property
    def view_add(self):
        self.view_count = self.view_count + 1
        self.save()

    def __str__(self):
        return self.title

    def imageURL(self):
        try:
            return self.image.url
        except:
            return ' '

    def fileURL(self):
        try:
            return self.file.url
        except:
            return ' '


class Reaction(models.Model):
    new = models.ForeignKey(New,related_name='reactions', on_delete=models.CASCADE)
    person = models.ForeignKey(Person, related_name='reacts', on_delete=models.SET_NULL, null=True, blank=True)
    reaction = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.person} s react for {self.new}'


class Comment(models.Model):
    new = models.ForeignKey(New, related_name='comments', on_delete=models.CASCADE)
    person = models.ForeignKey(Person, related_name='comments', on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.TextField()

    def __str__(self):
        return f'{self.person} s comment for {self.new}: {self.comment}'

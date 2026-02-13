from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone



# USER PROFILE

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username



# HOMEPAGE / ABOUT

class About(models.Model):
    content = models.TextField()
    about_photo = models.ImageField(upload_to='about_photos/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)



# MESSAGING SYSTEM

class Thread(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='thread_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='thread_user2')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Thread: {self.user1} & {self.user2}"


class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender.username}"



# SOCIAL POSTS

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Comment by {self.commenter.username}"



# LEARNING SYSTEM

class Chapter(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Lesson(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    lesson_photo = models.ImageField(upload_to='lesson_photos/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.chapter.title} - {self.title}"


class Flashcard(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='flashcards', on_delete=models.CASCADE)
    hanzi = models.CharField(max_length=20)
    pinyin = models.CharField(max_length=100)
    meaning = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.hanzi} ({self.pinyin})"


class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='quizzes', on_delete=models.CASCADE)
    question = models.TextField()
    option_a = models.CharField(max_length=100)
    option_b = models.CharField(max_length=100)
    option_c = models.CharField(max_length=100)
    option_d = models.CharField(max_length=100)
    correct_answer = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
    )
    is_active = models.BooleanField(default=True)

    def clean(self):
        if self.correct_answer not in ['A', 'B', 'C', 'D']:
            raise ValidationError("Correct answer must be A, B, C, or D.")

    def __str__(self):
        return f"Quiz for {self.lesson.title}"



# PROGRESS TRACKING (IMPROVED)


class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"



# GUESSING GAME


class PictureGuessQuestion(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('input', 'Text Input'),
        ('multiple_choice', 'Multiple Choice'),
    ]

    image = models.ImageField(upload_to='picture_guessing/')
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default='input')
    hanzi_answer = models.CharField(max_length=50)
    pinyin = models.CharField(max_length=100, blank=True)
    english = models.CharField(max_length=100, blank=True)
    hint = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Guess: {self.english or self.hanzi_answer}"


class MultipleChoiceOption(models.Model):
    question = models.ForeignKey(PictureGuessQuestion, related_name='options', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def clean(self):
        if self.is_correct:
            if MultipleChoiceOption.objects.filter(
                question=self.question,
                is_correct=True
            ).exclude(id=self.id).exists():
                raise ValidationError("Only one correct option allowed.")

    def __str__(self):
        return self.option_text



# MATCHING EXERCISE


class MatchingExercise(models.Model):
    TYPE_CHOICES = [
        ('pinyin_hanzi', 'Pinyin to Hanzi'),
        ('hanzi_english', 'Hanzi to English'),
    ]

    title = models.CharField(max_length=100)
    instructions = models.TextField(default="Match the correct pairs")
    exercise_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.get_exercise_type_display()})"


class MatchingPair(models.Model):
    exercise = models.ForeignKey(MatchingExercise, related_name='pairs', on_delete=models.CASCADE)
    hanzi = models.CharField(max_length=50)
    pinyin = models.CharField(max_length=100, blank=True)
    english = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.hanzi}"



# SENTENCE PUZZLE


class SentencePuzzle(models.Model):
    title = models.CharField(max_length=100)
    instruction = models.TextField(default="Reorder the sentence correctly")
    correct_sentence = models.TextField()
    pinyin = models.CharField(max_length=200)
    translation = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.correct_sentence


class WordTile(models.Model):
    puzzle = models.ForeignKey(SentencePuzzle, related_name='tiles', on_delete=models.CASCADE)
    hanzi = models.CharField(max_length=20)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.hanzi

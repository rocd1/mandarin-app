from django.contrib import admin
from .models import *

# =============================
# USER PROFILE
# =============================

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)


# =============================
# LEARNING SYSTEM
# =============================

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_published', 'created_by')
    list_filter = ('is_published',)
    search_fields = ('title',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter', 'order', 'is_published')
    list_filter = ('is_published', 'chapter')
    search_fields = ('title',)


@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('hanzi', 'pinyin', 'lesson')
    search_fields = ('hanzi', 'pinyin')


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'question', 'correct_answer', 'is_active')
    list_filter = ('is_active',)


# =============================
# SOCIAL
# =============================

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'created_at')
    list_filter = ('is_published',)
    search_fields = ('title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'commenter', 'timestamp')
    search_fields = ('commenter__username',)


# =============================
# PROGRESS
# =============================

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed', 'score')
    list_filter = ('completed',)


# =============================
# GAMES
# =============================

admin.site.register(PictureGuessQuestion)
admin.site.register(MultipleChoiceOption)
admin.site.register(MatchingExercise)
admin.site.register(MatchingPair)
admin.site.register(SentencePuzzle)
admin.site.register(WordTile)

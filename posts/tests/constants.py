from django.urls import reverse

HOME_PAGE = reverse('index')
ABOUT_AUTHOR_PAGE = reverse('about:author')
ABOUT_TECH_PAGE = reverse('about:tech')
NEW_POST_PAGE = reverse('new_post')
FOLLOW = reverse('follow_index')

# User
username = 'TestUser'

# User2
username2 = 'TestUser2'

# Group
title = 'TestGroup'
slug = 'TestSlug'
description = 'TestDescription'
title_other = 'TestGroupOther'
slug_other = 'TestSlugOther'
description_other = 'TestDescriptionOther'
# Post
text = 'TestText'
text_edit = 'TestTextEdit'
text_other = 'TestTextOther'

group_page = reverse('group', kwargs={'slug': slug})
profile_page = reverse('profile', kwargs={'username': username})

# Page not found
PAGE_NOT_FOUND = reverse('group', kwargs={'slug': 'not_found'})

# Verbose name and help text Post
field_verboses_Post = {
    'text': 'Содержание поста',
    'group': 'Группа',
}
field_help_texts_Post = {
    'text': 'Введите содержание вашего поста.',
    'group': 'Выберите группу.',
}

# Verbose name and help text Group
field_verboses_Group = {
    'title': 'Заголовок',
    'slug': 'URL',
    'description': 'Описание',
}
field_help_texts_Group = {
    'title': 'Введите заголовок вашего поста.',
    'description': 'Введите описание вашего поста.',
}

small_gif = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B'
)

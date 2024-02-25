import re

from rest_framework.serializers import ValidationError


class LinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        """
        Проверка, что ссылка на материал ведет только на youtube.com.
        """
        youtube_regex = re.compile(
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

        tmp_val = dict(value).get(self.field)

        if not bool(youtube_regex.match(tmp_val)):
            raise ValidationError("Ссылка на материал должна быть с YouTube.")

        return value

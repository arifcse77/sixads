from django.test import TestCase
from .models import Tag, Channel


class TagNameTestCase(TestCase):
    def setUp(self):
        Tag.objects.create(tag_name="lion")
        Tag.objects.create(tag_name="cat")

    def test_tag_name(self):
        lion_model = Tag.objects.filter(tag_name="lion").first()
        cat_model = Tag.objects.filter(tag_name="cat").first()

        self.assertEqual(lion_model.tag_name, 'lion')
        self.assertEqual(cat_model.tag_name, 'cat')


class ChannelTestCase(TestCase):
    def setUp(self) -> None:
        Channel.objects.create(youtube_channel_id="UCBi2mrWuNuyYy4gbM6fU18Q", channel_title="ABC News")

    def test_channel(self):
        model = Channel.objects.filter(youtube_channel_id="UCBi2mrWuNuyYy4gbM6fU18Q").first()

        self.assertEqual(model.youtube_channel_id, 'UCBi2mrWuNuyYy4gbM6fU18Q')
        self.assertEqual(model.channel_title, 'ABC News')



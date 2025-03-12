from django.test import TestCase
from .models import ScamMessage
from .forms import ScamMessageForm

class ScamMessageModelTest(TestCase):
    
    def test_create_scam_message(self):
        scam_message = ScamMessage.objects.create(
            text="This is a scam message",
            risk_score=80.0,
            keywords="scam, fraud",
            category="scam"
        )

        self.assertEqual(scam_message.text, "This is a scam message")
        self.assertEqual(scam_message.risk_score, 80.0)
        self.assertEqual(scam_message.keywords, "scam, fraud")
        self.assertEqual(scam_message.category, "scam")

    def test_default_category(self):
        scam_message = ScamMessage.objects.create(
            text="This message has no category",
            risk_score=50.0,
            keywords="test"
        )
        self.assertEqual(scam_message.category, "other")  # 假設預設值是 "other"

class ScamMessageFormTest(TestCase):
    
    def test_valid_form(self):
        form_data = {'text': "This is a valid scam message"}
        form = ScamMessageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {'text': ""}
        form = ScamMessageForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)

    def test_cleaned_data(self):
        form_data = {'text': "   Scam  message  with extra spaces  "}
        form = ScamMessageForm(data=form_data)
        form.is_valid()
        self.assertEqual(form.cleaned_data['text'], "Scam message with extra spaces")

    def test_missing_text_field(self):
        form_data = {}  # 沒有提供 `text` 字段
        form = ScamMessageForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)

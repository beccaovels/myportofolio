from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Education


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="PBP Teaching Assistant",
            description="Help students understand web development.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/a-page-that-does-not-exist/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "PBP Teaching Assistant")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Ongoing")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "No experience has been added yet.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Completed")
        self.assertNotContains(response, "Ongoing")


class EducationTest(TestCase):
    def setUp(self):
        self.education = Education.objects.create(
            institution="Universitas Indonesia",
            program="S1 Ilmu Komputer KKI",
            level="university",
            description="Studying computer science with a focus on AI/ML.",
            started_at="2023-08-01",
        )

    def test_education_url_is_accessible_and_uses_correct_template(self):
        """Scenario 1: The URL is accessible and uses the correct template."""
        response = self.client.get(reverse("main:show_education"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")

    def test_education_data_appears_when_not_empty(self):
        """Scenario 2: Model data appears in the returned HTML response
        when the data is not empty."""
        response = self.client.get(reverse("main:show_education"))

        self.assertContains(response, self.education.institution)
        self.assertContains(response, self.education.program)
        self.assertContains(response, self.education.description)
        self.assertContains(response, "University")
        self.assertContains(response, "Present")

    def test_empty_education_page_shows_empty_message(self):
        """Scenario 3: An empty message appears in the returned HTML
        response when the data is empty."""
        Education.objects.all().delete()
        response = self.client.get(reverse("main:show_education"))

        self.assertContains(response, "No education records have been added yet.")
        self.assertNotContains(response, self.education.program)
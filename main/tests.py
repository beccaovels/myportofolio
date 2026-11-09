from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Education


class MainTest(TestCase):
    """Since Tutorial 5/7 the Experience page is an AJAX shell: the HTML has no
    cards, and the data comes from /api/v1/experience/. These tests keep their
    original intent but check each part where it now lives."""

    def setUp(self):
        self.experience = Experience.objects.create(
            title="PBP Teaching Assistant",
            description="Help students understand web development.",
            category="part-time",
            started_at=timezone.now(),
        )
        self.api_url = reverse("api:experience-list")

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
        self.assertContains(response, f'href="{reverse("main:show_main")}"')
        # The page loads its cards from the DRF endpoint...
        self.assertContains(response, self.api_url)
        self.assertContains(response, 'id="grid"')
        # ...which returns the experience data (ongoing = no end date).
        item = self.client.get(self.api_url).json()[0]
        self.assertEqual(item["title"], self.experience.title)
        self.assertEqual(item["description"], self.experience.description)
        self.assertEqual(item["category"], "part-time")
        self.assertIsNone(item["ended_at"])

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "No experiences have been added or found yet.")
        self.assertEqual(self.client.get(self.api_url).json(), [])

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()

        self.assertFalse(self.experience.is_ongoing)
        item = self.client.get(self.api_url).json()[0]
        self.assertIsNotNone(item["ended_at"])


class SkillsPageTest(TestCase):
    """Regression: the template used to read user.is_editor (which doesn't
    exist), so Editors never saw the Edit button."""

    def test_editor_flag_reaches_the_page_script(self):
        editor = User.objects.create_user(username="editor")
        editor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_login(editor)
        response = self.client.get(reverse("main:show_skills"))

        self.assertContains(response, 'const IS_EDITOR = "true" === "true";')
        self.assertContains(response, reverse("api:skill-list"))

    def test_regular_user_is_not_editor(self):
        self.client.force_login(User.objects.create_user(username="regular"))
        response = self.client.get(reverse("main:show_skills"))

        self.assertContains(response, 'const IS_EDITOR = "false" === "true";')

    def test_edit_modal_is_rendered_for_editor_and_owner_only(self):
        # Assignment 6: the owner and Editors edit through the PATCH modal.
        editor = User.objects.create_user(username="editor")
        editor.groups.add(Group.objects.create(name="Editor"))
        owner = User.objects.create_superuser(username="owner", password=None)
        for user, has_modal in ((editor, True), (owner, True),
                                (User.objects.create_user(username="regular"), False)):
            self.client.force_login(user)
            response = self.client.get(reverse("main:show_skills"))
            if has_modal:
                self.assertContains(response, 'id="skill-form"')
            else:
                self.assertNotContains(response, 'id="skill-form"')
        self.client.logout()
        self.assertNotContains(self.client.get(reverse("main:show_skills")), 'id="skill-form"')

    def test_add_button_is_owner_only(self):
        editor = User.objects.create_user(username="editor")
        editor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_login(editor)
        self.assertNotContains(self.client.get(reverse("main:show_skills")), 'id="add-skill-button"')

        self.client.force_login(User.objects.create_superuser(username="owner", password=None))
        self.assertContains(self.client.get(reverse("main:show_skills")), 'id="add-skill-button"')

    def test_sort_control_offers_the_api_orderings(self):
        response = self.client.get(reverse("main:show_skills"))
        for value in ("newest", "name", "stars"):
            self.assertContains(response, f'<option value="{value}">')


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
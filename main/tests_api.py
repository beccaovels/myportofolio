import uuid
from datetime import timedelta

from django.contrib.auth.models import Group, User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Experience, Skill


class ExperienceAPITest(APITestCase):
    """Tutorial 7's 13 API tests, adapted from Project to Experience."""

    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.experience = Experience.objects.create(
            title="Teaching Assistant",
            employer="Fasilkom UI",
            description="Helped students learn web development.",
            category="part-time",
            started_at=timezone.now(),
        )
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse("api:experience-detail", args=[self.experience.id])
        self.star_url = reverse("api:experience-star", args=[self.experience.id])
        self.payload = {
            "title": "Front-End Developer",
            "employer": "DDP0 2026",
            "description": "Built the event website.",
            "category": "volunteer",
            "started_at": "2026-08-01T00:00:00Z",
            "ended_at": "2026-09-01T00:00:00Z",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.experience.id))
        self.assertFalse(response.data[0]["is_starred"])
        # New flat contract: no Tutorial 5 "pk"/"fields" wrapper
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "TEACHING"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_missing_experience(self):
        url = reverse("api:experience-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Teaching Assistant")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Experience.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"category": "astronaut"}, "category"),
            ({"started_at": "2026-09-01T00:00:00Z", "ended_at": "2026-08-01T00:00:00Z"}, "ended_at"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Experience.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Changed")
        self.assertEqual(self.experience.description, "Helped students learn web development.")
        # PUT is a full replacement, so missing required fields fail
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Experience.objects.filter(pk=self.experience.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertEqual(response.data["starred_by_names"], "visitor")
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        forged_id = str(uuid.uuid4())
        response = self.client.post(self.list_url, {
            **self.payload, "id": forged_id, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data["id"], forged_id)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["starred_by_names"], "")

    def test_staff_and_editor_cannot_manage_experience(self):
        # Experience follows the tutorial rule: only the owner manages it.
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.client.force_authenticate(user=self.visitor)
        self.assertEqual(self.client.get(self.star_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        # The Browsable API page renders a real CSRF token and sets the cookie.
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class SkillAPITest(APITestCase):
    """Assignment section: the four Assignment 4 roles enforced by the API.

    visitor -> read | user -> read + star | Editor -> + PUT/PATCH | owner -> everything
    Users have no password because force_authenticate never checks one; only
    the session/CSRF tests set one, since .login() needs a real password.
    """

    PASSWORD = "test-password"

    def setUp(self):
        self.owner = User.objects.create_superuser(username="owner", password=None)
        self.user = User.objects.create_user(username="regular")
        self.editor = User.objects.create_user(username="editor")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.skill = Skill.objects.create(name="Python", description="Main language")
        self.list_url = reverse("api:skill-list")
        self.detail_url = reverse("api:skill-detail", args=[self.skill.id])
        self.star_url = reverse("api:skill-star", args=[self.skill.id])
        self.payload = {
            "name": "Django",
            "description": "Web framework",
            "logo_url": "https://example.com/django.png",
        }

    def test_visitor_can_read_list_detail_and_search(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.skill.id))
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.client.get(self.list_url, {"name": "PYTH"}).data), 1)
        self.assertEqual(self.client.get(self.list_url, {"name": "nope"}).data, [])

    def test_missing_skill(self):
        url = reverse("api:skill-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_visitor_and_regular_user_cannot_write(self):
        for user in (None, self.user):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"name": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.name, "Python")
        self.assertEqual(Skill.objects.count(), 1)

    def test_editor_can_update_but_not_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"name": "Python 3"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.name, "Python 3")
        self.assertEqual(self.skill.description, "Main language")
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertTrue(Skill.objects.filter(pk=self.skill.id).exists())
        self.assertEqual(Skill.objects.count(), 1)

    def test_staff_without_editor_group_cannot_update(self):
        # is_staff is not one of our roles; only the Editor group grants updates.
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.detail_url, {"name": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_create_update_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Skill.objects.filter(pk=response.data["id"]).exists())
        response = self.client.patch(self.detail_url, {"description": "Updated"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # PUT is a full replacement, so leaving out the required name fails
        response = self.client.put(self.detail_url, {"description": "No name"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Skill.objects.filter(pk=self.skill.id).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"name": "   "}, "name"),
            ({"name": "<script></script>"}, "name"),
            ({"logo_url": "javascript:alert(1)"}, "logo_url"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Skill.objects.count(), 1)

    def test_description_tags_are_stripped(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "description": "<b>Fast</b> framework",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["description"], "Fast framework")

    def test_drive_link_is_converted_to_thumbnail(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "logo_url": "https://drive.google.com/file/d/abc_123/view?usp=sharing",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["logo_url"], "https://drive.google.com/thumbnail?id=abc_123&sz=w1000")

    def test_any_logged_in_role_can_star_and_toggle(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        for user in (self.user, self.editor):
            self.client.force_authenticate(user=user)
            response = self.client.post(self.star_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 2)
        self.assertCountEqual(response.data["starred_by_names"].split(", "), ["regular", "editor"])
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True, "starred_by_names": "forged",
            "starred_by": [self.user.id], "created_at": "2000-01-01T00:00:00Z",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertFalse(response.data["created_at"].startswith("2000"))

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(self.client.get(self.star_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # --- ?ordering= (extra feature) ------------------------------------------

    def _make_ordering_fixture(self):
        """Python (oldest, 0 stars) < go (2 stars) < Zig (newest, 1 star).

        created_at is set explicitly: auto_now_add values can tie on fast
        machines, which would make "newest" flaky.
        """
        base = timezone.now()
        go = Skill.objects.create(name="go")
        zig = Skill.objects.create(name="Zig")
        for skill, days in ((self.skill, 0), (go, 1), (zig, 2)):
            Skill.objects.filter(pk=skill.pk).update(created_at=base + timedelta(days=days))
        go.starred_by.add(self.user, self.editor)
        zig.starred_by.add(self.user)

    def _names(self, params):
        response = self.client.get(self.list_url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return [item["name"] for item in response.data]

    def test_ordering_defaults_to_newest(self):
        self._make_ordering_fixture()
        self.assertEqual(self._names({}), ["Zig", "go", "Python"])
        self.assertEqual(self._names({"ordering": "newest"}), ["Zig", "go", "Python"])

    def test_ordering_by_name_is_case_insensitive(self):
        self._make_ordering_fixture()
        self.assertEqual(self._names({"ordering": "name"}), ["go", "Python", "Zig"])

    def test_ordering_by_stars(self):
        self._make_ordering_fixture()
        self.assertEqual(self._names({"ordering": "stars"}), ["go", "Zig", "Python"])
        # Annotating the count must not change the serializer's star_count.
        top = self.client.get(self.list_url, {"ordering": "stars"}).data[0]
        self.assertEqual(top["star_count"], 2)

    def test_ordering_combines_with_search(self):
        self._make_ordering_fixture()
        self.assertEqual(self._names({"name": "o", "ordering": "stars"}), ["go", "Python"])

    def test_unknown_ordering_is_rejected(self):
        for value in ("bogus", "-created_at", "starred_by__email"):
            response = self.client.get(self.list_url, {"ordering": value})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("ordering", response.data)

    # --- Real session + CSRF -------------------------------------------------
    # force_authenticate skips both login and CSRF, so these tests log in
    # through the session like the browser does and enforce CSRF checks.

    def _session_client(self, user):
        user.set_password(self.PASSWORD)
        user.save()
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username=user.username, password=self.PASSWORD))
        return client

    def test_session_write_without_csrf_is_rejected(self):
        client = self._session_client(self.owner)
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("CSRF", str(response.data["detail"]))
        self.assertEqual(Skill.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = self._session_client(self.owner)
        # The Browsable API page renders a real CSRF token and sets the cookie.
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Skill.objects.filter(name="Django").exists())

    def test_editor_patch_without_csrf_is_rejected(self):
        client = self._session_client(self.editor)
        response = client.patch(self.detail_url, {"name": "Hijacked"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.name, "Python")

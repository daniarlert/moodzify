from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..models import MoodEntry


class ListViewTest(TestCase):
    def setUp(self):
        self.url = reverse("mood_list")
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )

    def test_authenticated_user(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "moods/mood_list.html")

    def test_not_authenticated_user(self):
        self.client.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)


class CreateViewTest(TestCase):
    def setUp(self):
        self.url = reverse("mood_new")
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )

    def test_authenticated_user(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "moods/mood_create.html")

    def test_authenticated_user_can_create_mood_entry(self):
        self.client.login(username="testuser", password="testpassword")
        mood_entry = {
            "mood_level": 1,
            "notes": "This is a test.",
        }
        response = self.client.post(self.url, data=mood_entry, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(MoodEntry.objects.filter(notes="This is a test.").exists())

        created_mood_entry = MoodEntry.objects.get(notes="This is a test.")
        self.assertEqual(created_mood_entry.user, self.user)

    def test_not_authenticated_user(self):
        self.client.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)


class UpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )
        self.mood_entry = MoodEntry.objects.create(
            user=self.user,
            mood_level=1,
            notes="Initial mood entry",
        )
        self.url = reverse("mood_update", args=[self.mood_entry.id])

    def test_authenticated_user(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "moods/mood_update.html")

    def test_authenticated_user_can_update_mood_entry(self):
        self.client.login(username="testuser", password="testpassword")
        updated_notes = "Updated mood entry"
        mood_entry_data = {
            "mood_level": 2,
            "notes": updated_notes,
        }
        response = self.client.post(self.url, data=mood_entry_data, follow=True)

        self.assertEqual(response.status_code, 200)

        updated_mood_entry = MoodEntry.objects.get(id=self.mood_entry.id)
        self.assertEqual(updated_mood_entry.mood_level, 2)
        self.assertEqual(updated_mood_entry.notes, updated_notes)

    def test_authenticated_user_cannot_update_another_users_mood_entry(self):
        another_user = get_user_model().objects.create_user(
            username="anotheruser",
            email="another@example.com",
            password="anotherpassword",
        )
        another_user_mood_entry = MoodEntry.objects.create(
            user=another_user,
            mood_level=1,
            notes="Another user's mood entry",
        )

        self.client.login(username="testuser", password="testpassword")
        updated_notes = "Attempt to update another user's mood entry"
        mood_entry_data = {
            "mood_level": 2,
            "notes": updated_notes,
        }
        response = self.client.post(
            reverse("mood_update", args=[another_user_mood_entry.id]),
            data=mood_entry_data,
            follow=True,
        )

        self.assertRedirects(response, reverse("mood_list"))

    def test_not_authenticated_user(self):
        self.client.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)


class DeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )
        self.mood_entry = MoodEntry.objects.create(
            user=self.user,
            mood_level=1,
            notes="Test mood entry for deletion",
        )
        self.url = reverse("mood_delete", args=[self.mood_entry.id])

    def test_authenticated_user(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "moods/mood_delete.html")

    def test_authenticated_user_can_delete_mood_entry(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(MoodEntry.objects.filter(id=self.mood_entry.id).exists())

    def test_authenticated_user_cannot_delete_another_users_mood_entry(self):
        another_user = get_user_model().objects.create_user(
            username="anotheruser",
            email="another@example.com",
            password="anotherpassword",
        )
        another_user_mood_entry = MoodEntry.objects.create(
            user=another_user,
            mood_level=1,
            notes="Another user's mood entry",
        )

        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            reverse("mood_delete", args=[another_user_mood_entry.id]),
            follow=True,
        )

        self.assertRedirects(response, reverse("mood_list"))

    def test_not_authenticated_user(self):
        self.client.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)

from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Experience, Skill
from main.utils import normalize_drive_image_url


class StarredModelSerializer(serializers.ModelSerializer):
    """Adds the read-only star fields shared by Experience and Skill.

    The values are computed from the existing `starred_by` relation, so
    clients can read them but can never write them.
    """

    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    def get_star_count(self, obj):
        # len() over .all() reuses prefetch_related("starred_by") in list views.
        return len(obj.starred_by.all())

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        # Only usernames are exposed, never emails or other account data.
        return ", ".join(user.username for user in obj.starred_by.all())


class ExperienceSerializer(StarredModelSerializer):
    class Meta:
        model = Experience
        fields = [
            "id", "title", "employer", "description", "category",
            "started_at", "ended_at",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    # Same cleaning rules as ExperienceForm.clean_*: the API does not run
    # the form, so the rules have to live here too.
    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Experience title can't contain only HTML tags.")
        return value

    def validate_employer(self, value):
        return strip_tags(value).strip() if value else value

    def validate_description(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Description can't contain only HTML tags.")
        return value

    def validate(self, attrs):
        # On PATCH only one of the dates may be sent, so fall back to the
        # value already stored on the instance before comparing.
        started_at = attrs.get("started_at", getattr(self.instance, "started_at", None))
        ended_at = attrs.get("ended_at", getattr(self.instance, "ended_at", None))
        if started_at and ended_at and ended_at < started_at:
            raise serializers.ValidationError(
                {"ended_at": "End date can't be before the start date."}
            )
        return attrs


class SkillSerializer(StarredModelSerializer):
    class Meta:
        model = Skill
        fields = [
            "id", "name", "description", "logo_url", "created_at",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_name(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Skill name can't contain only HTML tags.")
        return value

    def validate_description(self, value):
        return strip_tags(value).strip() if value else value

    def validate_logo_url(self, value):
        # URLField has already rejected non-http(s) schemes such as javascript:.
        return normalize_drive_image_url(value)

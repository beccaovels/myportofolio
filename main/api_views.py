from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Experience, Skill
from main.permissions import IsPortfolioOwnerOrEditorOrReadOnly, IsPortfolioOwnerOrReadOnly
from main.serializers import ExperienceSerializer, SkillSerializer


def _experience_queryset():
    # Prefetch stars once so the serializer doesn't query per card.
    return Experience.objects.prefetch_related("starred_by").order_by("-started_at", "id")


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def experience_list(request):
    if request.method in ("GET", "HEAD"):
        experiences = _experience_queryset()
        title = request.query_params.get("title", "").strip()
        if title:
            experiences = experiences.filter(title__icontains=title)
        serializer = ExperienceSerializer(
            experiences, many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = ExperienceSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def experience_detail(request, experience_id):
    experience = get_object_or_404(_experience_queryset(), pk=experience_id)

    if request.method in ("GET", "HEAD"):
        serializer = ExperienceSerializer(experience, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # PUT replaces the whole representation; PATCH keeps omitted fields.
    serializer = ExperienceSerializer(
        experience, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def experience_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    # The starring account always comes from the session, never the body.
    if experience.starred_by.filter(pk=request.user.pk).exists():
        experience.starred_by.remove(request.user)
    else:
        experience.starred_by.add(request.user)
    serializer = ExperienceSerializer(experience, context={"request": request})
    return Response(serializer.data)


# --- Skills (assignment section): Editors may also update -------------------

def _skill_queryset():
    return Skill.objects.prefetch_related("starred_by").order_by("-created_at", "id")


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def skill_list(request):
    if request.method in ("GET", "HEAD"):
        skills = _skill_queryset()
        name = request.query_params.get("name", "").strip()
        if name:
            skills = skills.filter(name__icontains=name)
        serializer = SkillSerializer(skills, many=True, context={"request": request})
        return Response(serializer.data)

    serializer = SkillSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def skill_detail(request, skill_id):
    skill = get_object_or_404(_skill_queryset(), pk=skill_id)

    if request.method in ("GET", "HEAD"):
        serializer = SkillSerializer(skill, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = SkillSerializer(
        skill, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def skill_star(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    if skill.starred_by.filter(pk=request.user.pk).exists():
        skill.starred_by.remove(request.user)
    else:
        skill.starred_by.add(request.user)
    serializer = SkillSerializer(skill, context={"request": request})
    return Response(serializer.data)

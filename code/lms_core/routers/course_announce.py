from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import HttpResponse

from lms_core.models import Course, CourseAnnouncement
from lms_core.schema import CourseAnnouncementIn, CourseAnnouncementOut, MessageOut, CourseAnnouncementUpdateOut
from lms_core.api import apiAuth

announcement_router = Router(tags=["Course Announcements"])

@announcement_router.post("/{course_id}/announcements", auth=apiAuth, response={201: CourseAnnouncementOut, 403: MessageOut, 404: MessageOut})
def create_announcement(request, course_id: int, payload: CourseAnnouncementIn):
    """
    Create announcement: untuk menambahkan pengumuman pada course tertentu (hanya teacher yang dapat membuat announcement)
    """
    course = get_object_or_404(Course, id=course_id)
    if course.teacher.id != request.user.id:
        return 403, {"detail": "Only the course teacher can create announcements."}
    
    announcement = CourseAnnouncement.objects.create(course=course, **payload.dict())
    return 201, announcement

@announcement_router.get("/{course_id}/announcements", auth=apiAuth, response={200: List[CourseAnnouncementOut], 403: MessageOut, 404: MessageOut})
def list_announcements(request, course_id: int):
    """
    Show announcement: untuk menampilkan semua pengumuman pada course tertentu (teacher dan student dapat menampilkan announcement)
    """
    course = get_object_or_404(Course, id=course_id)
    # Check if the user is a member or the teacher of the course
    if not course.is_member(request.user.id) and course.teacher.id != request.user.id:
        return 403, {"detail": "You are not a member of this course."}
    
    now = timezone.now()
    announcements = CourseAnnouncement.objects.filter(course=course, show_at__lte=now)
    return 200, announcements

@announcement_router.put("/{course_id}/announcements/{announcement_id}", auth=apiAuth, response={200: CourseAnnouncementUpdateOut, 403: MessageOut, 404: MessageOut})
def update_announcement(request, course_id: int, announcement_id: int, payload: CourseAnnouncementIn):
    """
    Edit announcement: untuk mengedit announcement (hanya teacher yang dapat mengedit announcement)
    """
    course = get_object_or_404(Course, id=course_id)
    if course.teacher.id != request.user.id:
        return 403, {"detail": "Only the course teacher can edit announcements."}
        
    announcement = get_object_or_404(CourseAnnouncement, id=announcement_id, course=course)
    for attr, value in payload.dict().items():
        setattr(announcement, attr, value)
    announcement.save()
    return 200, {
        "detail": "Announcement updated successfully.",
        "announcement": announcement
    }

@announcement_router.delete("/{course_id}/announcements/{announcement_id}", auth=apiAuth, response={200: MessageOut, 403: MessageOut, 404: MessageOut})
def delete_announcement(request, course_id: int, announcement_id: int):
    """
    Delete announcement: endpoint untuk menghapus announcement (hanya teacher yang dapat menghapus announcement)
    """
    course = get_object_or_404(Course, id=course_id)
    if course.teacher.id != request.user.id:
        return 403, {"detail": "Only the course teacher can delete announcements."}
        
    announcement = get_object_or_404(CourseAnnouncement, id=announcement_id, course=course)
    announcement.delete()
    return 200, {"detail": "Announcement deleted successfully."}
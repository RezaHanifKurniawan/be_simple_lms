from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404

from lms_core.models import ContentBookmark, CourseContent
from lms_core.schema import ContentBookmarkIn, ContentBookmarkOut, MessageOut
from lms_core.api import apiAuth

bookmark_router = Router(tags=["Bookmark Content"])

@bookmark_router.post("/", auth=apiAuth, response={201: ContentBookmarkOut, 400: MessageOut, 403: MessageOut, 409: MessageOut})
def add_bookmark(request, payload: ContentBookmarkIn):
    """
    Add Bookmark: Student membuat bookmark pada course content yang mereka ikuti.
    """
    user_id = request.user.id
    content = get_object_or_404(CourseContent, id=payload.content_id)
    course = content.course_id

    # Cek apakah user adalah member (student) dari course terkait
    is_member = course.coursemember_set.filter(user_id=user_id).exists()
    if not is_member:
        return 403, {"detail": "You are not a member of this course."}

    # Cek duplikat
    if ContentBookmark.objects.filter(user_id=user_id, content=content).exists():
        return 409, {"detail": "Bookmark already exists."}
    bookmark = ContentBookmark.objects.create(
        user_id=user_id,
        name=payload.name_bookmark,
        content=content
    )
    return 201, bookmark

@bookmark_router.get("/", auth=apiAuth, response=List[ContentBookmarkOut])
def show_bookmarks(request):
    """
    Show Bookmark: Menampilkan semua bookmark milik user, lengkap dengan konten dan course.
    """
    return ContentBookmark.objects.filter(user_id=request.user.id).select_related("content", "content__course_id")

@bookmark_router.delete("/{bookmark_id}", auth=apiAuth, response={200: MessageOut, 403: MessageOut, 404: MessageOut})
def delete_bookmark(request, bookmark_id: int):
    """
    Delete Bookmark: Menghapus bookmark milik user.
    """
    bookmark = ContentBookmark.objects.filter(id=bookmark_id).first()
    if not bookmark:
        return 404, {"detail": "Bookmark not found."}
    if bookmark.user_id != request.user.id:
        return 403, {"detail": "You can only delete your own bookmark."}
    bookmark.delete()
    return 200, {"detail": "Bookmark deleted successfully."}
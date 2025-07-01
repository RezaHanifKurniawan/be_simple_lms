from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404

from lms_core.models import CourseCategory, Course
from lms_core.schema import CourseCategoryIn, CourseCategoryOut, MessageOut
from lms_core.api import apiAuth

category_router = Router(tags=["Course Category"])

@category_router.post("/", auth=apiAuth, response={201: CourseCategoryOut, 400: MessageOut, 403: MessageOut})
def add_category(request, payload: CourseCategoryIn):
    """
    Add Category: Hanya teacher (pengampu course) yang dapat membuat kategori baru.
    """
    user = request.user
    user_id = user.id

    # Cek apakah user adalah teacher pada minimal satu course
    is_teacher = Course.objects.filter(teacher_id=user_id).exists()
    if not is_teacher:
        return 403, {"detail": "Only teacher can add category."}

    if CourseCategory.objects.filter(name=payload.name).exists():
        return 400, {"detail": "Category with this name already exists."}
    category = CourseCategory.objects.create(
        name=payload.name,
        creator_id=user_id
    )
    return 201, category

@category_router.get("/", response=List[CourseCategoryOut])
def show_categories(request):
    """
    Show Category: Menampilkan semua kategori yang pernah dibuat (oleh semua user yang rolenya teacher).
    """
    return CourseCategory.objects.all()

@category_router.delete("/{category_id}", auth=apiAuth, response={200: MessageOut, 403: MessageOut, 404: MessageOut})
def delete_category(request, category_id: int):
    """
    Delete Category: Hanya teacher tersebut yang bisa menghapus kategori yang pernah dibuat.
    """
    category = CourseCategory.objects.filter(id=category_id).first()
    if not category:
        return 404, {"detail": "Category not found."}
    if category.creator_id != request.user.id:
        return 403, {"detail": "Only the creator can delete this category."}
    category.delete()
    return 200, {"detail": "Category deleted successfully."}
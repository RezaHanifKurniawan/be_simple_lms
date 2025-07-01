from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404

from lms_core.models import Course, CourseCategory
from lms_core.schema import CourseSchemaIn, CourseSchemaOut, MessageOut
from lms_core.api import apiAuth

course_router = Router(tags=["Course"])

@course_router.post("/", auth=apiAuth, response={201: CourseSchemaOut, 400: MessageOut, 403: MessageOut})
def create_course(request, payload: CourseSchemaIn):
    """
    Create Course: Hanya user yang sudah menjadi teacher pada minimal satu course yang bisa membuat course baru.
    """
    user_id = request.user.id

    # Cek apakah user adalah teacher pada minimal satu course
    is_teacher = Course.objects.filter(teacher_id=user_id).exists()
    if not is_teacher:
        return 403, {"detail": "Only teacher (pengampu minimal satu course) can create a new course."}

    category = None
    if payload.category:
        category = get_object_or_404(CourseCategory, id=payload.category)
    course = Course.objects.create(
        name=payload.name,
        description=payload.description,
        price=payload.price,
        teacher_id=user_id,
        category=category
    )
    return 201, course

@course_router.get("/", auth=apiAuth, response=List[CourseSchemaOut])
def list_courses(request):
    """
    List Course: Menampilkan semua course yang diikuti atau diajar oleh user.
    """
    user = request.user
    # Course sebagai teacher
    teacher_courses = Course.objects.filter(teacher_id=user.id)
    # Course sebagai student (anggota/member)
    student_courses = Course.objects.filter(coursemember__user_id=user.id)
    # Gabungkan dan hilangkan duplikat
    courses = (teacher_courses | student_courses).distinct()
    return courses

@course_router.get("/{course_id}", auth=apiAuth, response={200: CourseSchemaOut, 403: MessageOut, 404: MessageOut})
def get_course(request, course_id: int):
    """
    Get Course: Menampilkan detail course tertentu.
    Hanya teacher atau member course yang bisa mengakses.
    """
    course = get_object_or_404(Course, id=course_id)
    user = request.user
    # Cek apakah user adalah teacher atau member course
    if course.teacher_id != user.id and not course.coursemember_set.filter(user_id=user.id).exists():
        return 403, {"detail": "You are not allowed to access this course."}
    return 200, course

@course_router.put("/{course_id}", auth=apiAuth, response={200: CourseSchemaOut, 400: MessageOut, 403: MessageOut, 404: MessageOut})
def update_course(request, course_id: int, payload: CourseSchemaIn):
    """
    Update Course: Edit course, kategori boleh null.
    """
    course = get_object_or_404(Course, id=course_id)
    if course.teacher_id != request.user.id:
        return 403, {"detail": "Only the course teacher can edit this course."}
    category = None
    if payload.category:
        category = get_object_or_404(CourseCategory, id=payload.category)
    course.name = payload.name
    course.description = payload.description
    course.price = payload.price
    course.category = category
    course.save()
    return 200, course

@course_router.delete("/{course_id}", auth=apiAuth, response={200: MessageOut, 403: MessageOut, 404: MessageOut})
def delete_course(request, course_id: int):
    """
    Delete Course: Hapus course.
    """
    course = get_object_or_404(Course, id=course_id)
    if course.teacher_id != request.user.id:
        return 403, {"detail": "Only the course teacher can delete this course."}
    course.delete()
    return 200, {"detail": "Course deleted successfully."}
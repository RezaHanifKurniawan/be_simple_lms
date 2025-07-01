from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404

from lms_core.models import Course, CourseFeedback
from lms_core.schema import CourseFeedbackIn, CourseFeedbackOut, MessageOut
from lms_core.api import apiAuth

feedback_router = Router(tags=["Course Feedback"])

@feedback_router.post("/{course_id}/feedbacks", auth=apiAuth, response={201: CourseFeedbackOut, 403: MessageOut, 404: MessageOut})
def add_feedback(request, course_id: int, payload: CourseFeedbackIn):
    """
    Add Feedback: Student dapat menambahkan feedback pada course tertentu.
    Satu student hanya dapat memberikan satu feedback untuk setiap course.
    """
    course = get_object_or_404(Course, id=course_id)
    user_id = request.user.id

    # Cek apakah user adalah member course
    if not course.is_member(user_id):
        return 403, {"detail": "Only course members can add feedback."}

    # Cek apakah user sudah pernah memberi feedback
    if CourseFeedback.objects.filter(course=course, student_id=user_id).exists():
        return 403, {"detail": "You have already submitted feedback for this course."}

    feedback = CourseFeedback.objects.create(course=course, student_id=user_id, feedback=payload.feedback)
    return 201, feedback

@feedback_router.get("/{course_id}/feedbacks", auth=apiAuth, response={200: List[CourseFeedbackOut], 403: MessageOut, 404: MessageOut})
def show_feedback(request, course_id: int):
    """
    Show Feedback: Menampilkan semua feedback pada course tertentu.
    Hanya teacher dan member course yang dapat melihat feedback.
    """
    course = get_object_or_404(Course, id=course_id)
    user_id = request.user.id
    # Hanya teacher dan member yang bisa melihat feedback
    if not course.is_member(user_id) and course.teacher.id != user_id:
        return 403, {"detail": "You are not allowed to see feedback for this course."}
    feedbacks = CourseFeedback.objects.filter(course=course)
    return 200, feedbacks

@feedback_router.put("/{course_id}/feedbacks/{feedback_id}", auth=apiAuth, response={200: CourseFeedbackOut, 403: MessageOut, 404: MessageOut})
def edit_feedback(request, course_id: int, feedback_id: int, payload: CourseFeedbackIn):
    """
    Edit Feedback: Student dapat mengedit feedback yang sudah ditulisnya pada course tertentu.
    """
    course = get_object_or_404(Course, id=course_id)
    user_id = request.user.id
    feedback = get_object_or_404(CourseFeedback, id=feedback_id, course=course)
    # Hanya student yang menulis feedback yang bisa mengedit
    if feedback.student_id != user_id:
        return 403, {"detail": "You can only edit your own feedback."}
    feedback.feedback = payload.feedback
    feedback.save()
    return 200, feedback

@feedback_router.delete("/{course_id}/feedbacks/{feedback_id}", auth=apiAuth, response={200: MessageOut, 403: MessageOut, 404: MessageOut})
def delete_feedback(request, course_id: int, feedback_id: int):
    """
    Delete Feedback: Student dapat menghapus feedback yang sudah ditulisnya pada course tertentu.
    """
    course = get_object_or_404(Course, id=course_id)
    user_id = request.user.id
    feedback = get_object_or_404(CourseFeedback, id=feedback_id, course=course)
    # Hanya student yang menulis feedback yang bisa menghapus
    if feedback.student_id != user_id:
        return 403, {"detail": "You can only delete your own feedback."}
    feedback.delete()
    return 200, {"detail": "Feedback deleted successfully."}
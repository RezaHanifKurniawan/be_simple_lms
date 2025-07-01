from ninja import Router
from lms_core.schema import UserOut
from lms_core.models import Course, CourseMember
from lms_core.api import apiAuth

# 1. Buat instance Router baru
user_router = Router(tags=["User"])


@user_router.get("/me", auth=apiAuth, response=UserOut, tags=["User"])
def me(request):
    """
    Mengambil data untuk pengguna yang saat ini login.
    """
    user = request.user
    user_role = None  # Default role

    # Cek apakah pengguna adalah seorang pengajar di mata kuliah manapun
    if Course.objects.filter(teacher=user.id).exists():
        user_role = "teacher"
    # Jika bukan pengajar, cek apakah dia adalah siswa di mata kuliah manapun
    elif CourseMember.objects.filter(user_id=user.id).exists():
        user_role = "student"

    # Gabungkan data pengguna dengan peran tunggalnya
    user_data = {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user_role
    }
    
    return user_data
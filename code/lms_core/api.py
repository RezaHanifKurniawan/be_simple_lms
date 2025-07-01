from ninja import NinjaAPI
from ninja_simple_jwt.auth.views.api import mobile_auth_router
from ninja_simple_jwt.auth.ninja_auth import HttpJwtAuth


apiv1 = NinjaAPI()
apiAuth = HttpJwtAuth()

from lms_core.routers.user import user_router
from lms_core.routers.course import course_router
from lms_core.routers.course_announce import announcement_router
from lms_core.routers.course_feedback import feedback_router
from lms_core.routers.course_category import category_router
from lms_core.routers.bookmark import bookmark_router


apiv1.add_router("/auth/", mobile_auth_router)
apiv1.add_router("/user/", user_router)
apiv1.add_router("/courses/", course_router)
apiv1.add_router("/courses/", announcement_router)
apiv1.add_router("/courses/", feedback_router)
apiv1.add_router("/categories/", category_router)
apiv1.add_router("/bookmarks/", bookmark_router)
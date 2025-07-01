from ninja import Schema
from typing import Optional, List
from datetime import datetime

from django.contrib.auth.models import User

#==== USER SCHEMA ==== #
class UserMiniOut(Schema):
    id: int
    email: str
    first_name: str
    last_name: str

class UserOut(Schema):
    id: int
    email: str
    first_name: str
    last_name: str
    role: Optional[str]
#==== END OF USER SCHEMA ==== #

    
# ==== CATEGORY SCHEMA ==== #
class CourseCategoryIn(Schema):
    name: str

class CourseCategoryOut(Schema):
    id: int
    name: str
    creator_id: int
    created_at: datetime
# ==== END CATEGORY SCHEMA ==== #


class CourseSchemaOut(Schema):
    id: int
    name: str
    description: str
    price: int
    image : Optional[str]
    teacher: UserMiniOut
    category: Optional[CourseCategoryOut] = None
    created_at: datetime
    updated_at: datetime

class CourseMemberOut(Schema):
    id: int 
    course_id: CourseSchemaOut
    user_id: UserOut
    roles: str
    # created_at: datetime


class CourseSchemaIn(Schema):
    name: str
    description: str
    price: int
    category: Optional[int] = None


class CourseContentMini(Schema):
    id: int
    name: str
    description: str
    course_id: CourseSchemaOut
    created_at: datetime
    updated_at: datetime


class CourseContentFull(Schema):
    id: int
    name: str
    description: str
    video_url: Optional[str]
    file_attachment: Optional[str]
    course_id: CourseSchemaOut
    created_at: datetime
    updated_at: datetime

class CourseCommentOut(Schema):
    id: int
    content_id: CourseContentMini
    member_id: CourseMemberOut
    comment: str
    created_at: datetime
    updated_at: datetime

class CourseCommentIn(Schema):
    comment: str
    
#===== SCHEMA UNTUK MESSAGE PADA RESPONSE =====#     
class MessageOut(Schema):
    detail: str
#===== END OF SCHEMA UNTUK MESSAGE PADA RESPONSE =====#

    
#==== SCHEMA UNTUK COURSE ANNOUNCEMENT ====#
# schema untuk add announcement
class CourseAnnouncementIn(Schema):
    title: str
    content: str
    show_at: datetime

# schema untuk response announcement/output
class CourseAnnouncementOut(Schema):
    id: int
    title: str
    content: str
    show_at: datetime
    course_id: int
    created_at: datetime
    updated_at: datetime
    
# schema untuk update announcement + message
class CourseAnnouncementUpdateOut(MessageOut):
    announcement: CourseAnnouncementOut
#==== END OF SCHEMA UNTUK COURSE ANNOUNCEMENT ====#


#==== SCHEMA UNTUK COURSE FEEDBACK ====#
# schema untuk add feedback
class CourseFeedbackIn(Schema):
    feedback: str

# schema untuk response feedback/output
class CourseFeedbackOut(Schema):
    id: int
    course_id: int
    student_id: int
    feedback: str
    created_at: datetime
    updated_at: datetime
    
# schema untuk update feedback + message
class CourseFeedbackUpdateOut(MessageOut):
    feedback: CourseFeedbackOut
#==== END OF SCHEMA UNTUK COURSE FEEDBACK ====#

#==== SCHEMA UNTUK CONTENT BOOKMARK ====#
class ContentBookmarkIn(Schema):
    content_id: int
    name_bookmark: str  # nama bookmark

class ContentBookmarkOut(Schema):
    id: int
    name: str
    content: CourseContentFull
    user: UserMiniOut
    created_at: datetime
#==== END OF SCHEMA UNTUK CONTENT BOOKMARK ====#
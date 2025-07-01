# Daftar Fitur & Endpoint SimpleLMS

---

## 1. **Authentication & User**

### - **Login**
`POST /auth/login/`  
*Untuk login dan mendapatkan token JWT.*

### - **Get Current User**
`GET /user/me`  
*Mengambil data untuk pengguna yang saat ini login.*

---

## 2. **Course Management**

### - **List Course**
`GET /courses/`  
*Menampilkan semua course yang diikuti atau diajar oleh user yang sedang login.*

### - **Create Course**
`POST /courses/`  
*Menambah course baru (hanya teacher yang sudah pernah mengajar minimal satu course).*

### - **Get Course Detail**
`GET /courses/{course_id}`  
*Menampilkan detail course tertentu (hanya teacher atau member course yang bisa akses).*

### - **Update Course**
`PUT /courses/{course_id}`  
*Edit course (hanya teacher pemilik course).*

### - **Delete Course**
`DELETE /courses/{course_id}`  
*Hapus course (hanya teacher pemilik course).*

---

## 3. **Course Category Management**

### - **List Categories**
`GET /categories/`  
*Menampilkan semua kategori yang pernah dibuat oleh semua teacher.*

### - **Add Category**
`POST /categories/`  
*Menambah kategori baru (hanya teacher yang sudah pernah mengajar minimal satu course).*

### - **Delete Category**
`DELETE /categories/{category_id}`  
*Menghapus kategori yang pernah dibuat oleh teacher tersebut.*

---

## 4. **Course Announcement**

### - **List Announcements**
`GET /courses/{course_id}/announcements`  
*Menampilkan semua pengumuman pada course tertentu (teacher dan member course dapat melihat).*

### - **Add Announcement**
`POST /courses/{course_id}/announcements`  
*Menambah pengumuman pada course tertentu (hanya teacher pemilik course).*

### - **Update Announcement**
`PUT /courses/{course_id}/announcements/{announcement_id}`  
*Edit announcement (hanya teacher pemilik course).*

### - **Delete Announcement**
`DELETE /courses/{course_id}/announcements/{announcement_id}`  
*Hapus announcement (hanya teacher pemilik course).*

---

## 5. **Course Feedback**

### - **List Feedback**
`GET /courses/{course_id}/feedbacks`  
*Menampilkan semua feedback pada course tertentu (hanya teacher dan member course).*

### - **Add Feedback**
`POST /courses/{course_id}/feedbacks`  
*Student dapat menambahkan feedback pada course tertentu (hanya satu feedback per student per course).*

### - **Update Feedback**
`PUT /courses/{course_id}/feedbacks/{feedback_id}`  
*Student dapat mengedit feedback yang sudah ditulisnya.*

### - **Delete Feedback**
`DELETE /courses/{course_id}/feedbacks/{feedback_id}`  
*Student dapat menghapus feedback yang sudah ditulisnya.*

---

## 6. **Content Bookmarking**

### - **List Bookmarks**
`GET /bookmarks/`  
*Menampilkan semua bookmark milik user, lengkap dengan konten dan course.*

### - **Add Bookmark**
`POST /bookmarks/`  
*Student membuat bookmark pada course content yang mereka ikuti.*

### - **Delete Bookmark**
`DELETE /bookmarks/{bookmark_id}`  
*Menghapus bookmark milik user.*

---

**Catatan:**  
- Semua endpoint yang membutuhkan autentikasi harus mengirim header:  
  `Authorization: Bearer <token>`
- Endpoint `/courses/` juga digunakan untuk announcement & feedback (prefix sama, path berbeda).

---
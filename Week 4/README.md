Phân công công việc:

- Nguyễn Hải An
  Tổng hợp thông tin, thiết kế tổng quan app.py, xây dựng endpoint GET /books, POST /books
- Bùi Hoàng Tùng
  Xây dựng endpoint GET /books/{bookId}
- Trần Duy Thường
  Xây dựng endpoint PUT /books/{bookId}
- Lưu Việt Dũng
  Xây dựng endpoint PATCH /books/{bookId}
- Lê Khánh Hưng
  Xây dựng endpoint DELETE /books/{bookId}

Do vấn đề thời gian và thiếu kinh nghiệm xây dựng, trong app.py nhóm đã không xây dựng hết các status code, chưa thiết kế filtering, sorting, pagination cũng chưa xây dựng được cách sử dụng bearerAuth được đặc tả trong openapi.yaml.

0. Tổ chức files

- app.py: Sourcecode nội bộ của hệ thống quản lý sách.
- bookmanagingLITE.yaml: OpenAPI đặc tả cho hệ thống HIỆN THỜI, là API app.py sử dụng.
- bookmanaging.yaml: OpenAPI đặc tả đầy đủ của hệ thống, chứa filtering, sorting, pagination, authentication token.
- /SwaggerUI: Folder chứa thông tin 'Try It Out' thông qua Swagger UI.

1. Các endpoints sử dụng

- GET /books
- POST /books
- GET /books/{bookId}
- PUT /books/{bookId}
- PATCH /books/{bookId}
- DELETE /books/{bookId}

2. Swagger UI - 'Try It Out'

- GET /books:
  - 200:
    [GET/books200](SwaggerUI/get_books200.png)
- POST /books:
  - 201:
    [POST/books201](SwaggerUI/post_books201.png)
  - 400:
    [POST/books400](SwaggerUI/post_books400.png)
  - 409:
    [POST/books409](SwaggerUI/post_books409.png)
  - 422:
    [POST/books422](SwaggerUI/post_books422.png)

- GET /books/{bookId}:
  - 200:
    [GET/books_bookId200](SwaggerUI/get_books_bookId200.png)
  - 404:
    [GET/books_bookId404](SwaggerUI/get_books_bookId404.png)

- PUT /books/{bookId}:
  - 200:
    [PUT/books_bookId200](SwaggerUI/put_books_bookId200.png)
  - 400:
    [PUT/books_bookId400](SwaggerUI/put_books_bookId400.png)
  - 404:
    [PUT/books_bookId404](SwaggerUI/put_books_bookId404.png)
  - 422:
    [PUT/books_bookId422](SwaggerUI/put_books_bookId422.png)

- PATCH /books/{bookId}:
  - 200:
    [PATCH/books_bookId200](SwaggerUI/patch_books_bookId200.png)
  - 400:
    [PATCH/books_bookId400](SwaggerUI/patch_books_bookId400.png)
  - 404:
    [PATCH/books_bookId404](SwaggerUI/patch_books_bookId404.png)
  - 422:
    [PATCH/books_bookId422](SwaggerUI/patch_books_bookId422.png)

- DELETE /books/{bookId}:
  - 204:
    [DELETE/books_bookId204](SwaggerUI/delete_books_bookId204.png)
  - 404:
    [DELETE/books_bookId404](SwaggerUI/delete_books_bookId404.png)

3. Hai quyết định thiết kế khó nhất.

- Lựa chọn giữa trả về 200 hay 204 cho DELETE
  204 được đánh giá là tiêu chuẩn công nghiệp khi ta muốn thông báo client rẳng server đẫ delete resource thành công. Tuy nhiên, status code này sẽ không trả về response nào, và khi trong quá trình kiểm thử, ta thường muốn server trả về kết quả nào đó, và hầu như trả về sẽ tốt hơn là không trả những gì. Cuối cùng, nhóm đã kết luận nên theo tiêu chuẩn và sử dung 204 + No Content
- Phân tích sử dụng và phân biệt giữa 400 và 422
  Việc xác định ranh giới giữa invalid format và invalid request information là rất quan trọng trong quá trình trả về kết quả cho client. Việc không định nghĩa rõ ràng sẽ ảnh hưởng đến cả người sử dụng lẫn người xây dựng nên nhóm đã định nghĩa các status code phù hợp cho các method nào, kiểm duyệt ổn định mới bắt đầu xây dựng

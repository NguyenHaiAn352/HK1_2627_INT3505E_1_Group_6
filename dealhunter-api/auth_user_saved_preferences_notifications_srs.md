# Auth, User, Saved Vouchers, Preferences & Notifications --- SRS

## 1. Mục đích và phạm vi

Tài liệu mô tả yêu cầu chức năng và luồng xử lý cho 5 nhóm chức năng của
DealHunter:

-   **Auth:** đăng ký, đăng nhập, làm mới và đăng xuất.
-   **User:** xem và cập nhật hồ sơ cá nhân.
-   **Saved Vouchers:** lưu và bỏ lưu voucher.
-   **Preferences:** quản lý tiêu chí nhận gợi ý/thông báo voucher.
-   **Notifications:** xem và quản lý thông báo.

Tài liệu tập trung vào hành vi hệ thống và xác thực. Chi tiết triển khai
có thể được điều chỉnh theo thiết kế API và database cuối cùng.

## 2. Actors

  -----------------------------------------------------------------------
  Actor                               Mô tả
  ----------------------------------- -----------------------------------
  Guest                               Người chưa đăng nhập; có thể đăng
                                      ký và đăng nhập.

  User                                Người dùng đã xác thực; quản lý hồ
                                      sơ, voucher đã lưu, preferences và
                                      notifications của chính mình.

  Admin                               Người quản trị; quyền quản trị được
                                      kiểm soát bằng role.
  -----------------------------------------------------------------------

## 3. Functional Requirements

### 3.1. Authentication (Auth)

  -----------------------------------------------------------------------
  ID                                  Requirement
  ----------------------------------- -----------------------------------
  FR-AUTH-01                          Hệ thống cho phép người dùng đăng
                                      ký tài khoản với thông tin hợp lệ.

  FR-AUTH-02                          Hệ thống kiểm tra username/email
                                      không bị trùng.

  FR-AUTH-03                          Mật khẩu phải được băm trước khi
                                      lưu vào database; không lưu mật
                                      khẩu dạng plaintext.

  FR-AUTH-04                          Người dùng có thể đăng nhập bằng
                                      thông tin định danh và mật khẩu hợp
                                      lệ.

  FR-AUTH-05                          Khi đăng nhập thành công, hệ thống
                                      cấp Access Token và Refresh Token.

  FR-AUTH-06                          Access Token được dùng để xác thực
                                      các request cần đăng nhập.

  FR-AUTH-07                          Refresh Token được dùng để cấp
                                      token mới khi Access Token hết hạn.

  FR-AUTH-08                          Hệ thống lưu hash của Refresh
                                      Token, không lưu token gốc.

  FR-AUTH-09                          Khi refresh thành công, Refresh
                                      Token cũ bị thu hồi và token mới
                                      được cấp (token rotation).

  FR-AUTH-10                          Người dùng có thể đăng xuất;
                                      Refresh Token của phiên hiện tại bị
                                      thu hồi.

  FR-AUTH-11                          Hệ thống hỗ trợ xác thực bằng
                                      Bearer Token trong HTTP Header và
                                      bằng Cookie cho trình duyệt.

  FR-AUTH-12                          Với request thay đổi dữ liệu sử
                                      dụng Cookie, hệ thống yêu cầu CSRF
                                      token.

  FR-AUTH-13                          Hệ thống phân quyền theo role, tối
                                      thiểu gồm USER và ADMIN.
  -----------------------------------------------------------------------

### 3.2. User

  -----------------------------------------------------------------------
  ID                                  Requirement
  ----------------------------------- -----------------------------------
  FR-USER-01                          Người dùng đã đăng nhập có thể xem
                                      hồ sơ của chính mình.

  FR-USER-02                          Người dùng có thể cập nhật các
                                      trường hồ sơ được phép chỉnh sửa.

  FR-USER-03                          Danh tính người dùng được xác định
                                      từ token, không lấy `user_id` tùy ý
                                      từ request để truy cập hồ sơ cá
                                      nhân.

  FR-USER-04                          Hệ thống kiểm tra tính hợp lệ và
                                      tính duy nhất của các trường cần
                                      unique khi cập nhật.
  -----------------------------------------------------------------------

### 3.3. Saved Vouchers

  -----------------------------------------------------------------------
  ID                                  Requirement
  ----------------------------------- -----------------------------------
  FR-SAVED-01                         Người dùng có thể xem danh sách
                                      voucher đã lưu của mình.

  FR-SAVED-02                         Người dùng có thể lưu một voucher
                                      hợp lệ.

  FR-SAVED-03                         Hệ thống không tạo bản ghi lưu
                                      trùng cho cùng một cặp
                                      user-voucher.

  FR-SAVED-04                         Người dùng có thể bỏ lưu voucher.

  FR-SAVED-05                         Người dùng chỉ được xem, thêm hoặc
                                      xóa các bản ghi lưu thuộc tài khoản
                                      của mình.
  -----------------------------------------------------------------------

### 3.4. Preferences

  -----------------------------------------------------------------------
  ID                                  Requirement
  ----------------------------------- -----------------------------------
  FR-PREF-01                          Người dùng có thể xem danh sách
                                      preferences của mình.

  FR-PREF-02                          Người dùng có thể tạo preference áp
                                      dụng cho một platform cụ thể.

  FR-PREF-03                          Người dùng có thể tạo preference áp
                                      dụng cho tất cả platform bằng
                                      `platform_id = null`.

  FR-PREF-04                          Preference có thể cấu hình các tiêu
                                      chí như mức giảm giá tối thiểu và
                                      giá trị đơn hàng tối thiểu.

  FR-PREF-05                          Người dùng có thể cập nhật hoặc xóa
                                      preference của mình.

  FR-PREF-06                          Preference có trạng thái bật/tắt;
                                      chỉ preference đang bật được dùng
                                      khi tìm voucher phù hợp.

  FR-PREF-07                          Người dùng không được chỉnh sửa
                                      hoặc xóa preference thuộc tài khoản
                                      khác.
  -----------------------------------------------------------------------

### 3.5. Notifications

  -----------------------------------------------------------------------
  ID                                  Requirement
  ----------------------------------- -----------------------------------
  FR-NOTIF-01                         Người dùng có thể xem danh sách
                                      thông báo của mình.

  FR-NOTIF-02                         Danh sách thông báo hỗ trợ phân
                                      trang và lọc theo trạng thái đã
                                      đọc/chưa đọc.

  FR-NOTIF-03                         Người dùng có thể đánh dấu một
                                      thông báo là đã đọc.

  FR-NOTIF-04                         Người dùng có thể đánh dấu tất cả
                                      thông báo là đã đọc.

  FR-NOTIF-05                         Hệ thống hỗ trợ các loại thông báo
                                      `NEW_MATCH` và `DEAL_IMPROVED`.

  FR-NOTIF-06                         Hệ thống tránh tạo thông báo trùng
                                      cho cùng user, voucher và loại
                                      thông báo.

  FR-NOTIF-07                         Người dùng chỉ được xem và cập nhật
                                      thông báo thuộc tài khoản của mình.
  -----------------------------------------------------------------------

## 4. Use Case Specifications

### UC-AUTH-01 --- Register

-   **Actor:** Guest.
-   **Precondition:** Người dùng chưa có tài khoản với username/email đã
    đăng ký.
-   **Main flow:**
    1.  Người dùng gửi thông tin đăng ký.
    2.  Hệ thống kiểm tra dữ liệu đầu vào.
    3.  Hệ thống kiểm tra username/email đã tồn tại hay chưa.
    4.  Hệ thống băm mật khẩu và tạo tài khoản.
    5.  Hệ thống trả về kết quả đăng ký thành công.
-   **Alternative flow:** Dữ liệu không hợp lệ hoặc username/email đã
    tồn tại; hệ thống trả lỗi tương ứng.

### UC-AUTH-02 --- Login

-   **Actor:** Guest.
-   **Precondition:** Tài khoản tồn tại và hợp lệ.
-   **Main flow:**
    1.  Người dùng gửi thông tin đăng nhập.
    2.  Hệ thống tìm tài khoản và kiểm tra mật khẩu.
    3.  Hệ thống tạo Access Token và Refresh Token.
    4.  Hệ thống trả token cho API client hoặc thiết lập Cookie cho
        trình duyệt.
-   **Alternative flow:** Sai thông tin đăng nhập; hệ thống trả lỗi xác
    thực.

### UC-AUTH-03 --- Refresh Token

-   **Actor:** User / API client có Refresh Token.
-   **Main flow:**
    1.  Client gửi Refresh Token.
    2.  Hệ thống kiểm tra chữ ký, hạn sử dụng và trạng thái token.
    3.  Hệ thống đối chiếu hash token với bản ghi trong database.
    4.  Hệ thống thu hồi token cũ và cấp cặp token mới.
    5.  Hệ thống trả token mới hoặc cập nhật Cookie.
-   **Alternative flow:** Token không hợp lệ, hết hạn hoặc đã bị thu
    hồi; hệ thống từ chối và yêu cầu đăng nhập lại.

### UC-AUTH-04 --- Logout

-   **Actor:** User.
-   **Main flow:**
    1.  Người dùng gửi yêu cầu đăng xuất.
    2.  Hệ thống xác định Refresh Token của phiên hiện tại.
    3.  Hệ thống thu hồi token và xóa Cookie nếu dùng Cookie.
    4.  Hệ thống trả kết quả đăng xuất.

### UC-USER-01 --- View / Update Profile

-   **Actor:** User.
-   **Main flow:** Người dùng yêu cầu xem hoặc cập nhật hồ sơ; hệ thống
    xác định user từ token, kiểm tra dữ liệu và trả kết quả.
-   **Alternative flow:** Dữ liệu cập nhật không hợp lệ hoặc vi phạm
    unique constraint; hệ thống trả lỗi.

### UC-SAVED-01 --- Manage Saved Vouchers

-   **Actor:** User.
-   **Main flow:** Người dùng xem danh sách, lưu hoặc bỏ lưu voucher. Hệ
    thống kiểm tra voucher tồn tại và bảo đảm thao tác chỉ áp dụng cho
    user hiện tại.
-   **Alternative flow:** Voucher không tồn tại hoặc đã được lưu; hệ
    thống trả kết quả/lỗi phù hợp và không tạo dữ liệu trùng.

### UC-PREF-01 --- Manage Preferences

-   **Actor:** User.
-   **Main flow:** Người dùng xem, tạo, cập nhật hoặc xóa preference. Hệ
    thống kiểm tra quyền sở hữu và dữ liệu cấu hình.
-   **Business rule:** `platform_id = null` biểu thị preference áp dụng
    cho tất cả platform; preference không hoạt động sẽ không được dùng
    để đối chiếu voucher.

### UC-NOTIF-01 --- Manage Notifications

-   **Actor:** User.
-   **Main flow:** Người dùng xem danh sách thông báo, lọc/phân trang và
    đánh dấu một hoặc tất cả thông báo là đã đọc.
-   **Alternative flow:** Thông báo không tồn tại hoặc không thuộc user
    hiện tại; hệ thống từ chối thao tác.

## 5. API Endpoint Proposal

Các endpoint dưới đây là đề xuất cho API phiên bản `v1`.

  ------------------------------------------------------------------------------------------------
  Method                  Endpoint                                         Mô tả
  ----------------------- ------------------------------------------------ -----------------------
  POST                    `/api/v1/auth/register`                          Đăng ký

  POST                    `/api/v1/auth/login`                             Đăng nhập

  POST                    `/api/v1/auth/refresh`                           Làm mới token

  POST                    `/api/v1/auth/logout`                            Đăng xuất

  GET                     `/api/v1/users/me`                               Xem hồ sơ

  PATCH                   `/api/v1/users/me`                               Cập nhật hồ sơ

  GET                     `/api/v1/users/me/saved-vouchers`                Danh sách voucher đã
                                                                           lưu

  POST                    `/api/v1/users/me/saved-vouchers`                Lưu voucher

  DELETE                  `/api/v1/users/me/saved-vouchers/{voucher_id}`   Bỏ lưu voucher

  GET                     `/api/v1/users/me/preferences`                   Danh sách preferences

  POST                    `/api/v1/users/me/preferences`                   Tạo preference

  PATCH                   `/api/v1/users/me/preferences/{id}`              Cập nhật preference

  DELETE                  `/api/v1/users/me/preferences/{id}`              Xóa preference

  GET                     `/api/v1/notifications`                          Danh sách thông báo

  PATCH                   `/api/v1/notifications/{id}/read`                Đánh dấu đã đọc

  PATCH                   `/api/v1/notifications/read-all`                 Đánh dấu tất cả đã đọc
  ------------------------------------------------------------------------------------------------

## 6. Dual Authentication: Header và Cookie/CSRF

Hệ thống hỗ trợ hai cách truyền token tùy theo loại client. Đây là hai
phương thức thay thế nhau theo từng client, không có nghĩa mọi request
phải gửi đồng thời Header và Cookie.

### 6.1. Header Authentication

Dùng cho Postman hoặc API client:

``` http
Authorization: Bearer <access_token>
```

-   Client chủ động đính kèm token vào request.
-   Các request xác thực không dựa vào Cookie tự động gửi của trình
    duyệt nên thông thường không cần CSRF token.
-   Refresh Token được gửi tới endpoint refresh theo cơ chế thống nhất
    của API.

### 6.2. Cookie Authentication

Dùng cho giao diện web chạy trên trình duyệt:

-   Access Token và Refresh Token được đặt trong Cookie `HttpOnly`.
-   Cookie production nên bật `Secure` và cấu hình `SameSite` phù hợp.
-   Với request làm thay đổi dữ liệu (`POST`, `PUT`, `PATCH`, `DELETE`),
    client phải gửi CSRF token theo cấu hình server.
-   Khi logout, server thu hồi Refresh Token và xóa các Cookie liên
    quan.

**Lưu ý triển khai:** Cần cấu hình rõ tên CSRF cookie/header trong
Flask-JWT-Extended và kiểm tra cả CSRF cho access cookie lẫn refresh
cookie nếu refresh được thực hiện bằng Cookie. Không nên để một request
gửi đồng thời hai access token khác nhau qua Header và Cookie nếu chưa
định nghĩa quy tắc ưu tiên.

## 7. Sequence Diagrams

### 7.1. Login

``` mermaid
sequenceDiagram
    actor Client
    participant API
    participant UserDB as User Database
    participant TokenDB as Refresh Token Database

    Client->>API: POST /api/v1/auth/login
    API->>UserDB: Find user by identifier
    UserDB-->>API: User + password hash
    API->>API: Verify password
    alt Credentials valid
        API->>API: Generate Access Token + Refresh Token
        API->>TokenDB: Store hash of Refresh Token
        TokenDB-->>API: Saved
        API-->>Client: Tokens (API client) / HttpOnly Cookies (Browser)
    else Credentials invalid
        API-->>Client: 401 Unauthorized
    end
```

### 7.2. Refresh Token

``` mermaid
sequenceDiagram
    actor Client
    participant API
    participant TokenDB as Refresh Token Database

    Client->>API: POST /api/v1/auth/refresh
    API->>API: Validate Refresh Token
    API->>API: Hash received token
    API->>TokenDB: Find matching token record
    TokenDB-->>API: Token record
    alt Token valid and not revoked
        API->>TokenDB: Revoke old token
        API->>API: Generate new Access Token + Refresh Token
        API->>TokenDB: Store hash of new Refresh Token
        TokenDB-->>API: Saved
        API-->>Client: New tokens / Updated Cookies
    else Invalid, expired or revoked
        API-->>Client: 401 Unauthorized
    end
```

**Yêu cầu triển khai:** Việc thu hồi Refresh Token cũ và lưu token mới
nên được thực hiện trong cùng transaction để tránh hai request refresh
đồng thời sử dụng lại một token.

## 8. Security and Validation Rules

-   Không lưu mật khẩu hoặc Refresh Token dạng plaintext.
-   Access Token phải có thời hạn; Refresh Token phải có thời hạn và cơ
    chế thu hồi.
-   Kiểm tra chữ ký, loại token và hạn sử dụng trước khi chấp nhận
    token.
-   Với tài nguyên thuộc người dùng, luôn kiểm tra cả ID tài nguyên và
    user hiện tại để tránh truy cập chéo tài khoản (IDOR).
-   Kiểm tra dữ liệu đầu vào và trả lỗi nhất quán.
-   Chỉ cho phép ADMIN truy cập các chức năng quản trị.
-   Cookie-based unsafe requests phải được bảo vệ bằng CSRF.
-   Refresh rotation cần xử lý transaction và trường hợp request đồng
    thời.

## 9. Acceptance Tests

  ---------------------------------------------------------------------------------
  ID                      Test scenario                     Expected result
  ----------------------- --------------------------------- -----------------------
  AT-01                   Đăng ký với dữ liệu hợp lệ        Tạo tài khoản thành
                                                            công

  AT-02                   Đăng ký username/email đã tồn tại Trả lỗi
                                                            conflict/validation

  AT-03                   Đăng nhập sai mật khẩu            Trả `401 Unauthorized`

  AT-04                   Gọi API bằng Access Token hợp lệ  Cho phép nếu đủ quyền
                          trong Header                      

  AT-05                   Gọi API cần đăng nhập không có    Trả `401 Unauthorized`
                          token                             

  AT-06                   Cookie request thay đổi dữ liệu   Từ chối request
                          thiếu/sai CSRF token              

  AT-07                   Refresh bằng token hợp lệ         Cấp token mới và thu
                                                            hồi token cũ

  AT-08                   Dùng lại Refresh Token đã thu hồi Từ chối request

  AT-09                   User truy cập saved               Từ chối truy cập
                          voucher/preference/notification   
                          của user khác                     

  AT-10                   Lưu cùng một voucher nhiều lần    Không tạo bản ghi trùng

  AT-11                   Đánh dấu thông báo đã đọc         Trạng thái thông báo
                                                            được cập nhật
  ---------------------------------------------------------------------------------

## 10. Decisions to Confirm

Các điểm dưới đây cần nhóm thống nhất trước khi triển khai:

1.  Đăng nhập bằng username, email hay cả hai.
2.  Các trường nào của hồ sơ User được phép cập nhật.
3.  Refresh Token của API client gửi qua JSON body hay cơ chế khác;
    trình duyệt dùng HttpOnly Cookie.
4.  Logout chỉ thu hồi Refresh Token của phiên hiện tại hay cần cơ chế
    thu hồi Access Token ngay lập tức.
5.  Có cho phép nhiều phiên đăng nhập đồng thời trên nhiều thiết bị hay
    không.
6.  Thời hạn Access Token và Refresh Token sẽ được chốt trong cấu hình
    bảo mật.

------------------------------------------------------------------------

**Ghi chú:** Endpoint, thời hạn token, tên trường request và một số quy
tắc bảo mật trong tài liệu này là đề xuất thiết kế để nhóm xác nhận; cần
đồng bộ với ERD, OpenAPI và code thực tế trước khi triển khai.

# Backend API Documentation

## Base Configuration

```
BASE_URL: Your backend server URL
TOKEN: JWT token obtained from login
```

## Authentication Endpoints

### 1. Root Health Check

```http
GET {{BASE_URL}}/
```

**Description:** Check if the API server is running

**Response:** Basic server status

---

### 2. User Registration

```http
POST {{BASE_URL}}/api/auth/register
Content-Type: application/json
```

**Request Body:**

```json
{
  "email": "user@mail.com",
  "password": "123456",
  "role": "petani"
}
```

**Description:** Register a new user account

**Parameters:**

- `email` (string): User's email address
- `password` (string): User's password
- `role` (string): User role (e.g., "petani")

---

### 3. User Login

```http
POST {{BASE_URL}}/api/auth/login
Content-Type: application/json
```

**Request Body:**

```json
{
  "email": "user@mail.com",
  "password": "123456"
}
```

**Description:** Authenticate user and receive JWT token

**Parameters:**

- `email` (string): User's email address
- `password` (string): User's password

**Response:** JWT token for authorization

---

## Agricultural Services

### 4. Harvest Calculator

```http
POST {{BASE_URL}}/api/harvest/calculate
Content-Type: application/json
```

**Request Body:**

```json
{
  "crop_type": "padi",
  "area": 2
}
```

**Description:** Calculate harvest estimation based on crop type and area

**Parameters:**

- `crop_type` (string): Type of crop (e.g., "padi")
- `area` (number): Area in hectares or relevant unit

---

### 5. Plant Disease Detection

```http
POST {{BASE_URL}}/api/plant/detect
Authorization: Bearer {{TOKEN}}
Content-Type: multipart/form-data
```

**Form Data:**

- `image`: Image file of plant leaf for analysis

**Description:** Detect plant diseases from uploaded leaf images using AI

**Requirements:**

- Valid JWT token
- Image file (JPG, PNG format recommended)

---

### 6. Planting Recommendations

```http
GET {{BASE_URL}}/api/planting/recommend?lat=-6.2&lon=106.8
Authorization: Bearer {{TOKEN}}
```

**Query Parameters:**

- `lat` (number): Latitude coordinate
- `lon` (number): Longitude coordinate

**Description:** Get planting recommendations based on location and weather conditions

**Requirements:** Valid JWT token

---

## E-commerce Endpoints

### 7. Products List

```http
GET {{BASE_URL}}/api/ecommerce/products
Authorization: Bearer {{TOKEN}}
```

**Description:** Retrieve list of all available products

**Requirements:** Valid JWT token

---

### 8. Add New Product

```http
POST {{BASE_URL}}/api/ecommerce/sell
Authorization: Bearer {{TOKEN}}
Content-Type: multipart/form-data
```

**Form Data:**

- `name`: Product name (e.g., "Cabai")
- `price`: Product price (e.g., "25000")
- `description`: Product description (e.g., "Segar")
- `image`: Product image file

**Description:** Add a new product for sale

**Requirements:**

- Valid JWT token
- All form fields are required

---

## Educational Content

### 9. Articles List

```http
GET {{BASE_URL}}/api/education/articles
Authorization: Bearer {{TOKEN}}
```

**Description:** Retrieve list of educational articles

**Requirements:** Valid JWT token

---

### 10. Upload Article

```http
POST {{BASE_URL}}/api/education/articles/upload
Authorization: Bearer {{TOKEN}}
Content-Type: multipart/form-data
```

**Form Data:**

- `title`: Article title (e.g., "Pupuk Organik")
- `content`: Article content (e.g., "Lorem ipsum dolor sit amet")
- `image`: Thumbnail image file

**Description:** Upload new educational article

**Requirements:**

- Valid JWT token
- All form fields are required

---

### 11. Videos List

```http
GET {{BASE_URL}}/api/education/videos
Authorization: Bearer {{TOKEN}}
```

**Description:** Retrieve list of educational videos

**Requirements:** Valid JWT token

---

### 12. Upload Video

```http
POST {{BASE_URL}}/api/education/videos/upload
Authorization: Bearer {{TOKEN}}
Content-Type: multipart/form-data
```

**Form Data:**

- `title`: Video title (e.g., "Tutorial")
- `description`: Video description (e.g., "Step by step")
- `video`: Video file (MP4 format recommended)

**Description:** Upload new educational video

**Requirements:**

- Valid JWT token
- All form fields are required
- Large file size considerations for video uploads

---

## Notes

### Authentication

- Most endpoints require JWT token obtained from login
- Include token in Authorization header: `Bearer {{TOKEN}}`

### File Uploads

- Use `multipart/form-data` for endpoints with file uploads
- Supported image formats: JPG, PNG
- Supported video formats: MP4

### Error Handling

- Check response status codes for success/failure
- Implement proper error handling in your client application

### Rate Limiting

- Consider implementing rate limiting for production use
- Monitor API usage to prevent abuse

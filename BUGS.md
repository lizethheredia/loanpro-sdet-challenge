# Bug Report — LoanPro SDET Challenge

## Bug 1 — Duplicate Email Returns 500 Instead of 409

**Endpoint:** `POST /{env}/users`  
**Severity:** High  
**Expected:** `409 Conflict`  
**Actual:** `500 Internal Server Error`  

**Steps to Reproduce:**
1. Create a user with email `jane@example.com`
2. Create the same user again with the same email

**Spec Reference:** OpenAPI spec defines `409` for duplicate email.  
**Impact:** Unhandled server error exposed to client instead of a meaningful conflict response.

---

## Bug 2 — User Not Found Returns 500 Instead of 404

**Endpoint:** `GET /{env}/users/{email}`  
**Severity:** High  
**Expected:** `404 Not Found`  
**Actual:** `500 Internal Server Error`  

**Steps to Reproduce:**
1. `GET /dev/users/nobody@example.com` where user does not exist

**Spec Reference:** OpenAPI spec defines `404` when user is not found.  
**Impact:** Server crashes instead of returning a meaningful not found response.

---

## Bug 3 — Delete Without Authentication Returns 204 Instead of 401

**Endpoint:** `DELETE /{env}/users/{email}`  
**Severity:** Critical — Security Vulnerability  
**Expected:** `401 Unauthorized`  
**Actual:** `204 No Content`  

**Steps to Reproduce:**
1. Create a user with email `jane@example.com`
2. Send `DELETE /dev/users/jane@example.com` with no `Authentication` header
3. User is deleted successfully

**Spec Reference:** OpenAPI spec requires `Authentication` header.  
**Impact:** Any unauthenticated request can delete any user. Critical security vulnerability.
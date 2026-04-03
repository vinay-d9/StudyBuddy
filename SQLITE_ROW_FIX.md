# SQLite3.Row AttributeError Fix

## Problem
The Flask app was crashing with:
```
AttributeError: 'sqlite3.Row' object has no attribute 'get'
Location: POST /api/resume/extract-skills endpoint
```

The error occurred because:
1. Database functions returned `sqlite3.Row` objects directly from `cur.fetchone()`
2. Code tried to call `.get()` method on these Row objects
3. SQLite3.Row objects don't have a `.get()` method (only support bracket notation `row['key']`)

## Root Causes Fixed

### Database Functions (app/db.py)

#### 1. `get_latest_resume()` - Line 372-385
**Before:**
```python
return cur.fetchone()  # Returns sqlite3.Row
```

**After:**
```python
row = cur.fetchone()
return dict(row) if row else None  # Returns dict or None
```

#### 2. `get_resume_by_id()` - Line 401-410  
**Before:**
```python
return cur.fetchone()  # Returns sqlite3.Row
```

**After:**
```python
row = cur.fetchone()
return dict(row) if row else None  # Returns dict or None
```

#### 3. `get_onboarding_response()` - Line 277-281
**Before:**
```python
return cur.fetchone()  # Returns sqlite3.Row
```

**After:**
```python
row = cur.fetchone()
return dict(row) if row else None  # Returns dict or None
```

### Routes File (app/routes.py)

#### 4. Resume extraction logging - Line 1656
**Before:**
```python
print(f"✅ Resume found: {resume.get('filename')}")  # .get() fails on Row
```

**After:**
```python
print(f"✅ Resume found: {resume['filename']}")  # Bracket notation works
```

## Impact
- ✅ POST `/api/resume/extract-skills` endpoint now works correctly
- ✅ All resume operations use cached dict objects instead of Row objects
- ✅ Code follows consistent pattern used in other database functions
- ✅ Maintains backward compatibility with existing code that calls `dict()` on results

## Testing
The fix enables the following workflow:
1. User uploads resume → stored correctly
2. User clicks "Extract Skills" button  
3. Backend calls `/api/resume/extract-skills`
4. Endpoint fetches resume from database (now returns dict)
5. Skill extraction completes without AttributeError
6. Skills are added to user's skill checklist
7. Checklist is saved to database

## Related Code Patterns
Similar fixes are already applied in other database functions:
- `list_approved_resources()` - Line 928: `return [dict(r) for r in cur.fetchall()]`
- `list_pending_resources()` - Line 936: `return [dict(r) for r in cur.fetchall()]`
- `list_resumes()` - Line 416: `return [dict(r) for r in cur.fetchall()]`

These fixes ensure consistency across the codebase.

# Frontend UI Alignment Audit Report

## Executive Summary
Detected **multiple misalignment inconsistencies** across frontend CSS files. Since the workspace is not a git repository, file modification history cannot be verified. However, clear discrepancies exist between layout definitions across different pages.

---

## Critical Findings

### 1. **Horizontal Padding Inconsistency** 🔴
**Impact**: Causes left/right content shift between pages

#### Dashboard/Default Layout
```css
.dashboard-page .auth-shell {
    padding: 72px 6vw 6vh;  /* 6vw horizontal */
}
```
**File**: [auth.css](app/static/css/auth.css#L787)

#### Placement Prep Tracker Layout
```css
.progress-shell {
    padding: 72px 5vw 6vh;  /* 5vw horizontal (DIFFERENT!) */
}
```
**File**: [progress.css](app/static/css/progress.css#L8)

#### Resources Layout
```css
.resources-shell {
    padding: 72px 5vw !important;  /* 5vw horizontal */
}
```
**File**: [resources.css](app/static/css/resources.css#L14)

**Misalignment Score**: ⚠️ **HIGH** - Navigation between pages causes noticeable horizontal shift

---

### 2. **Grid Column Ratio Mismatch** 🟡
**Impact**: Affects two-column layout proportions across pages

#### Dashboard Top Row
```css
.dashboard-top-row {
    grid-template-columns: 1fr 1.1fr;  /* ~47% | ~53% */
}
```
**File**: [auth.css](auth.css#L800)

#### Progress Shell
```css
.progress-shell {
    grid-template-columns: 0.95fr 1.3fr;  /* ~42% | ~58% */
}
```
**File**: [progress.css](app/static/css/progress.css#L5)

#### Resources Shell
```css
.resources-shell {
    grid-template-columns: 0.9fr 1.3fr;  /* ~41% | ~59% */
}
```
**File**: [resources.css](app/static/css/resources.css#L11)

**Misalignment Score**: ⚠️ **MEDIUM** - Left sidebar width changes between pages

---

### 3. **Navbar Height Not Factored Into Content Offset** 🟡
**Impact**: Potential navbar overlap or content gap

#### Navbar Definition
```css
.dash-navbar {
    position: fixed;
    height: 56px;  /* Fixed navbar height */
    z-index: 500;
}
```
**File**: [auth.css](auth.css#L630)

#### Content Padding-Top
```css
.dashboard-page .auth-shell {
    padding: 72px 6vw 6vh;  /* 72px top padding */
}
```
**File**: [auth.css](auth.css#L788)

**Gap Analysis**: `72px - 56px = 16px` extra spacing (may be intentional or create awkward gaps)

---

### 4. **Responsive Breakpoint Inconsistencies** 🟡
**Impact**: Mobile/tablet layout breaks differently across pages

#### Dashboard Mobile
```css
@media (max-width: 768px) {
    .dash-navbar-inner {
        padding: 0 16px;
    }
}
```

#### Progress Mobile
```css
/* No specific media query for .progress-shell adjustments */
```

**Missing**: Responsive rules for progress and resources on tablets/mobile

---

## Suspected Changes

Without git history, these CSS properties appear to have been modified:

| Property | Current Value | Suspected Issue |
|----------|---------------|-----------------|
| `auth-shell` padding | `72px 6vw 6vh` | Changed from 5vw? |
| `progress-shell` padding | `72px 5vw 6vh` | Different than main shell |
| Grid column ratios | Varies (1fr/0.95fr/0.9fr) | Likely modified separately |
| Resources grid | `0.9fr 1.3fr` | Unique ratio not used elsewhere |

---

## Recommended Fixes

### Priority 1: Standardize Horizontal Padding
```css
/* Apply consistently across ALL main containers */
.dashboard-page .auth-shell,
.progress-shell,
.resources-shell,
.mocktest-shell {
    padding: 72px 5vw 6vh;  /* Choose 5vw or 6vw - keep consistent */
}
```

### Priority 2: Align Grid Columns
```css
/* Use single ratio across all two-column layouts */
.dashboard-top-row,
.progress-shell,
.resources-shell {
    grid-template-columns: 0.95fr 1.3fr;  /* Unified ratio */
    gap: 32px;
}
```

### Priority 3: Add Navbar Offset
```css
/* Ensure content respects navbar */
.dashboard-page .auth-shell {
    margin-top: 56px;  /* Match navbar height OR adjust padding */
}
```

### Priority 4: Mobile Consistency
```css
@media (max-width: 768px) {
    .dashboard-page .auth-shell,
    .progress-shell,
    .resources-shell {
        padding: 72px 4vw 6vh;  /* Consistent mobile padding */
    }
}
```

---

## Affected Pages
- ✗ Dashboard (skill-checklist)
- ✓ Placement Prep Tracker  
- ✗ Resources
- ✗ Mock Tests
- ✓ Resume (uses different layout)
- ✓ Admin (uses sidebar layout)

---

## Action Items
1. [ ] Verify intended padding values (5vw or 6vw?)
2. [ ] Choose single grid column ratio
3. [ ] Test navbar-to-content spacing
4. [ ] Add responsive mobile rules
5. [ ] Cross-browser alignment test (Chrome, Firefox, Safari)
6. [ ] Document layout standards for future changes

---

**Generated**: 2 April 2026  
**Audit Type**: CSS Alignment Consistency Check

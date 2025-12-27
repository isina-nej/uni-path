# Change Proposal: Initialize Unipath Project Structure

**Change ID:** `init-unipath-project`  
**Status:** Approved for Implementation  
**Date:** 2025-12-27

## Overview

Initialize the Unipath project with proper folder structure, separating frontend (Flutter) and backend (Django) implementations. This establishes the foundational architecture for the cross-platform course selection application.

## Scope

### In Scope
- Create `frontend/` folder structure with Flutter project initialization
- Create `backend/` folder structure with Django project initialization
- Configure project naming to "unipath" across all components
- Set up basic project configuration files

### Out of Scope
- Detailed feature implementation
- Database schema design
- API endpoint implementation
- UI/UX design details

## Changes

This change affects the following capabilities:

1. **Project Structure** - Creating the initial folder hierarchy
2. **Frontend Setup** - Initializing Flutter application
3. **Backend Setup** - Initializing Django application

## Affected Specs

- `openspec/specs/` - Will be updated after initialization with framework-specific specs

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Naming inconsistencies | Use "unipath" consistently across all configs |
| Dependency conflicts | Lock versions in pubspec.yaml and requirements.txt |
| Build environment issues | Document setup steps in README files |

## Acceptance Criteria

1. ✓ Frontend folder created with Flutter project at `frontend/`
2. ✓ Backend folder created with Django project at `backend/`
3. ✓ Both projects have app name "unipath" configured
4. ✓ Project root README updated with folder structure
5. ✓ Basic .gitignore configured for both platforms

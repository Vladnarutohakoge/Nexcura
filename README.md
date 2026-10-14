# NexCura — Master Healthcare Platform

A responsive, accessible, multilingual healthcare platform front-end supporting patients, clinicians, administrators, and hospital staff.

---

## 🚀 Live Interactive Applications

The platform includes a cohesive set of interconnected, standalone web applications and a comprehensive 86+ page template catalog:

| File | Application | Description |
|---|---|---|
| [`index.html`](index.html) | **Modern Landing Page** | Redesigned with 3D interactive tilt, animated metric counters, quick-action strip, and modern glassmorphic header. |
| [`about.html`](about.html) | **3D Interactive About Us** | English narrative with real 3D CSS transforms, flip cards, interactive 2020-2026 timeline, and leadership showcase. |
| [`specialties.html`](specialties.html) | **Care Specialties & Directory** | 8 clinical specialties with interactive filter chips, condition tags, doctor cards, and facility directory. |
| [`clinical-trials.html`](clinical-trials.html) | **Clinical Trials Discovery** | Research search with faceted filtering (phase, status, condition, sponsor), trial cards, and pre-screener. |
| [`ai-assistant.html`](ai-assistant.html) | **NexCura AI Assistant** | Conversational AI helper with emergency detection (112/911), suggested prompt chips, and multilingual support. |
| [`patient-portal.html`](patient-portal.html) | **Patient & Caregiver Portal (SPA)** | Protected SPA featuring Dashboard, Appointments, Intake, History, Meds, Labs, Documents, and Messages. |
| [`clinician-portal.html`](clinician-portal.html) | **Clinician Workspace (SPA)** | Protected SPA featuring Schedule, Patient List, Interactive Chart Drawer, SOAP Notes, and Trials Discovery. |
| [`staff-portal.html`](staff-portal.html) | **Hospital Staff Workspace (SPA)** | Protected SPA featuring Ward 4B Bed Occupancy, ED Triage Roster, Pharmacy Queue, and Shift Coordination. |
| [`admin-portal.html`](admin-portal.html) | **Administrator Console (SPA)** | Protected SPA featuring System Metrics, User & Role Management, RBAC Policy Matrix, and Audit Log. |
| [`feedback.html`](feedback.html) | **Public Feedback & Complaints** | Public submission interface with department routing, star ratings, and real-time backend persistence. |
| [`pages.html`](pages.html) | **Comprehensive Page Catalog** | Searchable directory and live router for all 86+ planned page templates across public and staff spaces. |

---

## 🌟 Modern 3D & Futuristic Frontend Features

1. **20-Image Continuous Crossfade Carousel**: Fast 1-second auto-transition between 20 high-resolution healthcare slides with image preloading, live slide counter, and pause-on-hover.
2. **Three.js 3D WebGL Interactive Hologram**: Dynamic rendering of rotating holographic icosahedron, orbiting DNA torus structures, and a 350+ neural particle cloud responsive to cursor movement.
3. **Universal 3D Perspective Tilt**: Depth-based hover perspective across cards, statistics, and platform module showcases.
4. **Progressive Web App (PWA)**: Standalone mobile/desktop app installability with offline Service Worker caching (`static/sw.js`, `static/manifest.json`).

---

## 🔐 Demo Credentials (Password Protection)

All 4 specialized portals are secured with client-side password protection and session persistence:

| Portal | URL | Demo Username | Demo Password |
|---|---|---|---|
| **Admin Console** | [`admin-portal.html`](admin-portal.html) | `admin` | `admin@123` |
| **Doctor & Clinician Workspace** | [`clinician-portal.html`](clinician-portal.html) | `clinician` | `clinic@123` |
| **Hospital Staff Workspace** | [`staff-portal.html`](staff-portal.html) | `staff` | `staff@123` |
| **Patient & Caregiver Portal** | [`patient-portal.html`](patient-portal.html) | `patient` | `patient@123` |

---

## 💾 Backend Architecture & Persistence

- **Runtime**: Python 3.11 / Flask Server (`app.py`)
- **Database**: SQLite Relational Database (`nexcura.db`) with automatic schema initialization and data seeding for:
  - `feedback` (`GET` & `POST /api/v1/feedback`)
  - `appointments` (`GET` & `POST /api/v1/appointments`)
- **Live Proxy**: Real-time integration with ClinicalTrials.gov API v2 (`GET /api/v1/trials/search`)
- **AI Safety Guardrails**: Regex-based acute emergency symptom interception triggering immediate emergency directives (`POST /api/v1/ai/chat`)

---

## 🚀 Quick Start & Deployment

### Local Development
```powershell
# Run Automated Tests
.\.venv\Scripts\python.exe test_app.py

# Launch Flask Server
.\.venv\Scripts\python.exe app.py
```

### Docker Container Deployment
```bash
# Build and run container
docker-compose up -d --build
```

---

## 📁 Project Structure

```
NexCura/
├── app.py                  # Flask REST API backend & static file server
├── test_app.py             # 13 automated unit tests
├── nexcura.db              # SQLite persistent database
├── Dockerfile              # Production container build recipe
├── docker-compose.yml      # Multi-container service definitions
├── templates/
│   └── home.html           # Full-width 3D WebGL hero & 20-image carousel
├── static/
│   ├── css/style.css       # Core design tokens, 3D tilt, and glassmorphic styles
│   ├── js/main.js          # Three.js 3D hologram, carousel logic, and PWA registration
│   ├── js/i18n.js          # 4-language internationalization
│   ├── manifest.json       # PWA Web App Manifest
│   └── sw.js               # Service Worker with offline caching
├── feedback.html           # Public feedback & complaints form
├── patient-portal.html     # Patient portal SPA
├── clinician-portal.html   # Clinician workspace SPA
├── admin-portal.html       # Administrator console SPA
├── staff-portal.html       # Hospital staff workspace SPA
├── specialties.html        # Care specialties & doctor directory
├── clinical-trials.html    # Clinical research explorer & 3D visualizations
├── ai-assistant.html       # 24/7 AI symptom triage companion
├── README.md               # Complete platform documentation
└── SITEMAP.md              # 86+ page inventory with access levels
```

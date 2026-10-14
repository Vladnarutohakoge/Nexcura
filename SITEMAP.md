# NexCura — Master Sitemap & Page Inventory

This sitemap inventories **86 distinct pages and templates** across 10 functional areas. Each page identifies target audience, purpose, access level, and primary action.

**Access Level Legend:**
- **Public (P)**: Open to all visitors; no authentication required. No private records exposed.
- **Authenticated Patient (A-Pt)**: Requires verified patient account login + MFA. Restricted to own data.
- **Restricted Clinician (R-Clin)**: Requires verified clinician credentials + MFA. Limited to assigned patients.
- **Restricted Staff (R-Staff)**: Requires authorized hospital staff credentials + MFA. Limited to task queues and operations.
- **Restricted Admin (R-Admin)**: Requires organization administrator credentials + MFA. Configuration, access, and audit only.
- **System (Shared)**: Contextual system state (errors, loading, session timeout).

### 🖥️ Direct Standalone Interactive Files
* Landing Page: [`index.html`](index.html)
* 3D About Page: [`about.html`](about.html)
* Specialties Directory: [`specialties.html`](specialties.html)
* Clinical Trials Discovery: [`clinical-trials.html`](clinical-trials.html)
* AI Assistant: [`ai-assistant.html`](ai-assistant.html)
* Patient Portal (Protected): [`patient-portal.html`](patient-portal.html)
* Clinician Workspace (Protected): [`clinician-portal.html`](clinician-portal.html)
* Staff Workspace (Protected): [`staff-portal.html`](staff-portal.html)
* Admin Console (Protected): [`admin-portal.html`](admin-portal.html)
* 86-Page Catalog & Router: [`pages.html`](pages.html)

---

## 1. Public Website (15 Pages)

| # | Page Name | Audience | Purpose | Access Level | Primary Action |
|---|---|---|---|---|---|
| 1 | **Home** | Public visitors | Brand introduction, service overview, AI entry, emergency guidance | **P** | Find care / Explore services |
| 2 | **About NexCura** | Public visitors | Mission, values, founding principles, and clinical safety philosophy | **P** | Learn about platform |
| 3 | **Our Mission** | Public visitors | In-depth healthcare equity, accessibility, and connectivity statement | **P** | Read mission |
| 4 | **How NexCura Works** | Patients & public | Visual overview of finding care, scheduling, and care coordination | **P** | Explore care journey |
| 5 | **Care Services Overview** | Patients & public | High-level summary of medical departments and clinical services | **P** | Browse specialties |
| 6 | **Specialty Directory** | Patients & public | Complete searchable list of medical specialties and care pathways | **P** | Select specialty |
| 7 | **Specialty Detail Template** | Patients & public | Deep dive into conditions treated, care team, and visit expectations | **P** | Find specialist / Book |
| 8 | **Hospital & Clinic Locations** | Patients & public | Interactive map and directory of physical and virtual facilities | **P** | Get directions / Hours |
| 9 | **Location Detail Template** | Patients & public | Facility hours, services offered, parking, transit, and accessibility info | **P** | View location details |
| 10 | **Doctor Directory** | Patients & public | Searchable clinician directory with specialty and language filters | **P** | View doctor profile |
| 11 | **Doctor Profile Template** | Patients & public | Clinician biography, credentials, specialties, languages, and practice location | **P** | Request appointment |
| 12 | **Clinical Trials Overview** | Patients & public | Introduction to research trials, ethical guidelines, and study discovery | **P** | Search trials |
| 13 | **Careers** | Job seekers | Open clinical and technical positions, culture, and benefits | **P** | Apply for position |
| 14 | **News & Stories** | Public visitors | Health education articles, clinical updates, and patient stories | **P** | Read article |
| 15 | **Contact & Support** | Public & patients | Facility contact numbers, inquiry forms, and emergency escalation | **P** | Submit inquiry / Call |

---

## 2. Patient & Caregiver Portal (20 Pages)

| # | Page Name | Audience | Purpose | Access Level | Primary Action |
|---|---|---|---|---|---|
| 16 | **Patient Sign In** | Patients | Secure authentication entry point with MFA support | **P** | Sign in |
| 17 | **Account Registration** | New patients | Multi-step onboarding to create account and verify identity | **P** | Register account |
| 18 | **Identity & Account Recovery** | Patients | Secure password reset and account verification workflows | **P** | Recover access |
| 19 | **Patient Onboarding** | New patients | Guided walkthrough of portal features, preferences, and language selection | **A-Pt** | Complete setup |
| 20 | **Patient Home Dashboard** | Patients | Central command: upcoming visits, pending tasks, messages, quick links | **A-Pt** | View next step |
| 21 | **Personal Profile** | Patients | Contact details, demographics, emergency contacts, language preferences | **A-Pt** | Update profile |
| 22 | **Care Team Directory** | Patients | List of assigned primary care and specialist clinicians | **A-Pt** | Contact care team |
| 23 | **Care Team Member Detail** | Patients | Role description, clinical focus, and direct messaging route for provider | **A-Pt** | Send message |
| 24 | **Appointment List** | Patients | Historical and upcoming appointments with status indicators | **A-Pt** | Manage appointments |
| 25 | **Appointment Detail** | Patients | Visit location, preparation instructions, provider notes, cancellation option | **A-Pt** | Reschedule / Prepare |
| 26 | **Appointment Request** | Patients | Multi-step scheduling request flow (in-person or virtual) | **A-Pt** | Request visit |
| 27 | **Visit Preparation Checklist** | Patients | Interactive checklist of questions, medications, and items to bring | **A-Pt** | Check off items |
| 28 | **Patient Intake** | Patients | Pre-visit symptoms, concerns, and history questionnaire (user-reported) | **A-Pt** | Submit intake |
| 29 | **Medical History** | Patients | Conditions, surgeries, family history (labeled by verification status) | **A-Pt** | Review / Add entry |
| 30 | **Medication List** | Patients | Active medications, dosages, frequency, and prescriber records | **A-Pt** | Report concern / Refill |
| 31 | **Allergy List** | Patients | Documented allergens, reactions, severity, and reported date | **A-Pt** | Report allergy |
| 32 | **Test Results List** | Patients | Diagnostic lab and imaging reports with date and status filters | **A-Pt** | View results |
| 33 | **Test Result Detail** | Patients | Result values, reference ranges, clinician interpretation, and plain-language summary | **A-Pt** | Download PDF / Ask team |
| 34 | **Care Plan** | Patients | Ongoing wellness goals, lifestyle instructions, and care team guidance | **A-Pt** | Track progress |
| 35 | **Patient Documents** | Patients | Discharge summaries, referral letters, medical certificates, and uploaded files | **A-Pt** | Upload / Download |

---

## 3. Doctor & Clinician Workspace (18 Pages)

| # | Page Name | Audience | Purpose | Access Level | Primary Action |
|---|---|---|---|---|---|
| 36 | **Clinician Sign In** | Clinicians | High-assurance clinical sign-in with institutional SSO / MFA | **P** | Sign in |
| 37 | **Clinician Dashboard** | Clinicians | Daily clinic schedule, pending intake reviews, urgent alerts, task queue | **R-Clin** | Start encounter / Review |
| 38 | **Assigned Patient List** | Clinicians | Searchable roster of assigned patients with risk and concern indicators | **R-Clin** | Open patient chart |
| 39 | **Patient Chart Overview** | Clinicians | Longitudinal health record drawer (demographics, meds, allergies, vitals) | **R-Clin** | Review clinical history |
| 40 | **Patient Intake Review** | Clinicians | Review patient-reported pre-visit questionnaires and flag key symptoms | **R-Clin** | Import to encounter |
| 41 | **Encounter Workspace** | Clinicians | Structured SOAP note documentation environment with real-time drafting | **R-Clin** | Document & sign |
| 42 | **Clinical Note Editor** | Clinicians | Full-screen progress note drafting, voice dictation, and macro support | **R-Clin** | Sign note |
| 43 | **Medication & Allergy Review** | Clinicians | Reconciliation interface for active prescriptions and patient-reported allergies | **R-Clin** | Reconcile / Approve |
| 44 | **Results Review** | Clinicians | In-depth diagnostic review with historical trend lines and critical value flags | **R-Clin** | Acknowledge result |
| 45 | **Care Plan Editor** | Clinicians | Multi-disciplinary care plan creation with patient goal assignments | **R-Clin** | Publish plan |
| 46 | **Referral Management** | Clinicians | Outgoing and incoming specialty referral coordination and tracking | **R-Clin** | Create referral |
| 47 | **Follow-Up Task Queue** | Clinicians | Actionable tasks: lab follow-ups, telephone calls, prescription reviews | **R-Clin** | Complete task |
| 48 | **Trial Discovery** | Clinicians | Search matching research studies based on patient diagnostic criteria | **R-Clin** | Evaluate trial |
| 49 | **Trial Detail & Criteria Review** | Clinicians | Deep-dive into inclusion/exclusion criteria, primary endpoints, and sites | **R-Clin** | Match patient |
| 50 | **Trial Pre-Screen Summary** | Clinicians | Generate preliminary clinical summary for study coordinator review | **R-Clin** | Submit pre-screen |
| 51 | **Team Messaging** | Clinicians | Secure intra-team clinical chat and care team coordination | **R-Clin** | Send clinical message |
| 52 | **Clinician Schedule** | Clinicians | Weekly and daily clinic calendar with appointment slot management | **R-Clin** | Modify availability |
| 53 | **Clinician Profile & Preferences** | Clinicians | Clinical credentials, notification preferences, and documentation templates | **R-Clin** | Save preferences |

---

## 4. Hospital & Support Staff Workspace (12 Pages)

| # | Page Name | Audience | Purpose | Access Level | Primary Action |
|---|---|---|---|---|---|
| 54 | **Staff Sign In** | Support staff | Role-gated operational sign-in with session timeout controls | **P** | Sign in |
| 55 | **Staff Home Dashboard** | Support staff | Today's arrivals, check-in queue, scheduling requests, escalation alerts | **R-Staff** | View queue |
| 56 | **Check-In Queue** | Front desk | Live roster of patients arriving today with identity verification status | **R-Staff** | Initiate check-in |
| 57 | **Patient Check-In Detail** | Front desk | Identity verification, insurance/consent collection, and rooming status | **R-Staff** | Complete check-in |
| 58 | **Scheduling Workspace** | Scheduling staff | Clinic capacity management, calendar bookings, and cancellation rebooking | **R-Staff** | Book slot |
| 59 | **Appointment Coordination** | Scheduling staff | Manage multi-specialty appointments and transport/interpreter arrangements | **R-Staff** | Coordinate visit |
| 60 | **Referral Coordination Queue** | Referral staff | Track pending external referrals and insurance prior-authorization status | **R-Staff** | Update referral |
| 61 | **Referral Detail** | Referral staff | Document exchange, authorization approval, and specialist scheduling | **R-Staff** | File authorization |
| 62 | **Document Processing Queue** | Records staff | Index, scan, and assign incoming medical faxes, scans, and external records | **R-Staff** | Route document |
| 63 | **Patient Communication Queue** | Support staff | Non-clinical outbound messaging (visit reminders, prep instructions, follow-ups) | **R-Staff** | Dispatch message |
| 64 | **Escalation Queue** | Triage staff | Operational and service escalations needing clinical or administrative review | **R-Staff** | Escalate issue |
| 65 | **Staff Profile & Preferences** | Support staff | Staff shift preferences, department assignment, and notification options | **R-Staff** | Save preferences |

---

## 5. Administrator Console (12 Pages)

| # | Page Name | Audience | Purpose | Access Level | Primary Action |
|---|---|---|---|---|---|
| 66 | **Administrator Sign In** | Admins | Privileged administrative access with mandatory hardware MFA | **P** | Sign in |
| 67 | **Organization Dashboard** | Admins | Organization-wide operational metrics, user statistics, system health | **R-Admin** | Inspect metrics |
| 68 | **Facility Management** | Admins | Configuration of physical clinics, operating hours, and location assets | **R-Admin** | Add / Edit facility |
| 69 | **Facility Detail** | Admins | Department assignments, room inventory, and local service mapping | **R-Admin** | Update configuration |
| 70 | **Department Management** | Admins | Clinical and administrative department hierarchy and service catalogs | **R-Admin** | Manage department |
| 71 | **User Directory** | Admins | Searchable user directory across all staff, clinicians, and patient accounts | **R-Admin** | Manage user |
| 72 | **User & Role Detail** | Admins | Individual account permission review, credential auditing, and deactivation | **R-Admin** | Edit permissions |
| 73 | **Role & Permission Configuration** | Admins | RBAC policy editor: define custom permission sets and access levels | **R-Admin** | Update RBAC policy |
| 74 | **Service Catalog Management** | Admins | Maintain publicly published clinical specialties, fees, and procedures | **R-Admin** | Publish service |
| 75 | **Content Management** | Admins | Maintain approved public educational content, announcements, and FAQs | **R-Admin** | Publish content |
| 76 | **Language & Locale Configuration** | Admins | Enable interface languages, review translation readiness, set regional defaults | **R-Admin** | Configure locales |
| 77 | **Audit & Activity Review** | Admins | Immutable, searchable audit logs tracking PHI access and security events | **R-Admin** | Export audit log |

---

## 6. Shared, Clinical Trials, AI & System Pages (9 Pages)

| # | Page Name | Audience | Purpose | Access Level | Primary Action |
|---|---|---|---|---|---|
| 78 | **NexCura AI Assistant** | Public & patients | Conversational navigation, intake helper, and emergency triage | **P / A-Pt** | Chat / Ask question |
| 79 | **Help Center** | All users | Self-service support knowledge base and portal navigation guides | **P / A-Pt** | Search articles |
| 80 | **Frequently Asked Questions** | All users | Categorized answers to common patient and clinician platform questions | **P** | Read FAQ |
| 81 | **Accessibility Information** | All users | WCAG 2.2 AA conformance statement, screen reader aids, feedback contact | **P** | Review a11y details |
| 82 | **Privacy Notice** | All users | Detailed policy on health data collection, storage, retention, and rights | **P** | Read policy |
| 83 | **Terms of Use** | All users | Platform governance, patient responsibilities, and medical disclaimer terms | **P** | Accept terms |
| 84 | **Consent & Preferences** | Patients | Manage granular clinical data sharing, communication, and research consents | **A-Pt** | Update consents |
| 85 | **Not Found / Unavailable (404)** | All users | Helpful 404 recovery state with search bar and key section links | **System** | Return to safety |
| 86 | **Access Denied / Session Expired** | Authenticated | Safe sign-in recovery state when permissions are insufficient or session lapses | **System** | Re-authenticate |

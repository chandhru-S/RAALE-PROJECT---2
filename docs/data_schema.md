# Data Schema Documentation — ORRS

All datasets in ORRS use 100% de-identified synthetic identifiers (`PAT001`, `SURG001`, `OT001`, `STAFF001`).

## 1. Theatre Schedule (`theatre_schedules`)

| Column Name | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer (PK) | Primary Key |
| `session_id` | String (Unique) | Synthetic Session Identifier (`SESSION001`) |
| `surgery_id` | String (Unique) | Synthetic Surgery Identifier (`SURG001`) |
| `theatre_id` | String | Operating Theatre Identifier (`OT001` - `OT008`) |
| `department` | String | Surgical Department (e.g. Orthopaedics, Cardiology) |
| `procedure_type` | String | Procedure Description |
| `scheduled_start` | DateTime | Scheduled Surgery Start Time |
| `scheduled_end` | DateTime | Scheduled Surgery End Time |
| `actual_start` | DateTime | Actual Surgery Start Time |
| `actual_end` | DateTime | Actual Surgery End Time |
| `priority` | String | Priority (`Normal`, `High`, `Emergency`) |
| `previous_session_overrun` | String | Overrun Flag (`Yes`, `No`) |

## 2. Staff Roster (`staff_rosters`)

| Column Name | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer (PK) | Primary Key |
| `staff_id` | String | Synthetic Staff Identifier (`STAFF001`) |
| `staff_name_alias` | String | Synthetic Staff Alias |
| `role` | String | Role (`Surgeon`, `Anaesthetist`, `Nurse`, `Technician`) |
| `department` | String | Assigned Department |
| `shift_start` | DateTime | Shift Start Timestamp |
| `shift_end` | DateTime | Shift End Timestamp |
| `availability_status` | String | Status (`AVAILABLE`, `DELAYED`, `UNAVAILABLE`, `NULL`) |
| `assigned_theatre` | String | Assigned OT ID |
| `assigned_surgery` | String (FK) | Foreign key to `theatre_schedules.surgery_id` |
| `last_updated` | DateTime | Status Update Timestamp |

## 3. Equipment Status (`equipment`)

| Column Name | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer (PK) | Primary Key |
| `equipment_id` | String (Unique)| Synthetic Equipment Identifier (`EQ0001`) |
| `equipment_name` | String | Equipment Description |
| `theatre_id` | String | Assigned Operating Theatre |
| `status` | String | Status (`READY`, `IN_USE`, `MAINTENANCE`, `FAULTY`, `UNKNOWN`) |
| `maintenance_status` | String | Maintenance State (`OK`, `REQUIRED`) |
| `last_maintenance_date`| DateTime | Last Bio-Medical Inspection Date |
| `last_updated` | DateTime | Status Update Timestamp |

## 4. Patient Readiness (`patient_readiness`)

| Column Name | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer (PK) | Primary Key |
| `patient_id` | String | Synthetic Patient ID (`PAT001`) |
| `surgery_id` | String (FK) | Foreign Key to `theatre_schedules.surgery_id` |
| `consent_complete` | Boolean | Surgical Consent Form Verified |
| `fasting_complete` | Boolean | Pre-op Fasting Protocol Verified |
| `preoperative_assessment` | String | Anesthetic Pre-op Clearance |
| `vitals_status` | String | Vitals Assessment (`NORMAL`, `ELEVATED_BP`, `FEVER`) |
| `blood_available` | String | Blood Bank Confirmation (`CONFIRMED`, `PENDING`) |
| `patient_ready` | Boolean | Overall Patient Readiness Flag |
| `last_updated` | DateTime | Checklist Timestamp |

## 5. Sterile Supplies (`sterile_supplies`)

| Column Name | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer (PK) | Primary Key |
| `supply_id` | String | Synthetic Supply Pack ID |
| `surgery_id` | String (FK) | Foreign Key to `theatre_schedules.surgery_id` |
| `supply_name` | String | Surgical Tray Description |
| `required_quantity` | Integer | Required Trays Count |
| `available_quantity` | Integer | Available Trays Count |
| `sterility_confirmed` | Boolean | CSSD Autoclave Sterility Confirmation |
| `status` | String | Status (`AVAILABLE`, `PARTIAL`, `MISSING`, `STERILITY_PENDING`) |
| `last_updated` | DateTime | Supply Verification Timestamp |

## 6. Delay Reasons (`delay_reasons`)

| Column Name | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer (PK) | Primary Key |
| `delay_id` | String | Delay Log ID |
| `surgery_id` | String (FK) | Foreign Key to `theatre_schedules.surgery_id` |
| `delay_category` | String | Category (`Patient`, `Staff`, `Equipment`, `Supplies`, `Emergency`) |
| `delay_reason` | String | Root Cause Narrative |
| `delay_minutes` | Integer | Recorded Delay Duration in Minutes |
| `avoidable` | Boolean | Avoidable Operational Delay Flag |
| `timestamp` | DateTime | Delay Incident Timestamp |

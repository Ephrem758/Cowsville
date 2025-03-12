# Farm Manager API Documentation

## Base URL

`http://localhost:8000/api`

## Authentication

Currently using Django's default authentication system.

## Endpoints

### 1. Farms Management

#### List Farms

- **URL:** `/farms/`
- **Method:** `GET`
- **Query Parameters:**
  - `search`: Search farms by ID, owner name, or address
- **Description:** Get all farms with optional filtering
- **Success Response:** `200 OK`

#### Create Farm

- **URL:** `/farms/`
- **Method:** `POST`
- **Description:** Create a new farm
- **Request Body:**
  ```json
  {
    "farm_id": "FARM001",
    "owner_name": "John Doe",
    "address": "Addis Ababa",
    "telephone_number": "+251912345678",
    "fertility_camp_no": 1,
    "total_number_of_cows": 10,
    "number_of_calves": 2,
    "number_of_milking_cows": 5,
    "total_daily_milk": 100,
    "type_of_housing": 1,
    "type_of_floor": 1,
    "main_feed": "Grass and hay",
    "rate_of_cow_feeding": 1,
    "source_of_water": 1,
    "rate_of_water_giving": 1,
    "farm_hygiene_score": 3
  }
  ```

#### Change Farm's Doctor

- **URL:** `/farms/{farm_id}/change_doctor/`
- **Method:** `POST`
- **Description:** Assign a new doctor to the farm
- **Data:**
  ```json
  {
    "doctor_id": 1
  }
  ```

### 2. Cows Management

#### List Cows

- **URL:** `/cows/`
- **Method:** `GET`
- **Query Parameters:**
  - `farm_id`: Filter by farm ID
  - `breed`: Filter by breed type
- **Description:** Get all cows with optional filtering

#### Create Cow

- **URL:** `/cows/`
- **Method:** `POST`
- **Description:** Register a new cow
- **Request Body:**
  ```json
  {
    "is_deleted": false,
    "cow_id": "01",
    "age_in_days": 730,
    "sex": "F",
    "parity": 2,
    "body_weight": 450.5,
    "bcs": 3.5,
    "lactation_number": 2,
    "days_in_milk": 100,
    "average_daily_milk": 25.5,
    "cow_inseminated_before": true,
    "last_date_insemination": "2025-03-11",
    "number_of_inseminations": 2,
    "id_or_breed_bull_used": "HF-BULL-001",
    "last_calving_date": "2025-03-11",
    "farm": "01",
    "breed": 1,
    "gynecological_status": 1
  }
  ```

#### Farmer Medical Assessment

- **URL:** `/cows/farmer_medical_assessment/`
- **Method:** `POST`
- **Description:** Submit farmer's medical observation
- **Request Body:**
  ```json
  {
    "farm_id": "FARM001",
    "cow_id": "01",
    "sickness_description": "Reduced appetite and lethargy"
  }
  ```

#### Doctor Medical Assessment

- **URL:** `/cows/doctor_assessment/`
- **Method:** `POST`
- **Description:** Submit doctor's medical assessment
- **Request Body:**
  ```json
  {
    "farm_id": "FARM001",
    "cow_id": "01",
    "doctor_id": 1,
    "is_cow_sick": true,
    "sickness_type": "infectious",
    "general_health": 1,
    "udder_health": 1,
    "mastitis": 1,
    "body_condition_score": 3.5,
    "reproductive_health": "Normal cycling",
    "metabolic_disease": "None observed",
    "is_cow_vaccinated": true,
    "vaccination_date": "2024-03-21",
    "vaccination_type": "FMD Vaccine",
    "has_deworming": true,
    "deworming_date": "2024-03-21",
    "deworming_type": "Albendazole",
    "diagnosis": "Mild infection",
    "treatment": "Antibiotics prescribed",
    "prescription": "Medication details",
    "next_assessment_date": "2024-04-21",
    "notes": "Follow up required"
  }
  ```

#### Monitor Heat Sign

- **URL:** `/cows/monitor_heat_sign/`
- **Method:** `POST`
- **Description:** Record heat signs and insemination details
- **Request Body:**
  ```json
  {
    "farm_id": "FARM001",
    "cow_id": "01",
    "is_inseminated": true,
    "insemination_time": "14:30",
    "insemination_count": 2,
    "lactation_number": 3
  }
  ```

#### Monitor Pregnancy

- **URL:** `/cows/monitor_pregnancy/`
- **Method:** `POST`
- **Description:** Update pregnancy status
- **Request Body:**
  ```json
  {
    "farm_id": "FARM001",
    "cow_id": "01",
    "is_pregnant": true,
    "lactation_number": 2
  }
  ```

### 3. Medical Assessments

#### List Medical Assessments

- **URL:** `/medical-assessments/`
- **Method:** `GET`
- **Description:** Get all doctor medical assessments
- **Query Parameters:**
  - `farm_id`: Filter by farm ID
  - `cow_id`: Filter by cow ID
  - `doctor_id`: Filter by doctor ID
  - `is_cow_sick`: Filter by health status (true/false)
- **Success Response:** `200 OK`

#### Get Single Assessment

- **URL:** `/medical-assessments/{id}/`
- **Method:** `GET`
- **Description:** Get details of a specific medical assessment
- **Success Response:** `200 OK`

### 4. Inseminators Management

#### List Inseminators

- **URL:** `/inseminators/`
- **Method:** `GET`
- **Description:** Get all registered inseminators

#### Create Inseminator

- **URL:** `/inseminators/`
- **Method:** `POST`
- **Description:** Register a new inseminator
- **Data:**
  ```json
  {
    "name": "John Doe",
    "phone_number": "+251912345678",
    "address": "Addis Ababa",
    "is_active": true,
    "license_number": "INS123"
  }
  ```

#### Replace Inseminator

- **URL:** `/inseminators/{inseminator_id}/replace_inseminator/`
- **Method:** `POST`
- **Description:** Update inseminator details
- **Request Body:**
  ```json
  {
    "name": "John Doe",
    "phone_number": "+251912345678",
    "address": "Addis Ababa"
  }
  ```

### 5. Doctors Management

#### List Doctors

- **URL:** `/doctors/`
- **Method:** `GET`
- **Description:** Get all registered doctors

#### Create Doctor

- **URL:** `/doctors/`
- **Method:** `POST`
- **Description:** Register a new doctor
- **Data:**
  ```json
  {
    "name": "Dr. John Smith",
    "phone_number": "+251912345678",
    "address": "Addis Ababa",
    "is_active": true,
    "specialization": "Veterinary Medicine",
    "license_number": "VET123"
  }
  ```

### 6. Choice Models (Read-only)

#### List Breed Types

- **URL:** `/breedtypes/`
- **Method:** `GET`
- **Description:** Get all available breed types

#### List Housing Types

- **URL:** `/housingtypes/`
- **Method:** `GET`
- **Description:** Get all available housing types

#### List Floor Types

- **URL:** `/floortypes/`
- **Method:** `GET`
- **Description:** Get all available floor types

#### List Water Sources

- **URL:** `/watersources/`
- **Method:** `GET`
- **Description:** Get all available water sources

#### List Feeding Frequencies

- **URL:** `/feedingfrequencies/`
- **Method:** `GET`
- **Description:** Get all available feeding frequencies

### 7. Farmer Medical Reports

#### List Farmer Reports

- **URL:** `/farmer-medical-reports/`
- **Method:** `GET`
- **Description:** Get all farmer-submitted medical reports
- **Query Parameters:**
  - `farm_id`: Filter by farm ID
  - `cow_id`: Filter by cow ID
  - `is_reviewed`: Filter by review status (true/false)
- **Success Response:** `200 OK`

#### Get Single Farmer Report

- **URL:** `/farmer-medical-reports/{id}/`
- **Method:** `GET`
- **Description:** Get details of a specific farmer medical report
- **Success Response:** `200 OK`

### 8. Insemination Records

#### List Insemination Records

- **URL:** `/insemination-records/`
- **Method:** `GET`
- **Description:** Get all insemination records
- **Query Parameters:**
  - `farm_id`: Filter by farm ID
  - `cow_id`: Filter by cow ID
  - `inseminator_id`: Filter by inseminator ID
  - `is_inseminated`: Filter by insemination status (true/false)
- **Success Response:** `200 OK`

#### Get Single Record

- **URL:** `/insemination-records/{id}/`
- **Method:** `GET`
- **Description:** Get details of a specific insemination record
- **Success Response:** `200 OK`

## Message Types

- `heat_alert`: Heat detection alerts
- `health_alert`: Health-related notifications
- `vaccination_alert`: Vaccination reminders
- `pregnancy_update`: Pregnancy status updates
- `inseminator_alert`: Inseminator notifications
- `farmer_alert`: General farmer notifications
- `doctor_alert`: Doctor notifications
- `doctor_assignment`: Doctor assignment updates
- `inseminator_assignment`: Inseminator assignment updates
- `pregnancy_confirmation`: Pregnancy confirmation notices

## Error Responses

- `400 Bad Request`: Missing or invalid parameters
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Notes

- All IDs referenced in requests must exist in the system
- Dates should be in YYYY-MM-DD format
- Times should be in HH:MM format
- Phone numbers should be in international format (+251XXXXXXXXX)

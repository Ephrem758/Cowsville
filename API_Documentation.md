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
- **Description:** Create a new farm with all necessary details
- **Data:**
  ```json
  {
    "farm_id": "FARM001",
    "owner_name": "John Doe",
    "address": "Addis Ababa",
    "telephone_number": "+251912345678",
    "type_of_housing": 1,
    "type_of_floor": 1,
    "source_of_water": 1,
    "feeding_frequency": 1,
    "inseminator": 1,
    "doctor": 1
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
- **Description:** Register a new cow in the system
- **Data:**
  ```json
  {
    "farm": "FARM001",
    "cow_id": "COW001",
    "breed": 1,
    "age_in_days": 730,
    "sex": "F",
    "body_weight": 450.5,
    "bcs": 3.5,
    "gynecological_status": 1,
    "lactation_number": 2,
    "average_daily_milk": 25.5
  }
  ```

### 3. Medical Assessments

#### Doctor's Medical Assessment

- **URL:** `/medical-assessments/doctor_assessment/`
- **Method:** `POST`
- **Description:** Submit a comprehensive medical assessment by a doctor
- **Data:**
  ```json
  {
    "farm_id": "1",
    "cow_id": "8620",
    "doctor_id": 1,
    "is_cow_sick": true,
    "sickness_type": "infectious",
    "general_health": 1,
    "udder_health": 1,
    "mastitis": 1,
    "body_condition_score": 3,
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

#### Farmer's Medical Report

- **URL:** `/cows/farmer_medical_assessment/`
- **Method:** `POST`
- **Description:** Submit initial medical observation by a farmer
- **Data:**
  ```json
  {
    "farm_id": "1",
    "cow_id": "8620",
    "sickness_description": "የወተት ነጭ ራሽ ባክቴሪያ ይታያል"
  }
  ```

### 4. Heat Sign Monitoring

#### Record Heat Sign

- **URL:** `/cows/monitor_heat_sign/`
- **Method:** `POST`
- **Description:** Record heat signs and insemination details
- **Data:**
  ```json
  {
    "farm_id": "1",
    "cow_id": "8620",
    "is_inseminated": true,
    "insemination_time": "14:30",
    "insemination_count": 2,
    "lactation_number": 3
  }
  ```

### 5. Inseminators Management

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
- **Data:**
  ```json
  {
    "name": "New Name",
    "phone_number": "+251912345678",
    "address": "New Address"
  }
  ```

### 6. Doctors Management

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

### 7. Choice Models (Read-only)

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

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
  - `search`: Search by cow ID or breed name
- **Description:** Get all cows with optional filtering

#### Create Cow

- **URL:** `/cows/`
- **Method:** `POST`
- **Description:** Register a new cow. Automatically creates a default reproduction record and medical assessment for the cow.
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

#### Get Cows by Farm

- **URL:** `/cows/by_farm/`
- **Method:** `GET`
- **Query Parameters:**
  - `farm_id`: (Required) The ID of the farm to filter cows
- **Description:** Get all cows belonging to a specific farm
- **Success Response:**
  ```json
  {
    "farm_id": "FARM001",
    "total_cows": 5,
    "cows": [
      {
        "cow_id": "01",
        "breed": 1,
        "age_in_days": 730,
        "sex": "F",
        "parity": 2,
        "body_weight": "450.50",
        "bcs": "3.5",
        "gynecological_status": 1,
        "lactation_number": 2,
        "days_in_milk": 100,
        "average_daily_milk": "25.50",
        "cow_inseminated_before": true,
        "last_date_insemination": "2025-03-11",
        "number_of_inseminations": 2,
        "id_or_breed_bull_used": "HF-BULL-001",
        "last_calving_date": "2025-03-11"
      }
    ]
  }
  ```

#### Record Heat Sign

- **URL:** `/cows/record_heat_sign/`
- **Method:** `POST`
- **Description:** Record heat signs for a cow and notify relevant parties
- **Request Body:**
  ```json
  {
    "farm_id": "FARM001",
    "cow_id": "01",
    "heat_signs": "Mounting behavior, Restlessness"
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
    "date_of_insemination": "2024-03-21",
    "insemination_count": 2,
    "lactation_number": 3
  }
  ```

#### Monitor Pregnancy

- **URL:** `/cows/monitor_pregnancy/`
- **Method:** `POST`
- **Description:** Update pregnancy status and related information
- **Request Body:**
  ```json
  {
    "farm_id": "FARM001",
    "cow_id": "01",
    "pregnancy_date": "2024-03-21",
    "service_per_conception": 2,
    "lactation_number": 3
  }
  ```

#### Monitor Birth

- **URL:** `/cows/monitor_birth/`
- **Method:** `POST`
- **Description:** Record birth event for a cow
- **Request Body:**
  ```json
  {
    "farm_id": "FARM001",
    "cow_id": "01",
    "calving_date": "2024-03-21",
    "last_calving_date": "2023-03-21",
    "calf_sex": "M"
  }
  ```

#### Get Records

##### Pregnancy Records

- **URL:** `/cows/pregnancy_records/`
- **Method:** `GET`
- **Query Parameters:**
  - `farm_id`: (Required) Farm ID
  - `cow_id`: (Optional) Cow ID

##### Birth Records

- **URL:** `/cows/birth_records/`
- **Method:** `GET`
- **Query Parameters:**
  - `farm_id`: (Required) Farm ID
  - `cow_id`: (Optional) Cow ID

##### Heat Sign Records

- **URL:** `/cows/heat_sign_records/`
- **Method:** `GET`
- **Query Parameters:**
  - `farm_id`: (Required) Farm ID
  - `cow_id`: (Optional) Cow ID

##### Medical Records

- **URL:** `/cows/medical_records/`
- **Method:** `GET`
- **Query Parameters:**
  - `farm_id`: (Required) Farm ID
  - `cow_id`: (Optional) Cow ID
  - `type`: (Optional) Filter by record type ('farmer', 'doctor', or 'all')

### 3. Medical Management

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

### 4. Staff Management

#### List/Create Doctors

- **URL:** `/doctors/`
- **Method:** `GET` (list), `POST` (create)
- **Description:** Manage doctor records

#### List/Create Inseminators

- **URL:** `/inseminators/`
- **Method:** `GET` (list), `POST` (create)
- **Description:** Manage inseminator records

#### Replace Inseminator

- **URL:** `/inseminators/{inseminator_id}/replace_inseminator/`
- **Method:** `POST`
- **Description:** Update existing inseminator's details
- **Request Body:**
  ```json
  {
    "name": "John Doe",
    "phone_number": "+251912345678",
    "address": "Addis Ababa"
  }
  ```

### 5. Reference Data Endpoints

#### Breed Types

- **URL:** `/breedtypes/`
- **Method:** `GET`
- **Description:** List all breed types

#### Housing Types

- **URL:** `/housingtypes/`
- **Method:** `GET`
- **Description:** List all housing types

#### Floor Types

- **URL:** `/floortypes/`
- **Method:** `GET`
- **Description:** List all floor types

#### Feeding Frequencies

- **URL:** `/feedingfrequencies/`
- **Method:** `GET`
- **Description:** List all feeding frequencies

#### Water Sources

- **URL:** `/watersources/`
- **Method:** `GET`
- **Description:** List all water sources

#### Health Status Types

- **URL:** `/gynecologicalstatuses/`
- **URL:** `/udderhealthstatuses/`
- **URL:** `/mastitisstatuses/`
- **URL:** `/generalhealthstatuses/`
- **Method:** `GET`
- **Description:** List all health status types

### 6. Messages

#### List Messages

- **URL:** `/messages/`
- **Method:** `GET`
- **Query Parameters:**
  - `farm_id`: Filter by farm ID
  - `cow_id`: Filter by cow ID (requires farm_id)
  - `search`: Search in message text or type
- **Description:** Get all messages with optional filtering

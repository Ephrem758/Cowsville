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
- **Description:** Register a new cow. Automatically creates a default reproduction record for the cow.
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
- **Actions Performed:**
  1. Creates the cow record with provided details
  2. Automatically creates a default reproduction record with:
     - `is_cow_pregnant`: false
     - `heat_sign_start`: null
     - `heat_signs_seen`: null
- **Error Responses:**
  - `400 Bad Request`: Invalid data provided
  - `500 Internal Server Error`: Failed to create cow or reproduction record

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
- **Description:** Record heat signs and insemination details. Updates both insemination records and reproduction records if the cow is inseminated. Sends notifications to both farmer and inseminator.
- **Request Body:**
  ```json
  {
    "farm_id": "FARM001",
    "cow_id": "01",
    "inseminated_now": "Yes",
    "date_of_insemination": "2024-03-21",
    "insemination_number": "2",
    "lactation_no": "3"
  }
  ```
- **Success Response:**
  ```json
  {
    "message": "Heat sign monitoring recorded successfully",
    "record_id": 1,
    "farm_id": "FARM001",
    "cow_id": "01"
  }
  ```
- **Field Descriptions:**

  - `farm_id`: Farm identifier (required)
  - `cow_id`: Cow identifier (required)
  - `inseminated_now`: Whether the cow was inseminated ("Yes" or "No") (required)
  - `date_of_insemination`: Date when the cow was inseminated (YYYY-MM-DD format) (required)
  - `insemination_number`: Number of times the cow has been inseminated (required)
  - `lactation_no`: Current lactation number of the cow (required)

- **Actions Performed:**

  1. Creates an insemination record with the provided details
  2. If cow is inseminated (inseminated_now = "Yes"):
     - Updates or creates a reproduction record with the insemination date
  3. Sends notifications:
     - To Farmer: Includes cow status, lactation number, insemination count, and date of insemination
     - To Inseminator: Includes farm details, cow status, lactation number, insemination count, and date of insemination

- **Error Responses:**

  - `400 Bad Request`: Invalid data provided
    ```json
    {
      "error": "Invalid data format",
      "details": {
        "field_name": ["error message"]
      }
    }
    ```
  - `500 Internal Server Error`: Server-side error
    ```json
    {
      "error": "Failed to record heat sign monitoring"
    }
    ```

- **Validation Rules:**
  1. Farm and cow must exist in the system
  2. Farm must have an active inseminator assigned
  3. Insemination number and lactation number must be valid integers
  4. Date must be in YYYY-MM-DD format

#### Monitor Pregnancy

- **URL:** `/cows/monitor_pregnancy/`
- **Method:** `POST`
- **Description:** Update pregnancy status and related information for a cow. Creates or updates reproduction records and sends notifications.
- **Request Body:**
  ```json
  {
    "farm_id": "FARM001",
    "cow_id": "01",
    "pregnancy_date": "2024-03-21",
    "days_until_calving": 280,
    "service_per_conception": 2,
    "lactation_number": 3
  }
  ```
- **Success Response:**
  ```json
  {
    "message": "Pregnancy monitoring record updated successfully",
    "cow_id": "01",
    "farm_id": "FARM001",
    "pregnancy_date": "2024-03-21",
    "expected_calving_date": "2024-12-25",
    "service_per_conception": 2,
    "lactation_number": 3
  }
  ```
- **Actions Performed:**

  1. Creates or updates reproduction record with pregnancy information
  2. Updates cow's insemination and lactation records
  3. Calculates expected calving date
  4. Sends notification to farmer with pregnancy details

- **Error Responses:**

  - `400 Bad Request`: Invalid data provided
  - `500 Internal Server Error`: Failed to update pregnancy status

- **Validation Rules:**
  1. Farm and cow must exist in the system
  2. All fields are required
  3. Numbers must be valid integers
  4. Date must be in YYYY-MM-DD format

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
- **Success Response:**
  ```json
  {
    "message": "Heat sign recorded and alert sent successfully",
    "cow_id": "01",
    "farm_id": "FARM001",
    "heat_sign_time": "2024-03-21T10:30:00Z",
    "alert_sent": true
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
      // ... more cows
    ]
  }
  ```
- **Error Response:**
  ```json
  {
    "error": "farm_id query parameter is required"
  }
  ```
  Status: 400 Bad Request

#### Alternative Method (Using Filter)

You can also filter cows using the main cows endpoint:

- **URL:** `/cows/?farm__farm_id=FARM001`
- **Method:** `GET`
- **Description:** Filter cows by farm ID using query parameter

#### Monitor Birth

- **URL:** `/cows/monitor_birth/`
- **Method:** `POST`
- **Description:** Record birth event for a cow. Updates reproduction records and cow details, and sends notifications.
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
- **Success Response:**
  ```json
  {
    "message": "Birth event recorded successfully",
    "cow_id": "01",
    "farm_id": "FARM001",
    "calving_date": "2024-03-21",
    "last_calving_date": "2023-03-21",
    "calf_sex": "M",
    "parity": 3
  }
  ```
- **Actions Performed:**

  1. Updates or creates reproduction record with calving information
  2. Updates cow's parity and last calving date
  3. Sends notification to farmer with birth details

- **Error Responses:**
  - `400 Bad Request`: Invalid data provided
  - `500 Internal Server Error`: Failed to record birth event

#### Change Farm's Inseminator

- **URL:** `/farms/{farm_id}/change_inseminator/`
- **Method:** `POST`
- **Description:** Assign a new inseminator to the farm
- **Request Body:**
  ```json
  {
    "inseminator_id": 1
  }
  ```
- **Success Response:**
  ```json
  {
    "message": "inseminator changed successfully",
    "farm_id": "FARM001",
    "new_staff_id": 1,
    "old_staff_id": 2
  }
  ```
- **Actions Performed:**
  1. Updates farm's assigned inseminator
  2. Deactivates old inseminator if exists
  3. Sends notifications to:
     - Old inseminator about unassignment
     - New inseminator with farm details
     - Creates message record in system

#### Replace Inseminator

- **URL:** `/inseminators/{inseminator_id}/replace_inseminator/`
- **Method:** `POST`
- **Description:** Update existing inseminator's details and notify affected farms
- **Request Body:**
  ```json
  {
    "name": "John Doe",
    "phone_number": "+251912345678",
    "address": "Addis Ababa"
  }
  ```
- **Success Response:**
  ```json
  {
    "message": "Inseminator details updated successfully",
    "affected_farms_count": 5,
    "new_details": {
      "name": "John Doe",
      "phone": "+251912345678",
      "address": "Addis Ababa"
    }
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

### Messages

#### List Messages

- **URL:** `/messages/`
- **Method:** `GET`
- **Description:** Get all messages with optional filtering
- **Query Parameters:**
  - `farm_id`: Filter by farm ID
  - `cow_id`: Filter by cow ID (requires farm_id)
  - `search`: Search in message text or type
- **Note:** Cow ID filtering only works when farm ID is also provided

### Reproduction Records

#### List Reproduction Records

- **URL:** `/reproduction-records/`
- **Method:** `GET`
- **Description:** Get all reproduction records with optional filtering
- **Query Parameters:**
  - `farm_id`: Filter by farm ID
  - `cow_id`: Filter by cow ID
  - `is_pregnant`: Filter by pregnancy status (true/false)

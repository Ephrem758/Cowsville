import axios from "axios";

// Base URL from your API documentation
// const API_URL = "https://apiv2.cowsville-aau-cvma.com/api/";
// const FARM_API_URL = "https://apiv2.cowsville-aau-cvma.com/api/farms/";
// const COW_API_URL = "https://apiv2.cowsville-aau-cvma.com/api/cows/";
// const token = localStorage.getItem("authToken") || "mock_token_for_testing";

// Base URL from environment variables
const API_URL = process.env.REACT_APP_API_BASE_URL || "https://apiv3.cowsville-aau-cvma.com/api/";
// const API_URL = process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000/api/";
const FARM_API_URL = `${API_URL}${process.env.REACT_APP_FARMS_ENDPOINT || "farms/"}`;
const COW_API_URL = `${API_URL}${process.env.REACT_APP_COWS_ENDPOINT || "cows/"}`;

// Default credentials from environment
const DEFAULT_USERNAME = process.env.REACT_APP_USERNAME || "farmadmin";
const DEFAULT_PASSWORD = process.env.REACT_APP_PASSWORD || "SecurePass123";

// Create base64 encoded credentials for Basic Auth
const createBasicAuthCredentials = (username, password) => {
  return btoa(`${username}:${password}`);
};

// Get stored credentials or use defaults
const getStoredCredentials = () => {
  const storedUsername = localStorage.getItem("username") || DEFAULT_USERNAME;
  const storedPassword = localStorage.getItem("password") || DEFAULT_PASSWORD;
  return { username: storedUsername, password: storedPassword };
};

// Create an axios instance with proper cookie handling
const apiClient = axios.create({
  baseURL: API_URL,
  withCredentials: true, // CRITICAL: This sends cookies with requests
});

// Basic Auth login function
export const login = async (username, password) => {
  try {
    console.log("Attempting Basic Auth login to:", API_URL);
    console.log("With credentials:", { username, password: "***" });

    // Test the credentials by making a request to a protected endpoint
    const credentials = createBasicAuthCredentials(username, password);
    const response = await axios.get(`${API_URL}farms/`, {
      headers: {
        Authorization: `Basic ${credentials}`,
        "Content-Type": "application/json",
      },
    });

    console.log("Login successful! API response:", response.status);

    // Store credentials for future requests
    localStorage.setItem("username", username);
    localStorage.setItem("password", password);
    localStorage.setItem("authToken", credentials); // Store the base64 credentials as "token"

    return credentials; // Return the base64 credentials
  } catch (error) {
    console.error("Login failed - Full error:", error);
    console.error("Error response:", error.response?.data);
    console.error("Error status:", error.response?.status);
    console.error("Error URL:", error.config?.url);

    // Provide more specific error messages
    if (error.response?.status === 401) {
      throw new Error("Invalid username or password.");
    } else if (error.response?.status === 404) {
      throw new Error("API endpoint not found. Please check the API URL.");
    } else if (error.response?.status === 403) {
      throw new Error("Access forbidden. Please check your credentials.");
    } else {
      throw new Error(error.response?.data?.message || error.message || "Login failed");
    }
  }
};

// Function to display current environment configuration
export const displayEnvironmentConfig = () => {
  console.log("🔧 Environment Configuration:");
  console.log(`  API Base URL: ${API_URL}`);
  console.log(`  Authentication Method: Basic Auth`);
  console.log(`  Default Username: ${DEFAULT_USERNAME}`);
  console.log(`  Default Password: ${DEFAULT_PASSWORD ? "***" : "Not set"}`);
  console.log(`  Farms URL: ${FARM_API_URL}`);
  console.log(`  Cows URL: ${COW_API_URL}`);

  const stored = getStoredCredentials();
  console.log(`  Stored Username: ${stored.username}`);
  console.log(`  Stored Password: ${stored.password ? "***" : "Not set"}`);
};

// Function to test what endpoints are available
export const testApiEndpoints = async () => {
  console.log("🔍 Testing API endpoints to find authentication...");

  // Display current configuration
  displayEnvironmentConfig();

  // Test the base API first
  try {
    const baseResponse = await axios.get(API_URL);
    console.log("✅ Base API is accessible:", baseResponse.status);
    console.log("Base API response:", baseResponse.data);

    // Log all available endpoints
    const endpoints = baseResponse.data;
    console.log("📋 Available endpoints:");
    Object.keys(endpoints).forEach((key) => {
      console.log(`  - ${key}: ${endpoints[key]}`);
    });
  } catch (error) {
    console.log("❌ Base API error:", error.response?.status, error.message);
  }

  // Test if we can access farms without auth (to see what error we get)
  try {
    const farmsResponse = await axios.get(`${API_URL}farms/`);
    console.log("✅ Farms endpoint accessible without auth:", farmsResponse.status);
  } catch (error) {
    console.log("🔒 Farms endpoint requires auth:", error.response?.status, error.response?.data);
  }

  // Test some common authentication patterns that might not be in the base response
  const authEndpoints = [
    `${API_URL}auth/`,
    `${API_URL}login/`,
    `${API_URL}token/`,
    `${API_URL}user/`,
    `${API_URL}admin/`,
    `${API_URL}authentication/`,
  ];

  console.log("🔍 Testing potential auth endpoints not in base response:");
  for (const endpoint of authEndpoints) {
    try {
      const response = await axios.get(endpoint);
      console.log(`✅ ${endpoint} - Status: ${response.status}`);
      console.log(`   Response:`, response.data);
    } catch (error) {
      console.log(`❌ ${endpoint} - Status: ${error.response?.status}`);
    }
  }
};

// Alternative login function that tries different common endpoints
export const loginAlternative = async (username, password) => {
  const endpoints = [
    `${API_URL}auth/login/`,
    `${API_URL}login/`,
    `${API_URL}auth/token/`,
    `${API_URL}api-token-auth/`,
    `${API_URL}obtain-auth-token/`,
    // Try some other common patterns
    `${API_URL}authenticate/`,
    `${API_URL}signin/`,
    `${API_URL}user/login/`,
    `${API_URL}admin/login/`,
  ];

  for (const endpoint of endpoints) {
    try {
      console.log("Trying endpoint:", endpoint);
      const response = await axios.post(endpoint, {
        username,
        password,
      });

      console.log("Login successful at:", endpoint);
      console.log("Response:", response.data);

      const token = response.data.access || response.data.token || response.data.key;
      if (token) {
        localStorage.setItem("authToken", token);
        return token;
      }
    } catch (error) {
      console.log(`Failed at ${endpoint}:`, error.response?.status);
      continue;
    }
  }

  throw new Error(
    "All authentication endpoints failed. Please check with backend team for correct endpoint."
  );
};

// Temporary mock authentication for testing frontend functionality
export const mockLogin = async (username, password) => {
  console.log("🔧 Using mock authentication for testing...");

  // Simulate API delay
  await new Promise((resolve) => setTimeout(resolve, 1000));

  // Check credentials against environment variables
  if (username === DEFAULT_USERNAME && password === DEFAULT_PASSWORD) {
    const credentials = createBasicAuthCredentials(username, password);
    console.log("✅ Mock login successful with Basic Auth credentials");
    localStorage.setItem("username", username);
    localStorage.setItem("password", password);
    localStorage.setItem("authToken", credentials);
    return credentials;
  } else {
    throw new Error("Invalid username or password");
  }
};

export const getFarms = async (searchQuery = "") => {
  try {
    const { username, password } = getStoredCredentials();
    const credentials = createBasicAuthCredentials(username, password);

    const response = await axios.get(`${API_URL}farms/`, {
      params: { search: searchQuery },
      headers: {
        Authorization: `Basic ${credentials}`,
        "Content-Type": "application/json",
      },
    });

    const responses = await axios.get(`${API_URL}doctors/`, {
      params: { search: searchQuery },
      headers: {
        Authorization: `Basic ${credentials}`,
        "Content-Type": "application/json",
      },
    });
    console.log("Doctor", responses.data);

    // Ensure we always return an array
    const data = response.data;
    if (Array.isArray(data)) {
      return data;
    } else if (data && Array.isArray(data.results)) {
      // Handle paginated responses
      return data.results;
    } else if (data && typeof data === "object") {
      // If it's a single object, wrap it in an array
      return [data];
    }
    // Fallback to empty array
    return [];
  } catch (error) {
    console.error("Error fetching farms:", error);
    return [];
  }
};

// export const getdoctor = async (searchQuery = "") => {
//   try {
//     const token = localStorage.getItem("authToken"); // Retrieve token
//     const response = await axios.get("https://apiv2.cowsville-aau-cvma.com/api/doctors/", {
//       params: { search: searchQuery },
//       headers: { Authorization: `Bearer ${token}` }, // Add token
//     });
//     console.log("Doctor", data.Doctor);
//     return response.data;
//   } catch (error) {
//     console.error("Error fetching farms:", error);
//     return [];
//   }
// };

// export const getCows = async (farmId = null) => {
//   try {
//     let url = "https://apiv2.cowsville-aau-cvma.com/api/api/cows/";
//     if (farmId) {
//       url = `https://apiv2.cowsville-aau-cvma.com/api/api/cows/?farm_id=${farmId}`;
//     }
//     const response = await axios.get(url);
//     return farmId ? response.data.cows : response.data; // Handle API response structure
//   } catch (error) {
//     console.error("API Error:", error);
//     return []; // Fallback to empty array
//   }
// };

export const getCows = async (farmId = null) => {
  try {
    const { username, password } = getStoredCredentials();
    const credentials = createBasicAuthCredentials(username, password);

    const params = {};
    if (farmId) {
      params.farm_id = farmId; // Use farm_id as query parameter
    }

    const response = await axios.get(COW_API_URL, {
      params,
      headers: {
        Authorization: `Basic ${credentials}`,
        "Content-Type": "application/json",
      },
    });

    // Handle paginated response structure
    const data = response.data;
    if (Array.isArray(data)) {
      return data;
    } else if (data && Array.isArray(data.results)) {
      return data.results;
    } else if (data && typeof data === "object") {
      return [data];
    }
    return [];
  } catch (error) {
    console.error("API Error fetching cows:", error);
    console.error("Error response:", error.response?.data);
    console.error("Error status:", error.response?.status);
    return [];
  }
};

// export const getDoctorAssessments = async (farmId = null, cowId = null) => {
//   try {
//     const token = localStorage.getItem("authToken");
//     const params = {};
//     if (farmId) params.farm_id = farmId;
//     if (cowId) params.cow_id = cowId;
//     const response = await axios.get(`${API_URL}medical-assessments/`, {
//       params,
//       headers: { Authorization: `Bearer ${token}` },
//     });
//     return response.data.results || [];
//   } catch (error) {
//     console.error("Error fetching doctor assessments:", error);
//     return [];
//   }
// };
export const getDoctorAssessments = async (farmId = null, cowId = null) => {
  try {
    const token = localStorage.getItem("authToken");
    const params = {};
    if (farmId) params.farm_id = farmId;
    if (cowId) params.cow = cowId;

    const response = await axios.get(`${API_URL}medical-assessments/`, {
      params,
      headers: { Authorization: `Bearer ${token}` },
    });

    const payload = response.data;
    if (Array.isArray(payload)) {
      // the endpoint directly returned an array
      return payload;
    }
    if (Array.isArray(payload.results)) {
      // your view is paginated
      return payload.results;
    }
    // It was a single object – wrap it in an array
    return [payload];
  } catch (error) {
    console.error("Error fetching doctor assessments:", error);
    return [];
  }
};

// export const getCowHeatSign = async (farmId, cowId) => {
//   try {
//     const response = await axios.get("https://apiv2.cowsville-aau-cvma.com/api/api/cows/heat_sign_records/", {
//       farm_id: farmId,
//       cow_id: cowId,
//     });
//     return response.data.heat_sign_time; // "2024-03-21T10:30:00Z"
//   } catch (error) {
//     console.error("Failed to fetch heat sign time:", error);
//     return null; // Handle missing data
//   }
// };
// export const getCowHeatSign = async (farmId, cowId) => {
//   try {
//     const token = localStorage.getItem("authToken");
//     const response = await axios.get(`${API_URL}cows/heat_sign_records/`, {
//       params: { farm_id: farmId, cow_id: cowId },
//       headers: { Authorization: `Bearer ${token}` },
//     });
//     return response.data.heat_sign_time || null;
//   } catch (error) {
//     console.error("Failed to fetch heat sign time:", error);
//     return null;
//   }
// };

// Fetch cow details (breed)
// export const getCowDetails = async (cowId) => {
//   try {
//     const response = await axios.get(`${COW_API_URL}${cowId}/`);
//     return response.data; // Includes breed and other cow details
//   } catch (error) {
//     console.error("Failed to fetch cow details:", error);
//     return null;
//   }
// };
export const getCowDetails = async (cowId) => {
  try {
    const token = localStorage.getItem("authToken");
    const response = await axios.get(`${API_URL}cows/${cowId}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    // Log the breed data structure for debugging
    console.log("Raw breed data:", response.data.breed);

    // Handle breed data properly
    let breedName = "N/A";
    if (response.data.breed) {
      if (typeof response.data.breed === "object" && response.data.breed.name) {
        breedName = response.data.breed.name;
      } else if (typeof response.data.breed === "string") {
        breedName = response.data.breed;
      } else if (typeof response.data.breed === "number") {
        // If it's a number, we need to map it to a breed name
        const breedMap = {
          1: "Holstein",
          2: "Jersey",
          3: "Zebu",
          4: "Crossbreed",
          // Add more mappings as needed
        };
        breedName = breedMap[response.data.breed] || "Unknown Breed";
      }
    }

    // Flatten nested fields for compatibility
    return {
      ...response.data,
      farm_id: response.data.farm?.farm_id || "N/A",
      breed: breedName,
      owner_name: response.data.farm?.owner_name || "N/A",
    };
  } catch (error) {
    console.error("Failed to fetch cow details:", error);
    return null;
  }
};

// export const getInseminationCount = async (farmId, cowId) => {
//   try {
//     const token = localStorage.getItem("authToken");
//     const response = await axios.get("http://127.0.0.1:8000/api/insemination-records/", {
//       params: { farm_id: farmId, cow_id: cowId },
//       headers: { Authorization: `Bearer ${token}` },
//     });
//     return response.data.insemination_count || 0;
//   } catch (error) {
//     console.error("Failed to fetch insemination count:", error);
//     return 0;
//   }
// };

export const getInseminationRecords = async (farmId, cowId) => {
  try {
    const token = localStorage.getItem("authToken");
    const response = await axios.get("http://127.0.0.1:8000/api/insemination-records/", {
      params: { farm_id: farmId, cow_id: cowId },
      headers: { Authorization: `Bearer ${token}` },
    });
    // response.data is an array of record objects
    return Array.isArray(response.data) ? response.data : response.data.results || [];
  } catch (error) {
    console.error("Failed to fetch insemination records:", error);
    return [];
  }
};

export const getDateOfAI = async (cowId) => {
  try {
    const token = localStorage.getItem("authToken");
    const response = await axios.get(`${API_URL}cows/${cowId}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data.date_of_ai || "N/A";
  } catch (error) {
    console.error("Failed to fetch date of AI:", error);
    return "N/A";
  }
};

// Get Monitor Birth Data (add token)
export const getMonitorBirthData = async (farmId = null) => {
  try {
    const token = localStorage.getItem("authToken");
    const params = {};
    if (farmId) params.farm_id = farmId;
    const response = await axios.get(
      "https://apiv2.cowsville-aau-cvma.com/api/cows/reproduction/",
      {
        params,
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    // Handle paginated response structure
    const data = response.data;
    if (Array.isArray(data)) {
      return data;
    } else if (data && Array.isArray(data.results)) {
      return data.results;
    }
    return [];
  } catch (error) {
    console.error("Error fetching calving data:", error);
    return [];
  }
};

// heat sign time with GET(important)
export const getHeatSignData = async (farmId, cowId) => {
  try {
    const token = localStorage.getItem("authToken");
    const response = await axios.get(`${COW_API_URL}reproduction/`, {
      params: {
        farm_id: farmId,
        cow_id: cowId || "ALL",
      },
      headers: { Authorization: `Bearer ${token}` },
    });
    // Handle paginated response structure
    const data = response.data;
    if (Array.isArray(data)) {
      return data;
    } else if (data && Array.isArray(data.results)) {
      return data.results;
    }
    return [];
  } catch (error) {
    console.error("Error fetching heat sign data:", error);
    return []; // return empty array on failure
  }
};

// heat sign time with POST to avoid 400 bad request(important)
// export const getHeatSignData = async (farmId, cowId) => {
//   try {
//     const token = localStorage.getItem("authToken");
//     // POST to record_heat_sign to ensure we always get back a record
//     const recordResponse = await axios.post(
//       `${COW_API_URL}record_heat_sign/`,
//       { farm_id: farmId, cow_id: cowId, heat_signs: "" },
//       { headers: { Authorization: `Bearer ${token}` } }
//     );
//     // Wrap the single record in an array so Tables/.find() still works
//     return [recordResponse.data];
//   } catch (error) {
//     console.error("Error fetching heat sign data:", error);
//     return []; // empty array if it fails
//   }
// };

// Get Insemination Count Data (add token)
export const getInseminationCountData = async (farmId = null, cowId = "ALL") => {
  try {
    const token = localStorage.getItem("authToken");
    const params = { farm_id: farmId || "ALL", cow_id: cowId };
    const response = await axios.get("http://127.0.0.1:8000/api/insemination-records/", {
      params,
      headers: { Authorization: `Bearer ${token}` },
    });
    // Handle paginated response structure
    const data = response.data;
    if (Array.isArray(data)) {
      return data;
    } else if (data && Array.isArray(data.results)) {
      return data.results;
    }
    return [];
  } catch (error) {
    console.error("Error fetching insemination count data:", error);
    return [];
  }
};

// Get Monitor Pregnancy Data (add token)
export const getMonitorPregnancyData = async (farmId = null, cowId = "ALL") => {
  try {
    const token = localStorage.getItem("authToken");
    const params = { farm_id: farmId, cow_id: cowId };
    const response = await axios.get(
      "https://apiv2.cowsville-aau-cvma.com/api/cows/reproduction/",
      {
        params,
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    // Handle paginated response structure
    const data = response.data;
    if (Array.isArray(data)) {
      return data;
    } else if (data && Array.isArray(data.results)) {
      return data.results;
    }
    return [];
  } catch (error) {
    console.error("Error fetching pregnancy data:", error);
    return [];
  }
};

export const getReproductionRecords = async (farmId, cowId) => {
  try {
    const token = localStorage.getItem("authToken");
    const response = await axios.get(`${API_URL}reproduction/`, {
      params: { farm: farmId, cow: cowId },
      headers: { Authorization: `Bearer ${token}` },
    });
    console.log("Reproduction Records Response:", response.data);
    // returns an array of objects like { heat_sign_start, heat_sign_end, …, pregnancy_date, calving_date }
    return Array.isArray(response.data) ? response.data : response.data.results || [];
  } catch (error) {
    console.error("Error fetching reproduction data:", error);
    return [];
  }
};

/**
 * Convenience wrappers if you'd rather name them for each form type:
 */

// heat sign monitoring window
export const getHeatSignWindow = async (farmId, cowId) => {
  try {
    const response = await axios.get(`${API_URL}reproduction/`, {
      params: { farm: farmId, cow: cowId },
    });
    console.log("Raw API Response for Heat Signs:", response.data);
    console.log("Looking for cowId:", cowId);

    // Handle paginated response structure
    const data = response.data;
    const records = Array.isArray(data) ? data : data?.results || [];

    const filteredData = records.filter((record) => {
      console.log("Checking record:", record);
      console.log("Record cow ID:", record.cow, "Type:", typeof record.cow);
      console.log("Searching for cowId:", cowId, "Type:", typeof cowId);
      return String(record.cow) === String(cowId);
    });

    console.log("Filtered Heat Sign Data:", filteredData);

    const mappedData = filteredData.map((record) => ({
      start: record.heat_sign_start,
      end: record.heat_sign_end,
      signs: record.heat_signs_seen,
      recordedAt: record.heat_sign_recorded_at,
    }));

    console.log("Final Mapped Heat Sign Data:", mappedData);
    return mappedData;
  } catch (error) {
    console.error("Error fetching heat sign window:", error);
    return [];
  }
};

// pregnancy monitor
export const getPregnancyRecords = async (farmId, cowId) => {
  try {
    const response = await axios.get(`${API_URL}reproduction/`, {
      params: { farm: farmId, cow: cowId },
    });
    console.log("Raw API Response for Pregnancy:", response.data);
    console.log("Looking for cowId:", cowId);

    // Handle paginated response structure
    const data = response.data;
    const records = Array.isArray(data) ? data : data?.results || [];

    const filteredData = records.filter((record) => {
      console.log("Checking record:", record);
      console.log("Record cow ID:", record.cow, "Type:", typeof record.cow);
      console.log("Searching for cowId:", cowId, "Type:", typeof cowId);
      return String(record.cow) === String(cowId);
    });

    console.log("Filtered Pregnancy Data:", filteredData);

    const mappedData = filteredData.map((record) => ({
      date: record.pregnancy_date,
      calving: record.calving_date,
    }));

    console.log("Final Mapped Pregnancy Data:", mappedData);
    return mappedData;
  } catch (error) {
    console.error("Error fetching pregnancy records:", error);
    return [];
  }
};

// birth monitoring
export const getBirthRecords = async (farmId, cowId) => {
  try {
    const response = await axios.get(`${API_URL}reproduction/`, {
      params: { farm: farmId, cow: cowId },
    });
    console.log("Raw API Response for Birth:", response.data);
    console.log("Looking for cowId:", cowId);

    // Handle paginated response structure
    const data = response.data;
    const records = Array.isArray(data) ? data : data?.results || [];

    const filteredData = records.filter((record) => {
      console.log("Checking record:", record);
      console.log("Record cow ID:", record.cow, "Type:", typeof record.cow);
      console.log("Searching for cowId:", cowId, "Type:", typeof cowId);
      return String(record.cow) === String(cowId);
    });

    console.log("Filtered Birth Data:", filteredData);

    const mappedData = filteredData.map((record) => ({
      calvingDate: record.calving_date,
    }));

    console.log("Final Mapped Birth Data:", mappedData);
    return mappedData;
  } catch (error) {
    console.error("Error fetching birth records:", error);
    return [];
  }
};

import axios from "axios";

// Base URL from your API documentation
const API_URL = "http://localhost:8000/api/";
const FARM_API_URL = "http://localhost:8000/api/farms/";
const COW_API_URL = "http://localhost:8000/api/cows/";
const token = localStorage.getItem("authToken") || "mock_token_for_testing";

export const getFarms = async (searchQuery = "") => {
  try {
    const token = localStorage.getItem("authToken"); // Retrieve token
    const response = await axios.get("http://localhost:8000/api/farms/", {
      params: { search: searchQuery },
      headers: { Authorization: `Bearer ${token}` }, // Add token
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching farms:", error);
    return [];
  }
};

// export const getCows = async (farmId = null) => {
//   try {
//     let url = "http://localhost:8000/api/cows/";
//     if (farmId) {
//       url = `http://localhost:8000/api/cows/?farm_id=${farmId}`;
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
    const token = localStorage.getItem("authToken");
    let url = "http://localhost:8000/api/cows/";
    if (farmId) {
      url = `${url}?farm_id=${farmId}`; // Correct endpoint for filtering
    }
    const response = await axios.get(url, { headers: { Authorization: `Bearer ${token}` } });
    return farmId ? response.data : response.data; // Adjust based on backend response
  } catch (error) {
    console.error("API Error:", error);
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
//     const response = await axios.get("http://localhost:8000/api/cows/heat_sign_records/", {
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
    const response = await axios.get("http://localhost:8000/api/cows/reproduction/", {
      params,
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
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
    // RETURN THE WHOLE ARRAY so you can .find() in Tables
    return response.data;
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
    return response.data;
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
    const response = await axios.get("http://localhost:8000/api/cows/reproduction/", {
      params,
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
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

    const filteredData = response.data.filter((record) => {
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

    const filteredData = response.data.filter((record) => {
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

    const filteredData = response.data.filter((record) => {
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

import axios from "axios";

// Base URL from your API documentation
const API_URL = "http://localhost:8000/api/farms/";
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
//     const params = {};
//     if (farmId) params.farm_id = farmId; // Required parameter
//     if (cowId) params.cow_id = cowId; // Optional parameter

//     const response = await axios.get("http://localhost:8000/api/doctor-assessments/", { params });
//     return response.data.results || []; // Adjust based on your API response
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
    if (cowId) params.cow_id = cowId;
    const response = await axios.get(`${API_URL}doctor-assessments/`, {
      params,
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data.results || [];
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
export const getCowHeatSign = async (farmId, cowId) => {
  try {
    const token = localStorage.getItem("authToken");
    const response = await axios.get(`${API_URL}cows/heat_sign_records/`, {
      params: { farm_id: farmId, cow_id: cowId },
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data.heat_sign_time || null;
  } catch (error) {
    console.error("Failed to fetch heat sign time:", error);
    return null;
  }
};

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
    // Flatten nested fields for compatibility
    return {
      ...response.data,
      farm_id: response.data.farm?.farm_id || "N/A", // Flatten farm ID
      breed: response.data.breed?.name || "N/A", // Flatten breed name
      owner_name: response.data.farm?.owner_name || "N/A",
    };
  } catch (error) {
    console.error("Failed to fetch cow details:", error);
    return null;
  }
};
// Fetch insemination count
// export const getInseminationCount = async (farmId, cowId) => {
//   try {
//     const response = await axios.post(`${COW_API_URL}monitor_heat_sign/`, {
//       farm_id: farmId,
//       cow_id: cowId,
//     });
//     return response.data.insemination_count || 0;
//   } catch (error) {
//     console.error("Failed to fetch insemination count:", error);
//     return 0;
//   }
// };
export const getInseminationCount = async (farmId, cowId) => {
  try {
    const token = localStorage.getItem("authToken");
    const response = await axios.get(`${API_URL}cows/monitor_heat_sign/`, {
      params: { farm_id: farmId, cow_id: cowId },
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data.insemination_count || 0;
  } catch (error) {
    console.error("Failed to fetch insemination count:", error);
    return 0;
  }
};

// Fetch date of AI (initially from /cows/)
// export const getDateOfAI = async (cowId) => {
//   try {
//     const response = await axios.get(`${COW_API_URL}${cowId}/`);
//     return response.data.date_of_ai || "N/A"; // Adjust based on your API response
//   } catch (error) {
//     console.error("Failed to fetch date of AI:", error);
//     return "N/A";
//   }
// };
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

// // Fetch calving data (monitor_birth)
// export const getMonitorBirthData = async (farmId = null) => {
//   try {
//     const params = {};
//     if (farmId && farmId !== "ALL") params.farm_id = farmId;
//     const response = await axios.get(`${COW_API_URL}birth_records/`, { params });
//     return response.data;
//   } catch (error) {
//     console.error("Error fetching calving data:", error);
//     return [];
//   }
// };

// export const getHeatSignData = async (farmId = null) => {
//   try {
//     const response = await axios.get(`${COW_API_URL}heat_sign_records/`, {
//       farm_id: farmId || "ALL", // Use "ALL" for bulk data
//       cow_id: "ALL",
//     });
//     return response.data;
//   } catch (error) {
//     console.error("Error fetching heat sign data:", error);
//     return [];
//   }
// };

// export const getInseminationCountData = async (farmId = null) => {
//   try {
//     const response = await axios.get(`${COW_API_URL}monitor_heat_sign/`, {
//       farm_id: farmId || "ALL", // Use "ALL" for bulk data
//       cow_id: "ALL",
//     });
//     return response.data;
//   } catch (error) {
//     console.error("Error fetching insemination count data:", error);
//     return [];
//   }
// };

// // export const getMonitorPregnancyData = async (farmId = null) => {
// //   try {
// //     const response = await axios.post(`${COW_API_URL}monitor_pregnancy/`, {
// //       farm_id: farmId || "ALL", // Use "ALL" for bulk data
// //       cow_id: "ALL",
// //     });
// //     return response.data;
// //   } catch (error) {
// //     console.error("Error fetching pregnancy data:", error);
// //     return [];
// //   }
// // };
// export const getMonitorPregnancyData = async (farmId = null, cowId = null) => {
//   try {
//     const params = {};
//     if (farmId) params.farm_id = farmId;
//     if (cowId) params.cow_id = cowId;

//     const response = await axios.get("http://localhost:8000/api/cows/pregnancy_records/", {
//       params,
//     });
//     return response.data.results || []; // Adjust based on API response
//   } catch (error) {
//     console.error("Error fetching pregnancy records:", error);
//     return [];
//   }
// };
// Get Monitor Birth Data (add token)
export const getMonitorBirthData = async (farmId = null) => {
  try {
    const token = localStorage.getItem("authToken");
    const params = {};
    if (farmId) params.farm_id = farmId;
    const response = await axios.get("http://localhost:8000/api/cows/birth_records/", {
      params,
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching calving data:", error);
    return [];
  }
};

// Get Heat Sign Data (add token)
// export const getHeatSignData = async (farmId, cowId) => {
//   try {
//     const token = localStorage.getItem("authToken");
//     const params = { farm_id: farmId, cow_id: cowId };
//     const response = await axios.get(`${API_URL}cows/heat_sign_records/`, {
//       params,
//       headers: { Authorization: `Bearer ${token}` },
//     });
//     // Return the latest heat_sign_time (first item in the array)
//     return response.data[0]?.heat_sign_time || null;
//   } catch (error) {
//     console.error("Error fetching heat sign data:", error);
//     return null;
//   }
// };

export const getHeatSignData = async (farmId, cowId) => {
  try {
    const token = localStorage.getItem("authToken");
    const response = await axios.get(`${API_URL}cows/heat_sign_records/`, {
      params,
      headers: { Authorization: `Bearer ${token}` },
    });
    // RETURN THE WHOLE ARRAY so you can .find() in Tables
    return response.data;
  } catch (error) {
    console.error("Error fetching heat sign data:", error);
    return []; // return empty array on failure
  }
};

// Get Insemination Count Data (add token)
export const getInseminationCountData = async (farmId = null, cowId = "ALL") => {
  try {
    const token = localStorage.getItem("authToken");
    const params = { farm_id: farmId || "ALL", cow_id: cowId };
    const response = await axios.get(`${API_URL}cows/monitor_heat_sign/`, {
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
    const response = await axios.get("http://localhost:8000/api/cows/pregnancy_records/", {
      params,
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching pregnancy data:", error);
    return [];
  }
};

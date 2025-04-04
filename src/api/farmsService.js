import axios from "axios";

// Base URL from your API documentation
const API_URL = "http://localhost:8000/api/farms/";
const FARM_API_URL = "http://localhost:8000/api/farms/";
const COW_API_URL = "http://localhost:8000/api/cows/";

export const getFarms = async (searchQuery) => {
  try {
    // Include search query as a URL parameter
    const response = await axios.get(API_URL, {
      params: {
        search: searchQuery, // Use the search parameter from the docs
      },
    });
    return response.data; // Return the farms data
  } catch (error) {
    console.error("Error fetching farms:", error);
    throw error;
  }
};

export const getCows = async (farmId = null) => {
  try {
    let url = "http://localhost:8000/api/cows/";
    if (farmId) {
      url = `http://localhost:8000/api/cows/by_farm/?farm_id=${farmId}`;
    }
    const response = await axios.get(url);
    return farmId ? response.data.cows : response.data; // Handle API response structure
  } catch (error) {
    console.error("API Error:", error);
    return []; // Fallback to empty array
  }
};

export const getDoctorAssessments = async () => {
  try {
    const response = await axios.get("http://localhost:8000/api/cows/doctor_assessment/");
    return response.data; // Returns all cow assessments
  } catch (error) {
    console.error("Error fetching doctor assessments:", error);
    return [];
  }
};

export const getCowHeatSign = async (farmId, cowId) => {
  try {
    const response = await axios.post("http://localhost:8000/api/cows/record_heat_sign/", {
      farm_id: farmId,
      cow_id: cowId,
    });
    return response.data.heat_sign_time; // "2024-03-21T10:30:00Z"
  } catch (error) {
    console.error("Failed to fetch heat sign time:", error);
    return null; // Handle missing data
  }
};

// Fetch cow details (breed)
export const getCowDetails = async (cowId) => {
  try {
    const response = await axios.get(`${COW_API_URL}${cowId}/`);
    return response.data; // Includes breed and other cow details
  } catch (error) {
    console.error("Failed to fetch cow details:", error);
    return null;
  }
};

// Fetch insemination count
export const getInseminationCount = async (farmId, cowId) => {
  try {
    const response = await axios.post(`${COW_API_URL}monitor_heat_sign/`, {
      farm_id: farmId,
      cow_id: cowId,
    });
    return response.data.insemination_count || 0;
  } catch (error) {
    console.error("Failed to fetch insemination count:", error);
    return 0;
  }
};

// Fetch date of AI (initially from /cows/)
export const getDateOfAI = async (cowId) => {
  try {
    const response = await axios.get(`${COW_API_URL}${cowId}/`);
    return response.data.date_of_ai || "N/A"; // Adjust based on your API response
  } catch (error) {
    console.error("Failed to fetch date of AI:", error);
    return "N/A";
  }
};

// Fetch calving data (monitor_birth)
export const getMonitorBirthData = async (farmId = null) => {
  try {
    const params = {};
    if (farmId && farmId !== "ALL") params.farm_id = farmId;
    const response = await axios.get(`${COW_API_URL}monitor_birth/`, { params });
    return response.data;
  } catch (error) {
    console.error("Error fetching calving data:", error);
    return [];
  }
};

export const getHeatSignData = async (farmId = null) => {
  try {
    const response = await axios.post(`${COW_API_URL}record_heat_sign/`, {
      farm_id: farmId || "ALL", // Use "ALL" for bulk data
      cow_id: "ALL",
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching heat sign data:", error);
    return [];
  }
};

export const getInseminationCountData = async (farmId = null) => {
  try {
    const response = await axios.post(`${COW_API_URL}monitor_heat_sign/`, {
      farm_id: farmId || "ALL", // Use "ALL" for bulk data
      cow_id: "ALL",
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching insemination count data:", error);
    return [];
  }
};

export const getMonitorPregnancyData = async (farmId = null) => {
  try {
    const response = await axios.post(`${COW_API_URL}monitor_pregnancy/`, {
      farm_id: farmId || "ALL", // Use "ALL" for bulk data
      cow_id: "ALL",
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching pregnancy data:", error);
    return [];
  }
};

import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance with base URL
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for authentication
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Farms Management
export const farmService = {
  // List all farms with optional search
  getFarms: (search = '') => {
    return api.get('/farms/', { params: { search } });
  },

  // Create a new farm
  createFarm: (farmData) => {
    return api.post('/farms/', farmData);
  },

  // Change farm's doctor
  changeFarmDoctor: (farmId, doctorId) => {
    return api.post(`/farms/${farmId}/change_doctor/`, { doctor_id: doctorId });
  },

  // Cows Management
  getCows: (params = {}) => {
    return api.get('/cows/', { params });
  },

  createCow: (cowData) => {
    return api.post('/cows/', cowData);
  },

  getCowsByFarm: (farmId) => {
    return api.get('/cows/by_farm/', { params: { farm_id: farmId } });
  },

  // Medical Assessments
  submitFarmerMedicalAssessment: (data) => {
    return api.post('/cows/farmer_medical_assessment/', data);
  },

  submitDoctorAssessment: (data) => {
    return api.post('/cows/doctor_assessment/', data);
  },

  getMedicalAssessments: (params = {}) => {
    return api.get('/medical-assessments/', { params });
  },

  getMedicalAssessment: (id) => {
    return api.get(`/medical-assessments/${id}/`);
  },

  // Insemination Management
  monitorHeatSign: (data) => {
    return api.post('/cows/monitor_heat_sign/', data);
  },

  monitorPregnancy: (data) => {
    return api.post('/cows/monitor_pregnancy/', data);
  },

  recordHeatSign: (data) => {
    return api.post('/cows/record_heat_sign/', data);
  },

  // Inseminators Management
  getInseminators: () => {
    return api.get('/inseminators/');
  },

  createInseminator: (data) => {
    return api.post('/inseminators/', data);
  },

  replaceInseminator: (inseminatorId, data) => {
    return api.post(`/inseminators/${inseminatorId}/replace_inseminator/`, data);
  },

  // Doctors Management
  getDoctors: () => {
    return api.get('/doctors/');
  },

  createDoctor: (data) => {
    return api.post('/doctors/', data);
  },

  // Choice Models
  getBreedTypes: () => {
    return api.get('/breedtypes/');
  },

  getHousingTypes: () => {
    return api.get('/housingtypes/');
  },

  getFloorTypes: () => {
    return api.get('/floortypes/');
  },

  getWaterSources: () => {
    return api.get('/watersources/');
  },

  getFeedingFrequencies: () => {
    return api.get('/feedingfrequencies/');
  },

  // Farmer Medical Reports
  getFarmerReports: (params = {}) => {
    return api.get('/farmer-medical-reports/', { params });
  },

  getFarmerReport: (id) => {
    return api.get(`/farmer-medical-reports/${id}/`);
  },

  // Insemination Records
  getInseminationRecords: (params = {}) => {
    return api.get('/insemination-records/', { params });
  },

  getInseminationRecord: (id) => {
    return api.get(`/insemination-records/${id}/`);
  },
};

export default farmService; 
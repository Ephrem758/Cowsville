const mockCows = [
  {
    cow_id: "COW101",
    farm_id: "FARM002",
    vaccination_date: "2024-03-20",
    udder_health: "Healthy",
    body_condition_score: "3.5",
    deworming_date: "2024-03-15",
    calving_date: "2023-06-01",
    recent_insemination_date: "2023-07-15",
    last_calving_date: "2022-06-01", // Previous calving date
    recent_insemination_date: "2023-07-15",
    heat_sign_date: "2023-06-20", // Heat sign date
    insemination_count: 2, // Number of inseminations
    pregnancy_status: false, // Not pregnant
    pregnancy_date: null,
  },
  {
    cow_id: "COW102",
    farm_id: "FARM002",
    vaccination_date: "2024-02-10",
    udder_health: "Mastitis",
    body_condition_score: "2.8",
    deworming_date: "2024-02-05",
    calving_date: "2023-05-10",
    last_calving_date: "2022-05-10",
    recent_insemination_date: "2023-06-20",
    heat_sign_date: "2023-05-25",
    insemination_count: 4, // More than 3 inseminations
    pregnancy_status: true, // Pregnant
    pregnancy_date: "2023-07-10",
  },
  {
    cow_id: "COW103",
    farm_id: "MOCK",
    vaccination_date: "2024-03-20",
    udder_health: "Healthy",
    body_condition_score: "3.5",
    deworming_date: "2024-03-15",
    calving_date: "2023-07-01",
    last_calving_date: "2022-07-01",
    recent_insemination_date: "2023-08-10",
    heat_sign_date: "2023-07-15",
    insemination_count: 5, // Exactly 3 inseminations
    pregnancy_status: false, // Not pregnant
    pregnancy_date: null,
  },
  {
    cow_id: "COW104",
    farm_id: "MOCK",
    vaccination_date: "2024-03-20",
    udder_health: "Healthy",
    body_condition_score: "3.5",
    deworming_date: "2024-03-15",
    calving_date: "2023-07-01",
    last_calving_date: "2022-06-01",
    recent_insemination_date: "2023-08-30",
    heat_sign_date: "2023-07-25",
    insemination_count: 4, // Exactly 3 inseminations
    pregnancy_status: true, // Not pregnant
    pregnancy_date: "2023-09-10",
  },
];
export default mockFarms;

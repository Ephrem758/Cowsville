/**
=========================================================
* Material Dashboard 2 React - v2.2.0
=========================================================

* Product Page: https://www.creative-tim.com/product/material-dashboard-react
* Copyright 2023 Creative Tim (https://www.creative-tim.com)

Coded by www.creative-tim.com

 =========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
*/

// @mui material components
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";

// Material Dashboard 2 React components
import { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import MDBox from "components/MDBox";
import MDTypography from "components/MDTypography";

// Material Dashboard 2 React example components
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Footer from "examples/Footer";
import DataTable from "examples/Tables/DataTable";

// Data
import {
  getFarms,
  getCows,
  getDoctorAssessments,
  getMonitorBirthData,
  getHeatSignData,
  getInseminationCountData,
  getMonitorPregnancyData,
} from "api/farmsService";
import authorsTableData from "layouts/tables/data/authorsTableData";
import projectsTableData from "layouts/tables/data/projectsTableData";

// Mock cow data (moved outside of useEffect for reuse)
export const mockCows = [
  {
    cow_id: "COW101",
    farm_id: "FARM001",
    owner_name: "William",
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
    farm_id: "FARM001",
    owner_name: "William",
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
    owner_name: "Phos",
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
    owner_name: "Phos",
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
    mastitis: "negative",
    reproductive_health: "normal",
    lameness: "No",
    general_health: "normal",
  },
  {
    cow_id: "1509",
    farm_id: "29",
    owner_name: "Yemane Abdi",
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
    date_of_birth: "2023-09-10",
    mastitis: "negative",
    reproductive_health: "normal",
    lameness: "no",
    general_health: "sick",
  },
  {
    cow_id: "1550",
    farm_id: "29",
    owner_name: "Yemane Abdi",
    vaccination_date: "2022-06-04",
    udder_health: "Healthy",
    body_condition_score: "2.0",
    deworming_date: "2022-06-15",
    calving_date: "2024-04-01",
    last_calving_date: "2023-01-15",
    recent_insemination_date: "2024-02-30",
    heat_sign_date: "2025-10-10",
    insemination_count: 4, // Exactly 3 inseminations
    pregnancy_status: true, // Not pregnant
    pregnancy_date: "2024-11-20",
    date_of_birth: "2019-10-16",
    mastitis: "CMT +",
    reproductive_health: "Dystocia",
    lameness: "yes",
    general_health: "sick",
  },
  {
    cow_id: "1588",
    farm_id: "29",
    owner_name: "Yemane Abdi",
    vaccination_date: "2020-08-14",
    udder_health: "Healthy",
    body_condition_score: "5.0",
    deworming_date: "2021-05-10",
    calving_date: "2024-04-01",
    last_calving_date: "2023-01-15",
    recent_insemination_date: "2024-02-30",
    heat_sign_date: "2025-10-10",
    insemination_count: 4, // Exactly 3 inseminations
    pregnancy_status: true, // Not pregnant
    pregnancy_date: "2024-11-20",
    date_of_birth: "2018-03-19",
    mastitis: "negative",
    reproductive_health: "normal",
    lameness: "no",
    general_health: "normal",
  },
  {
    cow_id: "1650",
    farm_id: "29",
    owner_name: "Yemane Abdi",
    vaccination_date: "2023-09-20",
    udder_health: "Healthy",
    body_condition_score: "4.0",
    deworming_date: "2024-01-15",
    calving_date: "2024-04-01",
    last_calving_date: "2023-01-15",
    recent_insemination_date: "2024-02-30",
    heat_sign_date: "2025-10-10",
    insemination_count: 4, // Exactly 3 inseminations
    pregnancy_status: true, // Not pregnant
    pregnancy_date: "2024-11-20",
    date_of_birth: "2021-01-23",
    mastitis: "negative",
    reproductive_health: "normal",
    lameness: "no",
    general_health: "normal",
  },
  {
    cow_id: "1697",
    farm_id: "29",
    owner_name: "Yemane Abdi",
    vaccination_date: "2024-06-24",
    udder_health: "Healthy",
    body_condition_score: "3.5",
    deworming_date: "2023-12-15",
    calving_date: "2024-04-01",
    last_calving_date: "2023-01-15",
    recent_insemination_date: "2024-02-30",
    heat_sign_date: "2025-10-10",
    insemination_count: 4, // Exactly 3 inseminations
    pregnancy_status: true, // Not pregnant
    pregnancy_date: "2024-11-20",
    date_of_birth: "2017-01-02",
    mastitis: "negative",
    reproductive_health: "normal",
    lameness: "no",
    general_health: "normal",
  },
  {
    cow_id: "1707",
    farm_id: "29",
    owner_name: "Yemane Abdi",
    vaccination_date: "2018-02-13",
    udder_health: "Healthy",
    body_condition_score: "1.5",
    deworming_date: "2019-05-12",
    calving_date: "2024-04-01",
    last_calving_date: "2023-01-15",
    recent_insemination_date: "2024-02-30",
    heat_sign_date: "2025-10-10",
    insemination_count: 4, // Exactly 3 inseminations
    pregnancy_status: true, // Not pregnant
    pregnancy_date: "2024-11-20",
    date_of_birth: "2016-09-29",
    mastitis: "clinical mastitis",
    reproductive_health: "Abortion",
    lameness: "yes",
    general_health: "sick",
  },
];

const GENERAL_HEALTH_LABELS = {
  1: "Normal",
  2: "Sick",
};

const UDDER_HEALTH_LABELS = {
  1: "4qt Normal",
  2: "3qt Normal",
  3: "2qt Normal",
  4: "1qt Normal",
};

const MASTITIS_LABELS = {
  1: "Negative",
  2: "Clinical Mastitis",
  3: "CMT+",
  4: "CMT++",
  5: "CMT+++",
};

function Tables() {
  // const { searchQuery, setSearchQuery } = useSearch();
  // const [tableSearchInput, setTableSearchInput] = useState(""); // Current input
  // const [tableSearchQuery, setTableSearchQuery] = useState(""); // Query for filtering
  const [searchParams, setSearchParams] = useSearchParams();
  const initialFarmId = searchParams.get("farm_id") || "";

  // seed both input & query from the URL on first render
  const [tableSearchInput, setTableSearchInput] = useState(initialFarmId);
  const [tableSearchQuery, setTableSearchQuery] = useState(initialFarmId);

  // if the URL querystring ever changes (e.g. you click another card),
  // re‑sync both input and query state so your fetch‐effect will fire
  useEffect(() => {
    const p = searchParams.get("farm_id") || "";
    if (p !== tableSearchQuery) {
      setTableSearchInput(p);
      setTableSearchQuery(p);
    }
  }, [searchParams]);

  const [cows, setCows] = useState([]);
  const [assessments, setAssessments] = useState([]); // Store real data
  const [farms, setFarms] = useState([]); // Store farms for ownerName lookup
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [ownerName, setOwnerName] = useState("Unknown");
  // Generate rows using the filtered assessments
  // const { columns } = authorsTableData(); // Keep existing columns
  const { columns: pColumns, rows: pRows } = projectsTableData();

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        // Fetch cows (filtered by farm ID)
        const cowsResponse = await getCows(tableSearchQuery);
        const cowsData = Array.isArray(cowsResponse) ? cowsResponse : cowsResponse.cows || [];

        // Fetch additional data from APIs
        const [
          monitorBirth,
          heatSign,
          inseminationCount,
          pregnancyData,
          assessments, // Fetch doctor assessments
        ] = await Promise.all([
          getMonitorBirthData(tableSearchQuery),
          getHeatSignData(tableSearchQuery, "ALL"),
          getInseminationCountData(tableSearchQuery, "ALL"),
          getMonitorPregnancyData(tableSearchQuery, "ALL"),
          getDoctorAssessments(tableSearchQuery), // Add this line
        ]);

        // Merge all data into a unified structure
        const mergedCows = cowsData.map((cow) => {
          // Find matching assessment for the cow
          // const assessment =
          //   assessments.find(
          //     (a) => a.cow_id === cow.cow_id && a.farm?.farm_id === cow.farm?.farm_id
          //   ) || {};
          const assessment =
            assessments.find((a) => {
              // a.cow is a number, cow.cow_id might be a string
              const cowMatch = String(a.cow) === String(cow.cow_id);
              // a.farm is a string like "28", cow.farm.farm_id is also a string
              const farmMatch = String(a.farm) === String(cow.farm?.farm_id || cow.farm_id);
              return cowMatch && farmMatch;
            }) || {};

          return {
            ...cow,
            calving_date:
              monitorBirth.find((b) => b.cow_id === cow.cow_id)?.calving_date || cow.calving_date,
            last_calving_date:
              monitorBirth.find((b) => b.cow_id === cow.cow_id)?.last_calving_date ||
              cow.last_calving_date,
            heat_sign_date:
              heatSign.find((h) => h.cow_id === cow.cow_id)?.heat_sign_time || cow.heat_sign_date,
            insemination_count:
              inseminationCount.find((i) => i.cow_id === cow.cow_id)?.insemination_count ||
              cow.insemination_count,
            pregnancy_date:
              pregnancyData.find((p) => p.cow_id === cow.cow_id)?.pregnancy_date ||
              cow.pregnancy_date,
            is_pregnant:
              pregnancyData.find((p) => p.cow_id === cow.cow_id)?.is_pregnant || cow.is_pregnant,
            // Merge doctor assessment fields
            vaccination_date: assessment.vaccination_date || cow.vaccination_date || "N/A",
            // mastitis: assessment.mastitis || cow.mastitis || "N/A",
            reproductive_health: assessment.reproductive_health || cow.reproductive_health || "N/A",
            // udder_health: assessment.udder_health || cow.udder_health || "N/A",
            body_condition_score:
              assessment.body_condition_score || cow.body_condition_score || "N/A",
            deworming_date: assessment.deworming_date || cow.deworming_date || "N/A",
            date_of_birth: assessment.date_of_birth || cow.date_of_birth || "N/A",
            // lameness: assessment.lameness || cow.has_lameness || "N/A",
            // general_health: assessment.general_health || cow.general_health || "N/A",
            lameness:
              assessment.has_lameness === true
                ? "Yes"
                : assessment.has_lameness === false
                ? "No"
                : cow.lameness !== undefined
                ? cow.lameness
                : "N/A",
            general_health:
              assessment.general_health !== undefined
                ? GENERAL_HEALTH_LABELS[assessment.general_health] || "Unknown"
                : cow.general_health !== undefined
                ? GENERAL_HEALTH_LABELS[cow.general_health] || "Unknown"
                : "N/A",
            udder_health:
              assessment.udder_health !== undefined
                ? UDDER_HEALTH_LABELS[assessment.udder_health] || "Unknown"
                : cow.udder_health !== undefined
                ? UDDER_HEALTH_LABELS[cow.udder_health] || "Unknown"
                : "N/A",

            // Mastitis: map 1→None, 2→Mild, etc.
            mastitis:
              assessment.mastitis !== undefined
                ? MASTITIS_LABELS[assessment.mastitis] || "Unknown"
                : cow.mastitis !== undefined
                ? MASTITIS_LABELS[cow.mastitis] || "Unknown"
                : "N/A",
          };
        });

        // Conditionally include mock cows
        if (tableSearchQuery?.toLowerCase() === "mock") {
          setCows(mockCows);

          const mockOwner = mockCows[0]?.owner_name || "Unknown";
          setOwnerName(mockOwner);
        } else {
          // const mockCowsForFarm = mockCows.filter((cow) => cow.farm?.farm_id === tableSearchQuery);
          const mockCowsForFarm = mockCows.filter(
            (cow) =>
              cow.farm_id === tableSearchQuery || // Mock cow (flat farm_id)
              cow.farm?.farm_id === tableSearchQuery // Backend cow (nested farm)
          );
          const mergedOwner = farms.find((farm) => farm.farm_id === tableSearchQuery)?.owner_name;

          // Set owner name from mockCows or farms
          const ownerFromMock = mockCowsForFarm[0]?.owner_name;
          const finalOwnerName = ownerFromMock || mergedOwner || "Unknown";

          // Use mergedCows if backend data exists, else use filtered mock data
          setCows(mergedCows.length > 0 ? mergedCows : mockCowsForFarm);
          setOwnerName(finalOwnerName);
        }

        setFarms(await getFarms());
      } catch (err) {
        console.error("Error fetching data:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [tableSearchQuery]);

  // Generate rows **only if cows is defined**
  const rows =
    cows.length > 0
      ? cows.map((cow) => ({
          cow_id: cow.cow_id || "N/A",
          date_of_birth: cow.date_of_birth || "N/A",
          vaccination_date: cow.vaccination_date || "N/A",
          udder_health: cow.udder_health || "N/A",
          body_condition_score: cow.body_condition_score || "N/A",
          deworming_date: cow.deworming_date || "N/A",
          mastitis: cow.mastitis || "N/A",
          reproductive_health: cow.reproductive_health || "N/A",
          lameness: cow.lameness || "N/A",
          general_health: cow.general_health || "N/A",

          // owner_name: farms.find((farm) => farm.farm_id === cow.farm_id)?.owner_name || "N/A",
          owner_name:
            cow.farm?.owner_name ||
            // Use mock farm owner if available, else fallback to backend farms
            mockCows.find((farm) => farm.farm_id === cow.farm_id)?.owner_name ||
            farms.find((farm) => farm.farm_id === cow.farm_id)?.owner_name ||
            "N/A",
        }))
      : [];

  return (
    <DashboardLayout>
      {/* <DashboardNavbar
        searchValue={tableSearchInput}
        onInputChange={setTableSearchInput}
        onSearch={() => setTableSearchQuery(tableSearchInput)}
      /> */}
      <DashboardNavbar
        searchValue={tableSearchInput}
        onInputChange={setTableSearchInput}
        onSearch={() => {
          setTableSearchQuery(tableSearchInput);
          setSearchParams({ farm_id: tableSearchInput });
        }}
      />
      <MDBox pt={6} pb={3}>
        <Grid container spacing={6}>
          <Grid item xs={12}>
            <Card>
              <MDBox
                mx={2}
                mt={-3}
                py={3}
                px={2}
                variant="gradient"
                bgColor="info"
                borderRadius="lg"
                coloredShadow="info"
              >
                <MDTypography variant="h6" color="white">
                  {`${ownerName} Farm - Cow Health and Farm Data`}
                </MDTypography>
              </MDBox>
              <MDBox pt={3}>
                <DataTable
                  table={{
                    columns: authorsTableData().columns, // Use columns from data.js
                    rows:
                      rows.length > 0
                        ? rows
                        : [
                            {
                              // Default row
                              cow_id: "N/A",
                              date_of_birth: "N/A",
                              vaccination_date: "N/A",
                              udder_health: "N/A",
                              body_condition_score: "N/A",
                              deworming_date: "N/A",
                              mastitis: "N/A",
                              reproductive_health: "N/A",
                              lameness: "N/A",
                              general_health: "N/A",

                              // owner_name: "N/A",
                            },
                          ],
                  }}
                  isSorted={false}
                  entriesPerPage={false}
                  showTotalEntries={false}
                  noEndBorder
                />
              </MDBox>
            </Card>
          </Grid>
          <Grid item xs={12}>
            <Card>
              <MDBox
                mx={2}
                mt={-3}
                py={3}
                px={2}
                variant="gradient"
                bgColor="info"
                borderRadius="lg"
                coloredShadow="info"
              >
                <MDTypography variant="h6" color="white">
                  Performance Indicators
                </MDTypography>
              </MDBox>
              <MDBox pt={3}>
                <DataTable
                  // table={{ columns: pColumns, rows: pRows }}
                  table={{
                    columns: projectsTableData(tableSearchQuery, mockCows).columns,
                    rows: projectsTableData(tableSearchQuery, mockCows).rows,
                  }}
                  isSorted={false}
                  entriesPerPage={false}
                  showTotalEntries={false}
                  noEndBorder
                />
              </MDBox>
            </Card>
          </Grid>
        </Grid>
      </MDBox>
      <Footer />
    </DashboardLayout>
  );
}

export default Tables;

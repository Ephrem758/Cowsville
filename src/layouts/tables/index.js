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
  },
];

function Tables() {
  // const { searchQuery, setSearchQuery } = useSearch();
  const [tableSearchInput, setTableSearchInput] = useState(""); // Current input
  const [tableSearchQuery, setTableSearchQuery] = useState(""); // Query for filtering
  const [cows, setCows] = useState([]);
  const [assessments, setAssessments] = useState([]); // Store real data
  const [farms, setFarms] = useState([]); // Store farms for ownerName lookup
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
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
        const [monitorBirth, heatSign, inseminationCount, pregnancyData] = await Promise.all([
          getMonitorBirthData(tableSearchQuery),
          getHeatSignData(tableSearchQuery, "ALL"),
          getInseminationCountData(tableSearchQuery, "ALL"),
          getMonitorPregnancyData(tableSearchQuery, "ALL"),
        ]);

        // Merge all data into a unified structure
        const mergedCows = cowsData.map((cow) => ({
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
        }));

        // Conditionally include mock cows
        if (tableSearchQuery?.toLowerCase() === "mock") {
          setCows(mockCows);
        } else {
          setCows(mergedCows);
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

  // useEffect(() => {
  //   const fetchData = async () => {
  //     setLoading(true);
  //     try {
  //       // Fetch cows (filtered by farm ID if provided)
  //       const cowsResponse = await getCows(tableSearchQuery);
  //       const cowsData = Array.isArray(cowsResponse) ? cowsResponse : cowsResponse.cows || [];

  //       // Fetch doctor assessments
  //       const assessmentsData = await getDoctorAssessments();

  //       // Fetch farms
  //       const farmsData = await getFarms();

  //       // Merge cow data with doctor assessments
  //       const mergedCows = cowsData.map((cow) => {
  //         const assessment = assessmentsData.find((a) => a.cow_id === cow.cow_id);
  //         return {
  //           ...cow,
  //           vaccination_date: assessment?.vaccination_date || "N/A",
  //           udder_health: assessment?.udder_health || "N/A",
  //           body_condition_score: assessment?.body_condition_score || "N/A",
  //           deworming_date: assessment?.deworming_date || "N/A",
  //         };
  //       });

  //       // Conditionally include mock cows
  //       if (tableSearchQuery?.toLowerCase() === "mock") {
  //         if (mergedCows.length === 0) {
  //           setCows(mockCows); // Use mock cows only if no real data
  //         } else {
  //           setCows(mergedCows); // Use real MOCK farm data if available
  //         }
  //       } else {
  //         setCows(mergedCows); // Use real data for other farms
  //       }
  //       setFarms(farmsData);
  //     } catch (err) {
  //       console.error("Error fetching data:", err);
  //       setError(err.message);
  //     } finally {
  //       setLoading(false);
  //     }
  //   };

  //   fetchData();
  // }, [tableSearchQuery]);

  // Generate rows **only if cows is defined**
  const rows =
    cows.length > 0
      ? cows.map((cow) => ({
          cow_id: cow.cow_id || "N/A",
          vaccination_date: cow.vaccination_date || "N/A",
          udder_health: cow.udder_health || "N/A",
          body_condition_score: cow.body_condition_score || "N/A",
          deworming_date: cow.deworming_date || "N/A",
          owner_name: farms.find((farm) => farm.farm_id === cow.farm_id)?.owner_name || "N/A",
        }))
      : [];

  return (
    <DashboardLayout>
      <DashboardNavbar
        searchValue={tableSearchInput}
        onInputChange={setTableSearchInput}
        onSearch={() => setTableSearchQuery(tableSearchInput)}
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
                  Cow Health and Farm Data
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
                              vaccination_date: "N/A",
                              udder_health: "N/A",
                              body_condition_score: "N/A",
                              deworming_date: "N/A",
                              owner_name: "N/A",
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

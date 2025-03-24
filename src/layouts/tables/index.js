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
import { getFarms } from "api/farmsService";
import authorsTableData from "layouts/tables/data/authorsTableData";
import projectsTableData from "layouts/tables/data/projectsTableData";
import { getDoctorAssessments } from "api/farmsService";

function Tables() {
  // const { searchQuery, setSearchQuery } = useSearch();
  const [tableSearchInput, setTableSearchInput] = useState(""); // Current input
  const [tableSearchQuery, setTableSearchQuery] = useState(""); // Query for filtering
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
        const assessmentsData = await getDoctorAssessments();
        const farmsData = await getFarms();
        console.log("All assessments:", assessmentsData); // Check if assessments exist
        console.log("All farms:", farmsData); // Check if farms exist
        setAssessments(assessmentsData);
        setFarms(farmsData);
      } catch (err) {
        console.error("Error fetching data:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Filter assessments based on search query
  const filteredAssessments = assessments.filter((assessment) => {
    const farm = farms.find((farm) => farm.id === assessment.farm_id);
    return (
      assessment.farm_id?.toLowerCase().includes(tableSearchQuery.toLowerCase()) ||
      (farm?.owner_name || "").toLowerCase().includes(tableSearchQuery.toLowerCase()) ||
      tableSearchQuery.trim() === "" // Always include all assessments when no search
    );
  });

  // Generate rows with fallbacks
  let rows = filteredAssessments.map((assessment) => ({
    cow_id: assessment.cow_id || "N/A",
    vaccination_date: assessment.vaccination_date || "N/A",
    udder_health: assessment.udder_health || "N/A",
    body_condition_score: assessment.body_condition_score || "N/A",
    deworming_date: assessment.deworming_date || "N/A",
    owner_name: farms.find((farm) => farm.id === assessment.farm_id)?.owner_name || "N/A",
  }));

  // Add default row if no filtered assessments but data exists
  if (rows.length === 0 && assessments.length > 0) {
    rows = [
      {
        cow_id: "N/A",
        vaccination_date: "N/A",
        udder_health: "N/A",
        body_condition_score: "N/A",
        deworming_date: "N/A",
        owner_name: "N/A",
      },
    ];
  }

  // Add default rows if no assessments or farms exist
  if (assessments.length === 0 || farms.length === 0) {
    rows = [
      {
        cow_id: "N/A",
        vaccination_date: "N/A",
        udder_health: "N/A",
        body_condition_score: "N/A",
        deworming_date: "N/A",
        owner_name: "N/A",
      },
    ];
  }

  // Handle empty search query
  // if (tableSearchQuery.trim() === "") {
  //   // Show all assessments if no search
  //   rows = assessments.map((assessment) => ({
  //     cow_id: assessment.cow_id || "N/A",
  //     vaccination_date: assessment.vaccination_date || "N/A",
  //     udder_health: assessment.udder_health || "N/A",
  //     body_condition_score: assessment.body_condition_score || "N/A",
  //     deworming_date: assessment.deworming_date || "N/A",
  //     owner_name: farms.find((farm) => farm.id === assessment.farm_id)?.owner_name || "N/A",
  //   }));
  // }

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
                  Farm Data
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
                            /* default row */
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
                  table={{ columns: pColumns, rows: pRows }}
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

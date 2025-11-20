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
// start from here
// @mui material components
// import Grid from "@mui/material/Grid";

// // Material Dashboard 2 React components
// import MDBox from "components/MDBox";

// // Material Dashboard 2 React examples
// import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
// import DashboardNavbar from "examples/Navbars/DashboardNavbar";
// import Footer from "examples/Footer";
// import MasterCard from "examples/Cards/MasterCard";
// import DefaultInfoCard from "examples/Cards/InfoCards/DefaultInfoCard";

// // Billing page components
// import PaymentMethod from "layouts/billing/components/PaymentMethod";
// import Invoices from "layouts/billing/components/Invoices";
// import BillingInformation from "layouts/billing/components/BillingInformation";
// import Transactions from "layouts/billing/components/Transactions";

// function Billing() {
//   return (
//     <DashboardLayout>
//       <DashboardNavbar absolute isMini />
//       <MDBox mt={8}>
//         <MDBox mb={3}>
//           <Grid container spacing={3}>
//             <Grid item xs={12} lg={8}>
//               <Grid container spacing={3}>
//                 <Grid item xs={12} xl={6}>
//                   <MasterCard number={4562112245947852} holder="jack peterson" expires="11/22" />
//                 </Grid>
//                 <Grid item xs={12} md={6} xl={3}>
//                   <DefaultInfoCard
//                     icon="account_balance"
//                     title="salary"
//                     description="Belong Interactive"
//                     value="+$2000"
//                   />
//                 </Grid>
//                 <Grid item xs={12} md={6} xl={3}>
//                   <DefaultInfoCard
//                     icon="paypal"
//                     title="paypal"
//                     description="Freelance Payment"
//                     value="$455.00"
//                   />
//                 </Grid>
//                 <Grid item xs={12}>
//                   <PaymentMethod />
//                 </Grid>
//               </Grid>
//             </Grid>
//             <Grid item xs={12} lg={4}>
//               <Invoices />
//             </Grid>
//           </Grid>
//         </MDBox>
//         <MDBox mb={3}>
//           <Grid container spacing={3}>
//             <Grid item xs={12} md={7}>
//               <BillingInformation />
//             </Grid>
//             <Grid item xs={12} md={5}>
//               <Transactions />
//             </Grid>
//           </Grid>
//         </MDBox>
//       </MDBox>
//       <Footer />
//     </DashboardLayout>
//   );
// }

// export default Billing;

// Ends here
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
import MDBox from "components/MDBox";
import MDTypography from "components/MDTypography";
import LogoAsana from "assets/images/small-logos/logo-asana.svg";
import MDAvatar from "components/MDAvatar";
import MDProgress from "components/MDProgress";
import Icon from "@mui/material/Icon";
import PropTypes from "prop-types";
import React, { useState, useEffect } from "react";

import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Footer from "examples/Footer";
import DataTable from "examples/Tables/DataTable";
import averageStatisticsData from "layouts/Average Statistics/averageStatisticsData";
import mockCows from "layouts/Average Statistics/mockData";
import mockClusters from "layouts/Average Statistics/mockClusters";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import {
  getCows,
  getMonitorBirthData,
  getHeatSignData,
  getInseminationCountData,
  getMonitorPregnancyData,
} from "api/farmsService";

// Data
import authorsTableData from "layouts/tables/data/authorsTableData";
import projectsTableData from "layouts/tables/data/projectsTableData";

// function AverageStatistics() {
//   const { columns, rows } = authorsTableData();
//   const { columns: pColumns, rows: pRows } = projectsTableData();

//   return (
//     <DashboardLayout>
//       <DashboardNavbar />
//       <MDBox pt={6} pb={3}>
//         <Grid container spacing={6}>
//           <Grid item xs={12}>
//             <Card>
//               <MDBox
//                 mx={2}
//                 mt={-3}
//                 py={3}
//                 px={2}
//                 variant="gradient"
//                 bgColor="info"
//                 borderRadius="lg"
//                 coloredShadow="info"
//               >
//                 <MDTypography variant="h6" color="white">
//                   Average Statistics for all farms
//                 </MDTypography>
//               </MDBox>
//               <MDBox pt={3}>
//                 <DataTable
//                   table={{ columns: pColumns, rows: pRows }}
//                   isSorted={false}
//                   entriesPerPage={false}
//                   showTotalEntries={false}
//                   noEndBorder
//                 />
//               </MDBox>
//             </Card>
//           </Grid>
//         </Grid>
//       </MDBox>
//       <Footer />
//     </DashboardLayout>
//   );
// }

// export default AverageStatistics;
import { calculateDaysDifference } from "utils/helpers";

function AverageStatistics() {
  const [cows, setCows] = useState([]); // State to store all cows
  const [loading, setLoading] = useState(false); // Loading state
  const [error, setError] = useState(null); // Error state
  const [selectedClusterId, setSelectedClusterId] = useState("ALL");

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        // Fetch all cows
        const allCows = await getCows();

        // Fetch additional data for all cows
        const [monitorBirth, heatSign, inseminationCount, pregnancyData] = await Promise.all([
          getMonitorBirthData("ALL"), // Fetch all calving data
          getHeatSignData("ALL"), // Fetch all heat sign data
          getInseminationCountData("ALL"), // Fetch all insemination data
          getMonitorPregnancyData("ALL"), // Fetch all pregnancy data
        ]);

        // Merge all data into a unified structure
        const mergedCows = allCows.map((cow) => ({
          ...cow,
          calving_date: monitorBirth.find((b) => b.cow_id === cow.cow_id)?.calving_date || "N/A",
          last_calving_date:
            monitorBirth.find((b) => b.cow_id === cow.cow_id)?.last_calving_date || "N/A",
          heat_sign_date: heatSign.find((h) => h.cow_id === cow.cow_id)?.heat_sign_time || "N/A",
          recent_insemination_date:
            inseminationCount.find((i) => i.cow_id === cow.cow_id)?.insemination_time || "N/A", // Added this line
          insemination_count:
            inseminationCount.find((i) => i.cow_id === cow.cow_id)?.insemination_count || 0,
          pregnancy_date:
            pregnancyData.find((p) => p.cow_id === cow.cow_id)?.pregnancy_date || "N/A",
          is_pregnant: pregnancyData.find((p) => p.cow_id === cow.cow_id)?.is_pregnant || false,
        }));

        // If the API is down or returned no data, fall back to mock data
        if (!mergedCows || mergedCows.length === 0) {
          setCows(mockCows);
        } else {
          setCows(mergedCows);
        }
      } catch (err) {
        console.error("Error fetching data:", err);
        setError(err.message);
        // Fall back to mock data so the table remains visible while backend is down
        setCows(mockCows);
      } finally {
        setLoading(false);
      }
    };

    // Fast-fallback timeout to mock data to reduce perceived load time
    const timeoutId = setTimeout(() => {
      setError((prev) => prev || "Request timed out");
      setCows((prev) => (prev && prev.length ? prev : mockCows));
      setLoading(false);
    }, 1200);

    fetchData().finally(() => {
      clearTimeout(timeoutId);
    });
  }, []);

  // Derive cows filtered by selected cluster
  const selectedCluster = mockClusters.find((c) => c.id === selectedClusterId) || mockClusters[0];
  const filteredCows =
    selectedClusterId === "ALL" || !selectedCluster?.farm_ids?.length
      ? cows
      : cows.filter((cow) => selectedCluster.farm_ids.includes(String(cow.farm_id)));

  // Pass filtered cows to the averageStatisticsData function
  const { columns, rows } = averageStatisticsData(filteredCows);

  return (
    <DashboardLayout>
      <DashboardNavbar
        searchValue=""
        onInputChange={() => {}}
        onSearch={() => {}}
        onSearchChange={() => {}}
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
                  {selectedClusterId === "ALL"
                    ? "Average Statistics for all farms"
                    : `Average Statistics — ${selectedCluster?.name}`}
                </MDTypography>
              </MDBox>
              <MDBox pt={3}>
                <MDBox px={2} pb={2}>
                  <FormControl size="small" sx={{ minWidth: 220, maxWidth: 260 }}>
                    <InputLabel id="cluster-select-label">Cluster</InputLabel>
                    <Select
                      labelId="cluster-select-label"
                      id="cluster-select"
                      value={selectedClusterId}
                      label="Cluster"
                      sx={{ fontSize: "0.95rem" }}
                      onChange={(e) => setSelectedClusterId(e.target.value)}
                    >
                      {mockClusters.map((cluster) => (
                        <MenuItem key={cluster.id} value={cluster.id} sx={{ fontSize: "0.95rem" }}>
                          {cluster.name}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </MDBox>
                {loading && (
                  <MDTypography variant="button" color="text" px={2}>
                    Loading statistics...
                  </MDTypography>
                )}
                {error && !loading && (
                  <MDTypography variant="button" color="error" px={2}>
                    {error} — showing sample data
                  </MDTypography>
                )}
                <DataTable
                  table={{ columns, rows }} // Pass columns and rows to DataTable
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

export default AverageStatistics;

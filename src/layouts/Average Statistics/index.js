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

        setCows(mergedCows);
      } catch (err) {
        console.error("Error fetching data:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Pass all cows to the averageStatisticsData function
  const { columns, rows } = averageStatisticsData(cows);

  return (
    <DashboardLayout>
      <DashboardNavbar />
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
                  Average Statistics for all farms
                </MDTypography>
              </MDBox>
              <MDBox pt={3}>
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

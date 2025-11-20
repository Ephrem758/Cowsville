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

// Material Dashboard 2 React components
import MDBox from "components/MDBox";
// Custom styles for MDButton
import MDButtonRoot from "components/MDButton/MDButtonRoot";
import MDButton from "components/MDButton";
import MDTypography from "components/MDTypography";
import MDInput from "components/MDInput";

// Material Dashboard 2 React example components
import { useState, useEffect, useMemo } from "react";
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Footer from "examples/Footer";
import ReportsBarChart from "examples/Charts/BarCharts/ReportsBarChart";
import ReportsLineChart from "examples/Charts/LineCharts/ReportsLineChart";
import ComplexStatisticsCard from "examples/Cards/StatisticsCards/ComplexStatisticsCard";
import {
  getFarms,
  getCows,
  getCowDetails,
  getHeatSignData,
  getInseminationRecords,
  getDateOfAI,
  getReproductionRecords,
  getHeatSignWindow,
  getBirthRecords,
  getPregnancyRecords,
} from "api/farmsService";
import SimpleLineChart from "layouts/dashboard/data/SimpleLineChart";

// Data
import reportsBarChartData from "layouts/dashboard/data/reportsBarChartData";
// import reportsLineChartData from "layouts/dashboard/data/reportsLineChartData";

// Dashboard components
import Projects from "layouts/dashboard/components/Projects";
import OrdersOverview from "layouts/dashboard/components/OrdersOverview";

function Dashboard() {
  const [searchInput, setSearchInput] = useState(""); // Current input value
  const [searchQuery, setSearchQuery] = useState(""); // Query to filter farms
  const [farms, setFarms] = useState([]); // Real data from backend
  const [selectedFarm, setSelectedFarm] = useState(null); // Track selected farm
  const [cows, setCows] = useState([]); // New state for cows
  const [cowSearchInput, setCowSearchInput] = useState(""); // Cow search input
  const [selectedCow, setSelectedCow] = useState(null); // Selected cow data
  const [loading, setLoading] = useState(false); // For future use
  const [error, setError] = useState(null); // For future use

  // Fetch farms when searchQuery changes
  useEffect(() => {
    const fetchFarms = async () => {
      setLoading(true);
      try {
        const farmsData = await getFarms(searchQuery);
        // Ensure farmsData is always an array
        setFarms(Array.isArray(farmsData) ? farmsData : []);
      } catch (err) {
        setError(err.message);
        setFarms([]); // Set empty array on error
      } finally {
        setLoading(false);
      }
    };

    fetchFarms();
  }, [searchQuery]); // Only re-run on searchQuery change

  // Ensure farms is always an array before filtering
  const filteredFarms = Array.isArray(farms)
    ? farms.filter((farm) => {
        return (
          farm.farm_id?.toLowerCase().includes(searchQuery.toLowerCase()) ||
          farm.owner_name?.toLowerCase().includes(searchQuery.toLowerCase())
        );
      })
    : [];

  // Get firstFarm (derive after filteredFarms)
  const firstFarm = filteredFarms.length > 0 ? filteredFarms[0] : null;
  // Sync selectedFarm with firstFarm
  useEffect(() => {
    setSelectedFarm(firstFarm);
  }, [firstFarm]);

  // Fetch cows when a farm is selected
  useEffect(() => {
    const fetchCows = async () => {
      if (!selectedFarm) {
        // If no farm is selected, fetch all cows and add mock data
        try {
          const allCows = await getCows();
          const mockCows = [
            {
              cow_id: "COW123",
              heat_sign_time: "2024-03-21T06:00:00Z",
              farm_id: "MOCK",
              owner_name: "Phos Abdi",
              heat_signs: "Bellowing, Restlessness, Off-Feed",
              dalc: "5 days",
              last_date_insemination: "21 DEC 9:34 PM",
              insemination_number: "3",
              breed: "Zebu",
              calving_date: "21 Dec 10:15 AM",
            },
            {
              cow_id: "COW456",
              heat_sign_time: "2024-03-21T08:00:00Z",
              farm_id: "MOCK",
              owner_name: "Abebe Alemayehu",
              heat_signs: "Mounting, Mucus Discharge",
              dalc: "7 days",
              date_of_ai: "15 MAR 2:15 PM",
              insemination_number: "2",
              breed: "Holstein",
            },
            {
              cow_id: "16",
              heat_sign_time: "2024-03-21T06:00:00Z",
              farm_id: "MOCK",
              heat_signs: "Bellowing, Restlessness, Off-Feed",
              dalc: "5 days",
              date_of_ai: "21 DEC 9:34 PM",
              insemination_number: "3",
              breed: "Zebu",
            },
          ];
          setCows([...allCows, ...mockCows]);
        } catch (err) {
          console.error("Failed to fetch cows:", err);
          setCows([]);
        }
      } else {
        // If a real farm is selected, fetch only its cows (no mocks)
        try {
          const farmId = selectedFarm.farm_id;
          console.log("Fetching cows for farm ID:", farmId);
          const apiCows = await getCows(farmId);
          console.log("Fetched cows:", apiCows);
          setCows(apiCows); // Only real cows for the selected farm
        } catch (err) {
          console.error("Failed to fetch cows:", err);
          setCows([]);
        }
      }
    };
    fetchCows();
  }, [selectedFarm?.farm_id]); // Only depend on farm_id

  // Handle cow search functionality
  const handleCowSearch = async () => {
    try {
      const trimmedInput = cowSearchInput.trim();
      if (!trimmedInput) {
        setSelectedCow(null);
        return;
      }

      // 1. Try to find the cow in the already-fetched list for the selected farm
      const localCow = cows.find((cow) => {
        const cowFarmId = cow.farm?.farm_id || cow.farm_id;
        return (
          cow.cow_id?.toLowerCase() === trimmedInput.toLowerCase() &&
          (cow.farm_id === "MOCK" || cowFarmId === selectedFarm?.farm_id)
        );
      });

      if (localCow) {
        if (localCow.farm_id === "MOCK") {
          setSelectedCow(localCow);
          return;
        }

        const farmId = localCow.farm?.farm_id || localCow.farm_id;
        console.log("Using cached cow data for:", localCow.cow_id, "farm:", farmId);

        const [heatSignWindow, pregnancyRecords, birthRecords] = await Promise.all([
          getHeatSignWindow(farmId, localCow.cow_id),
          getPregnancyRecords(farmId, localCow.cow_id),
          getBirthRecords(farmId, localCow.cow_id),
        ]);

        const firstHeat = heatSignWindow[0] || {};
        const firstPreg = pregnancyRecords[0] || {};
        const firstBirth = birthRecords[0] || {};

        const updatedCowFromCache = {
          ...localCow,
          heat_sign_time: heatSignWindow.length > 0 ? firstHeat.start : "N/A",
          heat_signs: heatSignWindow.length > 0 ? firstHeat.signs : "No heat signs recorded",
          fertility_window: heatSignWindow,
          pregnancies: pregnancyRecords,
          births: birthRecords,
          calving_date: birthRecords.length > 0 ? firstBirth.calvingDate : "N/A",
          last_date_insemination: pregnancyRecords.length > 0 ? firstPreg.date : "N/A",
          breed_name: String(localCow.breed || "N/A"),
          average_daily_milk: String(localCow.average_daily_milk || "N/A"),
          lactation_number: String(localCow.lactation_number || "N/A"),
        };

        setSelectedCow(updatedCowFromCache);
        return;
      }

      // Fetch cow details directly from the backend
      const cowDetails = await getCowDetails(trimmedInput);
      if (!cowDetails) {
        console.warn("Cow not found for ID:", trimmedInput);
        setSelectedCow(null);
        return;
      }

      console.log("Found cow details:", cowDetails);

      const farmId = cowDetails.farm?.farm_id || cowDetails.farm_id;

      // Check if the current farm matches the cow's farm
      if (!selectedFarm || selectedFarm.farm_id !== farmId) {
        // Fetch the farm details for the cow's farm
        const farmsData = await getFarms(farmId);
        const newFarm = farmsData.find((farm) => farm.farm_id === farmId);

        if (newFarm) {
          setSelectedFarm(newFarm); // Update the selected farm
        } else {
          console.error("Farm not found for ID:", farmId);
          setSelectedCow(null);
          return;
        }
      }

      // Fetch additional data for the cow using the new reproduction API
      const [inseminationRecords, heatSignWindow, pregnancyRecords, birthRecords] =
        await Promise.all([
          getInseminationRecords(farmId, cowDetails.cow_id),
          getHeatSignWindow(farmId, cowDetails.cow_id),
          getPregnancyRecords(farmId, cowDetails.cow_id),
          getBirthRecords(farmId, cowDetails.cow_id),
        ]);

      console.log("Fetched data for cow:", cowDetails.cow_id, {
        heatSignWindow,
        pregnancyRecords,
        birthRecords,
      });

      // Get the first records for display
      const firstHeat = heatSignWindow[0] || {};
      const firstPreg = pregnancyRecords[0] || {};
      const firstBirth = birthRecords[0] || {};

      // Update the selected cow with all required fields
      const updatedCow = {
        ...cowDetails,
        farm_id: cowDetails.farm?.farm_id || cowDetails.farm_id,
        heat_sign_time: heatSignWindow.length > 0 ? firstHeat.start : "N/A",
        heat_signs: heatSignWindow.length > 0 ? firstHeat.signs : "No heat signs recorded",
        number_of_inseminations: inseminationRecords.length || 0,
        date_of_ai: pregnancyRecords.length > 0 ? firstPreg.date : "N/A",
        breed: String(cowDetails.breed || "N/A"),
        owner_name: cowDetails.farm?.owner_name || "N/A",
        fertility_window: heatSignWindow,
        pregnancies: pregnancyRecords,
        births: birthRecords,
        heat_sign_end: heatSignWindow.length > 0 ? firstHeat.end : "N/A",
        heat_signs_seen: heatSignWindow.length > 0 ? firstHeat.signs : "No heat signs recorded",
        calving_date: birthRecords.length > 0 ? firstBirth.calvingDate : "N/A",
        last_date_insemination: pregnancyRecords.length > 0 ? firstPreg.date : "N/A",
        breed_name: String(cowDetails.breed || "N/A"),
        average_daily_milk: String(cowDetails.average_daily_milk || "N/A"),
        lactation_number: String(cowDetails.lactation_number || "N/A"),
      };

      console.log("Updated cow data:", updatedCow);
      setSelectedCow(updatedCow);

      // Only add to cows if it doesn't exist
      setCows((prevCows) => {
        const exists = prevCows.some((cow) => cow.cow_id === cowDetails.cow_id);
        return exists ? prevCows : [...prevCows, updatedCow];
      });
    } catch (err) {
      console.error("Failed to fetch cow details:", err);
      setSelectedCow(null);
    }
  };

  // Handle loading/error states
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  // const selectedFarm = filteredFarms.length > 0 ? filteredFarms[0] : mockFarms[0]; // Default to first mock farm

  return (
    <DashboardLayout>
      <DashboardNavbar
        searchValue={searchInput}
        onInputChange={setSearchInput}
        onSearch={() => setSearchQuery(searchInput)} // Update query on Enter
      />
      <MDBox py={3}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6} lg={3}>
            <MDBox mb={1.5}>
              <ComplexStatisticsCard
                color="dark"
                icon="weekend"
                title="Total cows"
                count={firstFarm?.total_number_of_cows || "N/A"}
                // percentage={{
                //   color: "success",
                //   amount: "+55%",
                //   label: "than lask week",
                // }}
              />
            </MDBox>
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <MDBox mb={1.5}>
              <ComplexStatisticsCard
                icon="leaderboard"
                title="Daily milk allowance (L)"
                count={firstFarm?.total_daily_milk || "N/A"}
              />
            </MDBox>
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <MDBox mb={1.5}>
              <ComplexStatisticsCard
                color="success"
                icon="house"
                title="Address"
                count={firstFarm?.address || "N/A"}
              />
            </MDBox>
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <MDBox mb={1.5}>
              <ComplexStatisticsCard
                color="primary"
                icon="phone"
                title="Phone number"
                count={firstFarm?.telephone_number || "N/A"}
                // percentage={{
                //   color: "success",
                //   amount: "",
                //   label: "Just updated",
                // }}
              />
            </MDBox>
          </Grid>
        </Grid>
        {/* Cow ID search bar  */}
        <MDBox mb={3}>
          <MDTypography variant="h6" gutterBottom>
            Search Cow by ID
          </MDTypography>
          <MDBox display="flex" alignItems="center">
            <MDInput
              value={cowSearchInput}
              onChange={(e) => setCowSearchInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handleCowSearch();
                }
              }}
              sx={{ width: "100%", maxWidth: "400px", marginRight: 1 }}
              placeholder="Enter Cow ID..."
            />
            <MDButton variant="gradient" color="info" onClick={handleCowSearch}>
              Search
            </MDButton>
          </MDBox>
        </MDBox>
        {/* title */}
        <MDBox mt={2} mb={2}>
          <MDTypography variant="h5" fontWeight="bold" color="info">
            {selectedCow
              ? `Fertility Window: ${selectedCow.farm?.owner_name} Farm; COW ID = ${selectedCow.cow_id}`
              : `Fertility Window - ${selectedFarm?.owner_name || "Farm"}`}
          </MDTypography>
        </MDBox>
        <MDBox mt={4.5}>
          <Grid container spacing={3}>
            {/* <Grid item xs={12} md={6} lg={4}>
              <MDBox mb={3}>
                <ReportsBarChart
                  color="info"
                  title="website views"
                  description="Last Campaign Performance"
                  date="campaign sent 2 days ago"
                  chart={reportsBarChartData}
                />
              </MDBox>
            </Grid> */}
            <Grid item xs={12} md={6} lg={4}>
              <MDBox mb={3}>
                {selectedCow ? (
                  <SimpleLineChart cow={selectedCow} />
                ) : (
                  <MDBox>No cow selected</MDBox>
                )}
              </MDBox>
            </Grid>
          </Grid>
        </MDBox>
        {/* start */}
        <MDBox>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6} lg={8}>
              <Projects
                cows={
                  selectedFarm
                    ? cows.filter((cow) => {
                        // Handle both nested farm object and direct farm_id
                        const cowFarmId = cow.farm?.farm_id || cow.farm_id;
                        return cowFarmId === selectedFarm.farm_id;
                      })
                    : []
                }
                farm={firstFarm}
              />
            </Grid>
            <Grid item xs={12} md={6} lg={4}>
              <OrdersOverview cow={selectedCow} />
            </Grid>
          </Grid>
        </MDBox>
        {/* end */}
      </MDBox>
      <Footer />
    </DashboardLayout>
  );
}

export default Dashboard;

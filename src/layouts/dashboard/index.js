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
  getInseminationCount,
  getDateOfAI,
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
        setFarms(farmsData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchFarms();
  }, [searchQuery]); // Only re-run on searchQuery change

  useEffect(() => {
    console.log("Current cows:", cows); // Check if mock cow is present
  }, [cows]);

  const filteredFarms = farms.filter((farm) => {
    return (
      farm.farm_id?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      farm.owner_name?.toLowerCase().includes(searchQuery.toLowerCase())
    );
  });

  // Get firstFarm (derive after filteredFarms)
  const firstFarm = filteredFarms.length > 0 ? filteredFarms[0] : null;
  // Sync selectedFarm with firstFarm
  useEffect(() => {
    setSelectedFarm(firstFarm);
  }, [firstFarm]);

  // Fetch cows when a farm is selected
  // useEffect(() => {
  //   const fetchCows = async () => {
  //     if (!selectedFarm) return;

  //     try {
  //       const farmId = selectedFarm?.farm_id;
  //       const apiCows = await getCows(farmId);

  //       // Add mock cows for testing
  //       const mockCows = [
  //         {
  //           cow_id: "COW123",
  //           heat_sign_time: "2024-03-21T06:00:00Z",
  //           farm_id: "MOCK",
  //           heat_signs: "Bellowing, Restlessness, Off-Feed",
  //           dalc: "5 days",
  //           date_of_ai: "21 DEC 9:34 PM",
  //           insemination_number: "3",
  //           breed: "Zebu",
  //         },
  //         {
  //           cow_id: "COW456",
  //           heat_sign_time: "2024-03-21T08:00:00Z",
  //           farm_id: "MOCK",
  //           heat_signs: "Mounting, Mucus Discharge",
  //           dalc: "7 days",
  //           date_of_ai: "15 MAR 2:15 PM",
  //           insemination_number: "2",
  //           breed: "Holstein",
  //         },
  //       ];
  //       setCows([...apiCows, ...mockCows]);
  //     } catch (err) {
  //       console.error("Failed to fetch cows:", err);
  //       setCows([]);
  //     }
  //   };
  //   fetchCows();
  // }, [selectedFarm]);

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
              heat_signs: "Bellowing, Restlessness, Off-Feed",
              dalc: "5 days",
              date_of_ai: "21 DEC 9:34 PM",
              insemination_number: "3",
              breed: "Zebu",
            },
            {
              cow_id: "COW456",
              heat_sign_time: "2024-03-21T08:00:00Z",
              farm_id: "28",
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
          const apiCows = await getCows(farmId);
          setCows(apiCows); // Only real cows for the selected farm
        } catch (err) {
          console.error("Failed to fetch cows:", err);
          setCows([]);
        }
      }
    };
    fetchCows();
  }, [selectedFarm]);

  // Handle cow search functionality
  const handleCowSearch = async () => {
    try {
      // Fetch cow details directly from the backend
      const cowDetails = await getCowDetails(cowSearchInput);
      if (!cowDetails) {
        console.warn("Cow not found for ID:", cowSearchInput);
        setSelectedCow(null);
        return;
      }

      const farmId = cowDetails.farm_id; // Get the farm ID of the cow

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

      // Fetch additional data for the cow
      const [heatSigns, inseminationCount, dateOfAI] = await Promise.all([
        getHeatSignData(farmId, cowDetails.cow_id),
        getInseminationCount(farmId, cowDetails.cow_id),
        getDateOfAI(cowDetails.cow_id),
      ]);

      // Update the selected cow with all required fields
      setSelectedCow({
        ...cowDetails,
        heat_signs: heatSigns || "No heat signs recorded",
        insemination_count: inseminationCount || 0,
        date_of_ai: dateOfAI || "N/A",
        breed: cowDetails.breed || "N/A",
      });

      // Add the cow to the cows state if it doesn't already exist
      setCows((prevCows) => {
        const exists = prevCows.some((cow) => cow.cow_id === cowDetails.cow_id);
        return exists ? prevCows : [...prevCows, cowDetails];
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
                title="Daily milk allowance"
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
              sx={{ width: "100%", maxWidth: "400px", marginRight: 1 }}
              placeholder="Enter Cow ID..."
            />
            <MDButton
              variant="gradient"
              color="info"
              onClick={async () => {
                const foundCow = cows.find(
                  (cow) => cow.cow_id.toLowerCase() === cowSearchInput.toLowerCase()
                );

                if (foundCow) {
                  if (foundCow.farm_id === "MOCK") {
                    // Use mock cow's heat_sign_time directly
                    setSelectedCow(foundCow);
                  } else {
                    // Fetch heat_sign_time from API for real cows
                    const heatSignTime = await getHeatSignData(foundCow.farm_id, foundCow.cow_id);
                    setSelectedCow({
                      ...foundCow,
                      heat_sign_time: heatSignTime || "06:00",
                    });
                    // const updatedCow = {
                    //   ...foundCow,
                    //   heat_sign_time: heatSignTime || "06:00",
                    // };
                    // setSelectedCow(updatedCow);
                  }
                } else {
                  setSelectedCow(null);
                }
              }}
            >
              Search
            </MDButton>
          </MDBox>
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
                  selectedFarm ? cows.filter((cow) => cow.farm_id === selectedFarm.farm_id) : []
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

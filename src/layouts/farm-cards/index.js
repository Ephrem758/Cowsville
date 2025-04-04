// FarmCards.js
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom"; // For navigation
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import MDBox from "components/MDBox";
import MDTypography from "components/MDTypography";
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Footer from "examples/Footer";
import { getFarms, getCows } from "api/farmsService"; // Import API function
import mockFarms from "./mockFarms";
import { mockCows } from "layouts/tables/";

function FarmCards() {
  const navigate = useNavigate();
  const [farms, setFarms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  // Hardcoded farms (replace with API data later)

  // FarmCards.js
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        // Fetch backend farms and cows
        const [farmsResponse, cowsResponse] = await Promise.all([getFarms(), getCows()]);
        const backendFarms = Array.isArray(farmsResponse)
          ? farmsResponse
          : farmsResponse.farms || [];
        const allCows = Array.isArray(cowsResponse) ? cowsResponse : cowsResponse.cows || [];

        // Calculate total cows per farm from backend data
        const backendFarmCowCounts = allCows.reduce((acc, cow) => {
          acc[cow.farm_id] = (acc[cow.farm_id] || 0) + 1;
          return acc;
        }, {});

        // Merge backend farms with calculated totals
        const mergedFarms = backendFarms.map((farm) => ({
          ...farm,
          totalCows: backendFarmCowCounts[farm.id] || 0,
          image: farm.image || "/images/farm-cards/default-image.jpg",
        }));

        // Use mockCows-derived farms if backend data is empty
        if (mergedFarms.length === 0) {
          const mockFarmIds = [...new Set(mockCows.map((cow) => cow.farm_id))];
          const mockFarms = mockFarmIds.map((farmId) => ({
            id: farmId,
            name: mockCows.find((cow) => cow.farm_id === farmId)?.owner_name || "Unnamed Farm",
            totalCows: mockCows.filter((cow) => cow.farm_id === farmId).length,
            image: "/images/farm-cards/default-image.jpg",
          }));
          setFarms(mockFarms);
        } else {
          setFarms(mergedFarms);
        }
      } catch (err) {
        console.error("Error fetching data:", err);

        // Fallback to mockCows-derived farms
        const mockFarmIds = [...new Set(mockCows.map((cow) => cow.farm_id))];
        const mockFarms = mockFarmIds.map((farmId) => ({
          id: farmId,
          name: mockCows.find((cow) => cow.farm_id === farmId)?.owner_name || "Unnamed Farm",
          totalCows: mockCows.filter((cow) => cow.farm_id === farmId).length,
          image: "/images/farm-cards/default-image.jpg",
        }));
        setFarms(mockFarms);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <MDBox pt={6} pb={3}>
        <Grid container spacing={3}>
          {farms.map((farm) => (
            <Grid item xs={12} md={6} lg={4} key={farm.id}>
              <Card
                sx={{
                  cursor: "pointer",
                  transition: "transform 0.2s",
                  "&:hover": { transform: "scale(1.05)" },
                }}
                // onClick={() => navigate(`/tables?farm_id=${farm.id}`)} // Add later
              >
                <MDBox p={3} textAlign="center">
                  <MDBox
                    component="img"
                    src="/images/farm-cards/image-2.jpg"
                    alt={farm.name}
                    width="80%"
                    height="150px"
                    mx="auto"
                    borderRadius="md"
                    mb={2}
                  />
                  <MDTypography variant="h4" fontWeight="bold" color="info" mb={1}>
                    {farm.owner_name} Farm
                  </MDTypography>

                  <MDBox display="flex" alignItems="center" justifyContent="center" mt={1} mb={1.5}>
                    <MDTypography
                      variant="button"
                      color="text"
                      fontWeight="medium"
                      mr={1}
                      sx={{ minWidth: "90px", textAlign: "right" }} // Set min width
                    >
                      Farm ID :
                    </MDTypography>
                    <MDTypography variant="h6" fontWeight="medium" color="info">
                      {farm.farm_id}
                    </MDTypography>
                  </MDBox>

                  {/* Total Cows */}
                  <MDBox display="flex" alignItems="center" justifyContent="center" mb={1}>
                    <MDTypography
                      variant="button"
                      color="text"
                      fontWeight="medium"
                      mr={1}
                      sx={{ minWidth: "80px", textAlign: "right" }} // Set the same min width
                    >
                      Total Cows :
                    </MDTypography>
                    <MDTypography variant="h6" fontWeight="medium" color="info">
                      {farm.totalCows}
                    </MDTypography>
                  </MDBox>
                </MDBox>
              </Card>
            </Grid>
          ))}
        </Grid>
      </MDBox>
      <Footer />
    </DashboardLayout>
  );
}

export default FarmCards;
